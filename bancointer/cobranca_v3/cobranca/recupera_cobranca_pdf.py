# recupera_cobranca_pdf.py

import os

from bancointer import Util
from bancointer.utils.ambient import Ambient

from bancointer.utils.constants import PATH_COBRANCAS, HOST_SANDBOX, HOST
from bancointer.utils.exceptions import BancoInterException, Erro, ErroApi
from bancointer.utils.http_utils import HttpUtils


class RecuperaCobrancaPDF(object):
    def __init__(self, ambiente: Ambient, client_id, client_secret, cert):
        """Metodo construtor da classe.

        Args:
            client_id (str): Client Id obtido no detalhe da tela de aplicações no IB.
            client_secret (str): Client Secret obtido no detalhe da tela de aplicações no IB.
            cert (tuple): (cert_file_path, key_file_path) PEM path do certificado digital e PEM path da chave publica.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.cert = cert
        self.http_util = HttpUtils(
            HOST_SANDBOX if ambiente.SANDBOX else HOST, client_id, client_secret, cert
        )
        print(f"AMBIENTE: {ambiente.value}")

    def recuperar_pdf(self, codigo_solicitacao, download_path) -> bool:
        """Metodo para download de cobranças emitidas no formato PDF.

        Args:
            codigo_solicitacao (string <uuid>): Codigo unico da cobrança
            download_path (str): Path completo para salvar o boleto. Ex: `/tmp/downloads`

        Returns:
            (bool): True em caso de sucesso ou False caso contrario.
        """

        path = f"{PATH_COBRANCAS}/{codigo_solicitacao}/pdf"

        try:
            response = self.http_util.make_get(path)

            if "title" in response:
                raise ErroApi(**response)
            elif "codigo" in response:
                return response

            file_path = download_path + os.sep + codigo_solicitacao + ".pdf"

            return Util.file_save(response, file_path)
        except ErroApi as e:
            print(f"ErroApi: {e.title}: {e.detail} - violacoes: {e.violacoes}")
            return e.to_dict()
        except BancoInterException as e:
            print(f"BancoInterException.RecuperaCobrancaPDF.recuperar_pdf: {e}")
            return e.erro.to_dict()
        except Exception as e:
            print(f"Exception.RecuperaCobrancaPDF: {e}")
            raise BancoInterException("Ocorreu um erro no SDK", Erro(502, e))
