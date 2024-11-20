# consulta_saldo.py

from bancointer.banking.models.resposta_consultar_saldo import RespostaConsultarSaldo
from bancointer.utils.environment import Environment
from bancointer.utils import HttpUtils
from bancointer.utils.constants import (
    HOST_SANDBOX,
    HOST,
    PATH_SALDO,
    GENERIC_EXCEPTION_MESSAGE,
)

from bancointer.utils.exceptions import ErroApi, BancoInterException, Erro


class ConsultaSaldo(object):
    def __init__(
        self, ambiente: Environment, client_id, client_secret, cert, conta_corrente=None
    ):
        """Metodo construtor da classe ConsultaSaldo.

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

    def consultar(self, saldo_date: str) -> dict | ErroApi:
        """Recupera as informações do saldo posicional do cliente em uma determinada data.

        Args:
            saldo_date (string <date>): Data de consulta para o saldo posicional.

        Returns:
            dict: json-encoded of a response, `response.json()` dict com os dados do saldo.
        """

        path = f"{PATH_SALDO}?dataSaldo={saldo_date}"

        try:
            # Converting the request to JSON
            response = self.http_util.make_get(path)

            if "title" in response:
                raise ErroApi(**response)
            elif "codigo" in response:
                return response

            return RespostaConsultarSaldo(**response).to_dict()
        except ErroApi as e:
            print(f"ErroApi: {e.title}: {e.detail} - violacoes: {e.violacoes}")
            return e.to_dict()
        except BancoInterException as e:
            print(f"BancoInterException.ConsultaSaldo.consultar: {e}")
            return e.erro.to_dict()
        except Exception as e:
            print(f"Exception.ConsultaSaldo: {e}")
            raise BancoInterException(GENERIC_EXCEPTION_MESSAGE, Erro(502, e))
