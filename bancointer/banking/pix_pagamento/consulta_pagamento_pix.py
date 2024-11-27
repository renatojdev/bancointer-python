# consulta_pagamento_pix.py


from bancointer.banking.models.resposta_consulta_pagamento_pix import (
    RespostaConsultaPagamentoPix,
)
from bancointer.utils import HttpUtils
from bancointer.utils.bancointer_validations import BancoInterValidations
from bancointer.utils.environment import Environment
from bancointer.utils.exceptions import Erro, BancoInterException, ErroApi
from bancointer.utils.constants import (
    PATH_PIX_PAGAMENTO,
    GENERIC_EXCEPTION_MESSAGE,
    HOST_SANDBOX,
    HOST,
)


class ConsultaPagamentoPix(object):

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

    def consultar(self, codigo_solicitacao: str) -> dict | ErroApi:
        """Metodo para consulta de um pagamento/transferência Pix utilizando o codigo solicitação.
        Escopo requerido: pagamento-pix.read

        Args:
            codigo_solicitacao (string <uuid>): Codigo único da transaçao

        Returns:
            Dict object com informações da consulta de pagamento pix.
        """
        try:
            if (
                codigo_solicitacao is None
                or type(codigo_solicitacao) is not str
                or codigo_solicitacao == ""
            ):
                erro = Erro(404, "Campo 'codigo_solicitacao' é requerido.'")
                raise BancoInterException(GENERIC_EXCEPTION_MESSAGE, erro)

            if not BancoInterValidations.validate_transaction_code(codigo_solicitacao):
                erro = Erro(502, "Campo 'codigo_solicitacao' é inválido.'")
                raise BancoInterException(GENERIC_EXCEPTION_MESSAGE, erro)

            # Path to retrieve infos
            path = f"{PATH_PIX_PAGAMENTO}/{codigo_solicitacao}"

            response = self.http_util.make_get(path)

            if "title" in response:
                raise ErroApi(**response)
            elif "codigo" in response:
                return response
            # Converting the JSON response to an IssueCollectionResponse object
            return RespostaConsultaPagamentoPix(**response).to_dict()
        except ErroApi as e:
            print(f"ErroApi: {e.title}: {e.detail} - violacoes: {e.violacoes}")
            return e.to_dict()
        except BancoInterException as e:
            print(f"BancoInterException.ConsultaPagamentoPix.incluir: {e}")
            return e.erro.to_dict()
        except Exception as e:
            print(f"Exception.ConsultaPagamentoPix: {e}")
            raise BancoInterException(GENERIC_EXCEPTION_MESSAGE, Erro(502, e))
