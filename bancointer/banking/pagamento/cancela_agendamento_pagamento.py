# cancela_agendamento_pagamento.py


from bancointer.utils import HttpUtils
from bancointer.utils.bancointer_validations import BancoInterValidations
from bancointer.utils.constants import (
    PATH_PAGAMENTO,
    GENERIC_EXCEPTION_MESSAGE,
    HOST_SANDBOX,
    HOST,
)
from bancointer.utils.environment import Environment
from bancointer.utils.exceptions import Erro, BancoInterException, ErroApi


class CancelaAgendamentoPagamento(object):
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

    def cancelar(self, codigo_transacao) -> dict:
        """Metodo utilizado para cancelar o agendamento do pagamento de um boleto. Escopo requerido: pagamento-boleto.write.

        Args:
            codigo_transacao (string <uuid>): Codigo unico da transacao para cancelamento do agendamento de pagamento.

        Returns:
            Void Object dict {}. Http code 204, if successfully deleted.
        """

        path = f"{PATH_PAGAMENTO}/{codigo_transacao}"

        try:
            if not BancoInterValidations.validate_transaction_code(codigo_transacao):
                erro = Erro(501, "Campo 'codigo_transacao' é requerido.")
                raise BancoInterException(GENERIC_EXCEPTION_MESSAGE, erro)

            # Converting the request to JSON
            response = self.http_util.make_delete(path)

            if "title" in response:
                raise ErroApi(**response)
            elif "codigo" in response:
                return response

            return response
        except ErroApi as e:
            print(f"ErroApi: {e.title}: {e.detail} - violacoes: {e.violacoes}")
            return e.to_dict()
        except BancoInterException as e:
            print(f"BancoInterException.CancelaAgendamentoPagamento.cancelar: {e}")
            return e.erro.to_dict()
        except Exception as e:
            print(f"Exception.CancelaAgendamentoPagamento: {e}")
            raise BancoInterException(GENERIC_EXCEPTION_MESSAGE, Erro(502, e))
