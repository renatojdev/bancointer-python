# busca_pagamento.py


import urllib.parse

from bancointer.banking.models.resposta_busca_pagamento import RespostaBuscaPagamento
from bancointer.utils import HttpUtils
from bancointer.utils.constants import (
    HOST_SANDBOX,
    HOST,
    PATH_PAGAMENTO,
    GENERIC_EXCEPTION_MESSAGE,
)
from bancointer.utils.environment import Environment
from bancointer.utils.exceptions import ErroApi, BancoInterException, Erro


class BuscaPagamento(object):

    def __init__(
        self, ambiente: Environment, client_id, client_secret, cert, conta_corrente=None
    ):
        """Metodo construtor da classe.

        Args:
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

    def buscar(self, query_params: dict) -> RespostaBuscaPagamento | dict:
        """Metodo para obter uma coleção de pagamentos de boletos. Escopo requerido: `pagamento-boleto.read`

        Args:
            query_params (dict): Dict de query parameters para busca de pagamentos.

        Returns:
            dict: json-encoded of a response, `response.json()` dict com os dados da coleção de pagamentos.
        """
        try:
            if query_params is None or len(query_params) == 0:
                erro = Erro(501, "Campo 'query_params' é requerido.")
                raise BancoInterException(GENERIC_EXCEPTION_MESSAGE, erro)

            # Parse a dictionary in url parameters.
            url_params = urllib.parse.urlencode(query_params)

            path = f"{PATH_PAGAMENTO}?{url_params}"

            # Converting the request to JSON
            response = self.http_util.make_get(path)

            if "title" in response:
                raise ErroApi(**response)
            elif "codigo" in response:
                return response

            response = {"pagamentos": response}

            return RespostaBuscaPagamento(**response).to_dict()
        except ErroApi as e:
            print(f"ErroApi: {e.title}: {e.detail} - violacoes: {e.violacoes}")
            return e.to_dict()
        except BancoInterException as e:
            print(f"BancoInterException.BuscaPagamento.buscar: {e}")
            return e.erro.to_dict()
        except Exception as e:
            print(f"Exception.BuscaPagamento: {e}")
            raise BancoInterException(GENERIC_EXCEPTION_MESSAGE, Erro(502, e))
