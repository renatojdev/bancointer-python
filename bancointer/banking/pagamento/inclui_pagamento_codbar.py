# inclui_pagamento_codbar.py


from bancointer.banking.models.requisicao_pagamento import RequisicaoPagamento
from bancointer.banking.models.resposta_requisicao_pagamento import (
    RespostaRequisicaoPagamento,
)
from bancointer.utils.environment import Environment
from bancointer.utils.constants import (
    HOST_SANDBOX,
    HOST,
    PATH_PAGAMENTO,
    GENERIC_EXCEPTION_MESSAGE,
)
from bancointer.utils.exceptions import BancoInterException, Erro, ErroApi
from bancointer.utils.http_utils import HttpUtils


class IncluiPagamentoCodBar(object):

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

    def incluir(
        self,
        requisicao_pagamento: RequisicaoPagamento,
    ) -> RespostaRequisicaoPagamento | dict | ErroApi:
        """Metodo para inclusão de um pagamento imediato ou agendamento do pagamento de boleto, convênio ou tributo com código de barras.
        Escopo requerido: pagamento-boleto.write"""
        try:
            # Converting the request to JSON
            payload = requisicao_pagamento.to_dict()

            response = self.http_util.make_post(PATH_PAGAMENTO, payload)

            if "title" in response:
                raise ErroApi(**response)
            elif "codigo" in response:
                return response
            # Converting the JSON response to an IssueCollectionResponse object
            return RespostaRequisicaoPagamento(**response)
        except ErroApi as e:
            print(f"ErroApi: {e.title}: {e.detail} - violacoes: {e.violacoes}")
            return e.to_dict()
        except BancoInterException as e:
            print(f"BancoInterException.IncluiPagamentoCodBar.incluir: {e}")
            return e.erro.to_dict()
        except Exception as e:
            print(f"Exception.IncluiPagamentoCodBar: {e}")
            raise BancoInterException(GENERIC_EXCEPTION_MESSAGE, Erro(502, e))
