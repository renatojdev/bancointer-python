# emite_cobranca.py

from bancointer.cobranca_v3.models import RespostaEmitirCobranca
from bancointer.cobranca_v3.models import SolicitacaoEmitirCobranca
from bancointer.utils.constants import PATH_COBRANCAS, HOST_SANDBOX
from bancointer.utils.exceptions import BancoInterException, Erro, ErroApi
from bancointer.utils.http_utils import HttpUtils


class EmiteCobranca(object):
    http_util = HttpUtils(HOST_SANDBOX, "", "", "")

    def __init__(self, client_id, client_secret, cert):
        """Metodo construtor da classe.

        Args:
            client_id (str): Client Id obtido no detalhe da tela de aplicações no IB.
            client_secret (str): Client Secret obtido no detalhe da tela de aplicações no IB.
            cert (tuple): (cert_file_path, key_file_path) PEM path do certificado digital e PEM path da chave publica.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.cert = cert
        self.http_util = HttpUtils(HOST_SANDBOX, client_id, client_secret, cert)

    def emitir(
        self,
        solicitacao_emitir_cobranca: SolicitacaoEmitirCobranca,
    ) -> RespostaEmitirCobranca | dict:
        try:
            # Converting the request to JSON
            payload = solicitacao_emitir_cobranca.to_dict()
            print(f"payload.. {payload}")
            response = self.http_util.make_post(PATH_COBRANCAS, payload)

            if "title" in response:
                raise ErroApi(**response)
            elif "codigo" in response:
                return response
            # Converting the JSON response to an IssueCollectionResponse object
            return RespostaEmitirCobranca(**response)
        except ErroApi as e:
            print(f"Exception.API: {e.title}: {e.detail} - violacoes: {e.violacoes}")
            return e.to_dict()
        except BancoInterException as e:
            print(f"Exception.Emitecobranca: {e.erro}")
            return e.erro.to_dict()
        except Exception as e:
            print(f"Exception.EmiteCobranca: {e}")
            raise BancoInterException(
                "Ocorreu um erro no SDK", Erro(502, e)
            )