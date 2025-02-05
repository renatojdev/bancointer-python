# consulta_pix.py


from bancointer.pix.models.pix import Pix
from bancointer.utils import HttpUtils
from bancointer.utils.bancointer_validations import BancoInterValidations
from bancointer.utils.constants import (
    HOST_SANDBOX,
    HOST,
    GENERIC_EXCEPTION_MESSAGE,
    PATH_PIX_PIX,
)
from bancointer.utils.environment import Environment
from bancointer.utils.exceptions import ErroApi, BancoInterException, Erro


class ConsultaPix(object):
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

    def consultar(self, e2e_id: str) -> Pix | dict | ErroApi:
        """Metodo para consultar um pix através de um determinado EndToEndId..
        Escopo requerido: pix.read
        As transações de Pix retornadas nas consultas são recebimentos que tiveram
        origem de um Pix Cobrança(Cob ou CobV) gerado pela API Pix ou
        IBPJ(Boleto com Pix) pagos via QR Code.

        Returns:
            dict | ErroApi: Com as informações do pix efetuado.
        """
        try:
            # validations
            if not e2e_id or e2e_id is None:
                erro = Erro(
                    404,
                    f"O atributo 'consultaPix.e2eId' é obrigatório.",
                )
                raise BancoInterException("Erro de validação", erro)

            if not BancoInterValidations.validate_e2eid(e2e_id):
                erro = Erro(502, "Campo 'e2eId' é inválido.")
                raise BancoInterException(GENERIC_EXCEPTION_MESSAGE, erro)

            response = self.http_util.make_get(f"{PATH_PIX_PIX}/{e2e_id}")

            if "title" in response:
                raise ErroApi(**response)
            elif "codigo" in response:
                return response
            # Converting the JSON response to an IssueCollectionResponse object
            return Pix(**response).to_dict()
        except ErroApi as e:
            print(f"ErroApi: {e.title}: {e.detail} - violacoes: {e.violacoes}")
            return e.to_dict()
        except BancoInterException as e:
            print(f"BancoInterException.ConsultaPix.consultar: {e}")
            return e.erro.to_dict()
        except Exception as e:
            print(f"Exception.ConsultaPix: {e}")
            raise BancoInterException(GENERIC_EXCEPTION_MESSAGE, Erro(502, e))
