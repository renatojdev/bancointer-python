# recupera_cobranca.py

from bancointer.cobranca_v3.models import RespostaRecuperarCobranca
from bancointer.utils.constants import PATH_COBRANCAS, HOST_SANDBOX
from bancointer.utils.exceptions import BancoInterException, Erro, ErroApi
from bancointer.utils.http_utils import HttpUtils


class RecuperaCobranca(object):
    def __init__(self, client_id, client_secret, cert):
        """Metodo construtor da classe RecuperaCobranca.

        Args:
            client_id (str): Client Id obtido no detalhe da tela de aplicações no IB.
            client_secret (str): Client Secret obtido no detalhe da tela de aplicações no IB.
            cert (tuple): (cert_file_path, key_file_path) PEM path do certificado digital e PEM path da chave publica.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.cert = cert
        self.http_util = HttpUtils(HOST_SANDBOX, client_id, client_secret, cert)

    def recuperar(self, codigo_solicitacao) -> dict | ErroApi:
        """Recupera as informações detalhadas de um boleto atraves do `codigo_solicitacao`.

        Args:
            codigo_solicitacao (string <uuid>): Codigo unico da cobrança.

        Returns:
            dict: json-encoded of a response, `response.json()` dict com os dados do boleto.
        """

        path = f"{PATH_COBRANCAS}/{codigo_solicitacao}"

        try:
            # Converting the request to JSON
            response = self.http_util.make_get(path)

            if "title" in response:
                raise ErroApi(**response)
            elif "codigo" in response:
                return response

            return RespostaRecuperarCobranca(**response).to_dict()
        except ErroApi as e:
            print(f"Exception.API: {e.title}: {e.detail} - violacoes: {e.violacoes}")
            return e.to_dict()
        except BancoInterException as e:
            print(f"Exception.RecupearaCobranca: {e.erro}")
            return e.erro.to_dict()
        except Exception as e:
            print(f"Exception.RecuperaCobranca: {e}")
            erro = Erro(502, "Erro Interno.")
            raise BancoInterException("Ocorreu um erro no SDK", erro)