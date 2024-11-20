# consulta_extrato_pdf.py
import os

from bancointer import Util
from bancointer.utils.environment import Environment
from bancointer.utils.date_utils import DateUtils
from bancointer.utils import HttpUtils
from bancointer.utils.constants import (
    HOST_SANDBOX,
    HOST,
    PATH_EXTRATO_PDF,
    GENERIC_EXCEPTION_MESSAGE,
)

from bancointer.utils.exceptions import ErroApi, BancoInterException, Erro


class ConsultaExtratoPDF(object):
    def __init__(
        self, ambiente: Environment, client_id, client_secret, cert, conta_corrente=None
    ):
        """Metodo construtor da classe ConsultaExtrato.

        Args:
            ambiente (Environment): Application Environment, SANDBOX or PRODUCTION.
            client_id (str): Client Id obtido no detalhe da tela de aplicações no IB.
            client_secret (str): Client Secret obtido no detalhe da tela de aplicações no IB.
            cert (tuple): (cert_file_path, key_file_path) PEM path do certificado digital e PEM path da chave publica.
            conta_corrente (str): Conta corrente que será utilizada na operação, caso faça parte da lista de contas correntes da aplicação. Enviar apenas números(incluindo o dígito), e não enviar zeros a esquerda.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.cert = cert
        self.http_util = HttpUtils(
            HOST_SANDBOX if ambiente.SANDBOX else HOST,
            client_id,
            client_secret,
            cert,
            conta_corrente,
        )
        print(f"AMBIENTE: {ambiente.value}")

    def consultar_pdf(
        self, data_inicio, data_fim, download_path: str = "/tmp"
    ) -> dict | ErroApi:
        """Recupera as informações do extrato do cliente durante um periodo de datas em
        um período específico. O período máximo entre as datas é de 90 dias.

        Args:
            data_inicio (string <date>): Data início da consulta de extrato.
            data_fim (string <date>): Data fim da consulta de extrato.
            download_path (str): Path completo para salvar o extrato. Ex: `/tmp/downloads`

        Returns:
            dict: json-encoded of a response, `response.json()` dict com os dados do extrato.
        """

        path = f"{PATH_EXTRATO_PDF}?dataInicio={data_inicio}&dataFim={data_fim}"

        try:
            if DateUtils.periodo_dates_extrato_e_valido(data_inicio, data_fim) is False:
                raise BancoInterException(
                    GENERIC_EXCEPTION_MESSAGE, Erro(502, "Periodo de datas invalido")
                )

            # Converting the request to JSON
            response = self.http_util.make_get(path)

            if "title" in response:
                raise ErroApi(**response)
            elif "codigo" in response:
                return response

            file_path = (
                download_path
                + os.sep
                + f"{DateUtils.get_current_date()}_inter_extrato.pdf"
            )

            return Util.file_save(response, file_path)
        except ErroApi as e:
            print(f"ErroApi: {e.title}: {e.detail} - violacoes: {e.violacoes}")
            return e.to_dict()
        except BancoInterException as e:
            print(f"BancoInterException.ConsultaExtrato.consultar: {e}")
            return e.erro.to_dict()
        except Exception as e:
            print(f"Exception.ConsultaExtrato: {e}")
            raise BancoInterException("Ocorreu um erro no SDK", Erro(502, e))
