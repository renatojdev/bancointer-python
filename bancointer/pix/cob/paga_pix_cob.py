# paga_pix_cob.py


from bancointer.utils import HttpUtils
from bancointer.utils.constants import (
    PATH_PIX_COB,
    GENERIC_EXCEPTION_MESSAGE,
    HOST,
    HOST_SANDBOX,
)
from bancointer.utils.environment import Environment
from bancointer.utils.exceptions import ErroApi, BancoInterException, Erro


# Pagar Pix de cobrança imediata (SANDBOX)
class PagaPixCobrancaImediata(object):
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

    def pagar(self, valor: str, txid: str):
        """Metodo para pagar uma cobrança imediata via Pagamento Pix. (Exclusivo para o ambiente Sandbox)
        Escopo requerido: pix.write

        Returns:
            e2e (str): Id único para identificação do Pix Cobrança.
        """
        try:

            response = self.http_util.make_post(
                f"{PATH_PIX_COB}/pagar/{txid}", {"valor": valor}
            )

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
            print(f"BancoInterException.ConsultaPix.consultar: {e}")
            return e.erro.to_dict()
        except Exception as e:
            print(f"Exception.ConsultaPix: {e}")
            raise BancoInterException(GENERIC_EXCEPTION_MESSAGE, Erro(502, e))
