# consulta_extrato.py

from bancointer.banking.models.resposta_consultar_extrato import (
    RespostaConsultarExtrato,
)
from bancointer.utils.date_utils import DateUtils
from bancointer.utils.exceptions import Erro
from bancointer.utils import HttpUtils
from bancointer.utils.constants import HOST_SANDBOX, PATH_EXTRATO

from bancointer.utils.exceptions import ErroApi, BancoInterException, Erro


class ConsultaExtrato(object):
    def __init__(self, client_id, client_secret, cert):
        """Metodo construtor da classe RecuperaCobranca.

        Args:
            client_id (str): Client Id obtido no detalhe da tela de aplicações no IB.
            client_secret (str): Client Secret obtido no detalhe da tela de aplicações no IB.
            cert (tuple): (cert_file_path, key_file_path) PEM path do certificado digital e PEM path da chave publica.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.cert = cert
        self.http_util = HttpUtils(HOST_SANDBOX, client_id, client_secret, cert)

    def consultar(self, data_inicio, data_fim) -> dict | ErroApi:
        """Recupera as informações do extrato do cliente durante um periodo de datas em
        um período específico. O período máximo entre as datas é de 90 dias.

        Args:
            data_inicio (string <date>): Data início da consulta de extrato.
            data_fim (string <date>): Data fim da consulta de extrato.

        Returns:
            dict: json-encoded of a response, `response.json()` dict com os dados do extrato.
        """
        du = DateUtils()
        if du.periodo_dates_extrato_e_valido(data_inicio, data_fim) is False:
            raise BancoInterException(
                "Ocorreu um erro no SDK", Erro(502, "Periodo de datas invalido")
            )

        path = f"{PATH_EXTRATO}?data_inicio={data_inicio}&data_fim={data_fim}"

        try:
            # Converting the request to JSON
            response = self.http_util.make_get(path)

            if "title" in response:
                raise ErroApi(**response)
            elif "codigo" in response:
                return response

            return RespostaConsultarExtrato(**response).to_dict()
        except ErroApi as e:
            print(
                f"Exception.ConsultaExtrato.API: {e.title}: {e.detail} - violacoes: {e.violacoes}"
            )
            return e.to_dict()
        except BancoInterException as e:
            print(f"Exception.ConsultaExtrato: {e}")
            return e.erro.to_dict()
        except Exception as e:
            print(f"Exception.ConsultaExtrato: {e}")
            return Erro(502, e).to_dict()