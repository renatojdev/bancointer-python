# cria_cobranca_com_vencimento.py


from bancointer.pix.models.resposta_solicitacao_cobranca import (
    RespostaSolicitacaoCobranca,
)
from bancointer.pix.models.solicitacao_cobranca import (
    SolicitacaoCobranca,
)
from bancointer.utils import HttpUtils
from bancointer.utils.constants import (
    HOST,
    HOST_SANDBOX,
    GENERIC_EXCEPTION_MESSAGE,
    PATH_PIX_COBV,
)
from bancointer.utils.environment import Environment
from bancointer.utils.exceptions import ErroApi, BancoInterException, Erro
from bancointer.utils.bancointer_validations import BancoInterValidations


class CriaCobrancaComVencimento(object):

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
            HOST_SANDBOX if ambiente.SANDBOX else HOST,
            client_id,
            client_secret,
            cert,
            conta_corrente,
        )
        print(f"AMBIENTE: {ambiente.value}")

    def criar(
        self, solicitacao_cob_imediata: SolicitacaoCobranca, txid: str = None
    ) -> dict | ErroApi:
        """Metodo para criar uma cobrança com vencimento, neste caso, o txid é definido pelo PSP.
        Escopo requerido: cob.write"""

        path = (
            PATH_PIX_COBV
            if (not txid and txid is not "")
            else f"{PATH_PIX_COBV}/{txid}"
        )

        try:
            # validating txid
            if txid and not BancoInterValidations.validate_txid(txid):
                erro = Erro(502, "Campo 'txid' é inválido.")
                raise BancoInterException(GENERIC_EXCEPTION_MESSAGE, erro)

            # Converting the request to JSON
            response = self.http_util.make_put(
                path, payload=solicitacao_cob_imediata.to_dict()
            )

            if "title" in response:
                raise ErroApi(**response)
            elif "codigo" in response:
                return response
            # Converting the JSON response to an IssueCollectionResponse object
            return RespostaSolicitacaoCobranca(**response).to_dict()
        except ErroApi as e:
            print(f"ErroApi: {e.title}: {e.detail} - violacoes: {e.violacoes}")
            return e.to_dict()
        except BancoInterException as e:
            print(f"BancoInterException.CriaCobrancaComVencimento.criar: {e}")
            return e.erro.to_dict()
        except Exception as e:
            print(f"Exception.CriaCobrancaComVencimento: {e}")
            raise BancoInterException(GENERIC_EXCEPTION_MESSAGE, Erro(502, e))