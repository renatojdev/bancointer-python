# exclui_webhook.py


from bancointer.utils import HttpUtils
from bancointer.utils.bancointer_validations import BancoInterValidations
from bancointer.utils.constants import (
    HOST_SANDBOX,
    HOST,
    GENERIC_EXCEPTION_MESSAGE,
    PATH_PIX_WEBHOOK,
)
from bancointer.utils.environment import Environment
from bancointer.utils.exceptions import ErroApi, BancoInterException, Erro


class ExcluiWebhook(object):
    def __init__(
        self,
        ambiente: Environment,
        client_id,
        client_secret,
        cert,
        conta_corrente=None,
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
            HOST_SANDBOX if ambiente.is_sandbox else HOST,
            client_id,
            client_secret,
            cert,
            conta_corrente,
        )
        print(f"AMBIENTE: {ambiente.value}")

    def excluir(self, chave: str) -> dict | ErroApi:
        """Metodo para excluir o webhook de acordo com a chave informada.
        Escopo requerido: webhook.write

        Returns:

        """
        try:
            # validations
            if not chave or chave is None:
                erro = Erro(
                    404,
                    f"O atributo 'excluiWebhook.chave' é obrigatório.",
                )
                raise BancoInterException("Erro de validação", erro)

            if not BancoInterValidations.validate_pix_chave(chave):
                erro = Erro(502, "Campo 'chave' é inválido.")
                raise BancoInterException(GENERIC_EXCEPTION_MESSAGE, erro)

            response = self.http_util.make_delete(f"{PATH_PIX_WEBHOOK}/{chave}")

            if "title" in response:
                raise ErroApi(**response)
            elif "codigo" in response:
                return response
            # Converting the JSON response to an IssueCollectionResponse object
            return response
        except ErroApi as e:
            print(f"ErroApi: {e.title}: {e.detail} - violacoes: {e.violacoes}")
            return e.to_dict()
        except BancoInterException as e:
            print(f"BancoInterException.ExcluiWebhook.excluir: {e}")
            return e.erro.to_dict()
        except Exception as e:
            print(f"Exception.ExcluiWebhook: {e}")
            raise BancoInterException(GENERIC_EXCEPTION_MESSAGE, Erro(502, e))
