# inclui_pagamento_pix.py


from bancointer.banking.models.requisicao_pagamento_pix import RequisicaoPagamentoPix
from bancointer.banking.models.resposta_requisicao_pagamento_pix import (
    RespostaRequisicaoPagamentoPix,
)
from bancointer.utils import HttpUtils
from bancointer.utils.bancointer_validations import BancoInterValidations
from bancointer.utils.constants import (
    HOST,
    HOST_SANDBOX,
    GENERIC_EXCEPTION_MESSAGE,
    PATH_PIX_PAGAMENTO,
)
from bancointer.utils.environment import Environment
from bancointer.utils.exceptions import ErroApi, BancoInterException, Erro


class IncluiPagamentoPix(object):

    def __init__(
        self,
        ambiente: Environment,
        client_id,
        client_secret,
        cert,
        conta_corrente=None,
        id_idempotente: str = None,
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
        if id_idempotente is not None:
            if isinstance(id_idempotente, str):
                if BancoInterValidations.validate_x_id_idempotente(id_idempotente):
                    self.http_util.add_custom_header("x-id-idempotente", id_idempotente)
        print(f"AMBIENTE: {ambiente.value}")

    def incluir(
        self,
        requisicao_pagamento: RequisicaoPagamentoPix,
    ) -> RespostaRequisicaoPagamentoPix | dict:
        """Metodo para inclusão de um pagamento/transferência Pix utilizando dados bancários, chave ou código Copia e Cola.
        Escopo requerido: pagamento-pix.write"""
        try:
            # Converting the request to JSON
            payload = requisicao_pagamento.to_dict()

            response = self.http_util.make_post(PATH_PIX_PAGAMENTO, payload)

            if "title" in response:
                raise ErroApi(**response)
            elif "codigo" in response:
                return response
            # Converting the JSON response to an IssueCollectionResponse object
            return RespostaRequisicaoPagamentoPix(**response).to_dict()
        except ErroApi as e:
            print(f"ErroApi: {e.title}: {e.detail} - violacoes: {e.violacoes}")
            return e.to_dict()
        except BancoInterException as e:
            print(f"BancoInterException.IncluiPagamentoPix.incluir: {e}")
            return e.erro.to_dict()
        except Exception as e:
            print(f"Exception.IncluiPagamentoPix: {e}")
            raise BancoInterException(GENERIC_EXCEPTION_MESSAGE, Erro(502, e))
