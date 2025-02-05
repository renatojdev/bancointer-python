# solicita_devolucao.py


from bancointer.pix.models.devolucao import Devolucao, NaturezaDevolucao
from bancointer.utils import HttpUtils
from bancointer.utils.bancointer_validations import BancoInterValidations
from bancointer.utils.constants import (
    HOST_SANDBOX,
    HOST,
    GENERIC_EXCEPTION_MESSAGE,
    PATH_PIX_PIX,
)
from bancointer.utils.environment import Environment
from bancointer.utils.exceptions import Erro, BancoInterException, ErroApi


class SolicitaDevolucao(object):
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

    def solicitar(
        self,
        e2e_id: str,
        cli_id: str,
        valor: str,
        natureza: NaturezaDevolucao = None,
        descricao: str = None,
    ):
        """Metodo para solicitar uma devolução através de um E2EID do Pix e do ID da devolução.
        Escopo requerido: pix.write

        Arguments:
            e2e_id (str): Id único para identificação do Pix Cobrança.
            cli_id (str): Id gerado pelo cliente para representar unicamente uma devolução
            valor (str):  Natureza da Devolução Solicitada
            natureza (NaturezaDevolucao): Natureza da Devolução Solicitada. Default: `ORIGINAL`
            descricao (str): Mensagem ao pagador relativa à devolução

        Returns:
            dict | ErroApi: Com as informações dos dados da devolução.
        """
        try:
            # validations
            if not e2e_id or e2e_id is None:
                erro = Erro(
                    404,
                    f"O atributo 'solicitaDevolucao.e2eId' é obrigatório.",
                )
                raise BancoInterException("Erro de validação", erro)

            if not cli_id or cli_id is None:
                erro = Erro(
                    404,
                    f"O atributo 'solicitaDevolucao.id' é obrigatório.",
                )
                raise BancoInterException("Erro de validação", erro)

            if not valor or valor is None:
                erro = Erro(
                    404,
                    f"O atributo 'solicitaDevolucao.valor' é obrigatório.",
                )
                raise BancoInterException("Erro de validação", erro)

            if not BancoInterValidations.validate_e2eid(e2e_id):
                erro = Erro(502, "Campo 'e2eId' é inválido.")
                raise BancoInterException(GENERIC_EXCEPTION_MESSAGE, erro)

            if not BancoInterValidations.is_valid_valor_nominal(valor):
                erro = Erro(502, "Campo 'valor' é inválido.")
                raise BancoInterException(GENERIC_EXCEPTION_MESSAGE, erro)

            payload = {"valor": valor}

            if natureza:
                payload["natureza"] = NaturezaDevolucao.value

            if descricao:
                payload["descricao"] = descricao

            response = self.http_util.make_put(
                f"{PATH_PIX_PIX}/{e2e_id}/devolucao/{cli_id}", payload
            )

            if "title" in response:
                raise ErroApi(**response)
            elif "codigo" in response:
                return response
            # Converting the JSON response to an IssueCollectionResponse object
            return Devolucao(**response).to_dict()
        except ErroApi as e:
            print(f"ErroApi: {e.title}: {e.detail} - violacoes: {e.violacoes}")
            return e.to_dict()
        except BancoInterException as e:
            print(f"BancoInterException.SolicitaDevolucao.consultar: {e}")
            return e.erro.to_dict()
        except Exception as e:
            print(f"Exception.SolicitaDevolucao: {e}")
            raise BancoInterException(GENERIC_EXCEPTION_MESSAGE, Erro(502, e))
