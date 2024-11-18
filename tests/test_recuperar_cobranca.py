# test_recuperar_cobranca.py
import json
import unittest
from unittest.mock import MagicMock, patch

from decouple import config

from bancointer.cobranca_v3.cobranca import RecuperaCobranca
from bancointer.cobranca_v3.models import RespostaRecuperarCobranca
from bancointer.utils.environment import Environment
from bancointer.utils.token_utils import token_file_is_exist

client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")
cert = (
    config("SSL_DIR_BASE") + config("PUBLIC_KEY_V2"),
    config("SSL_DIR_BASE") + config("PRIVATE_KEY_V2"),
)


class TestRecuperaCobranca(unittest.TestCase):

    @patch("http.client.HTTPSConnection")
    def test_recupera_cobranca_success(self, mock_https_connection):
        # Mock da resposta para o token de acesso
        mock_token_response = MagicMock()
        mock_token_response.read.return_value = b'{"access_token": "5e5b232a-381a-477d-83b5-4ac65b6a0679", "token_type": "Bearer", "expires_in": 3600, "scope": "boleto-cobranca.read boleto-cobranca.write", "expires_at": "2024-11-08 07:17:36.580932"}'
        mock_token_response.status = 200

        mock_https_connection.return_value.getresponse.return_value = (
            mock_token_response
        )

        # Cria um mock para a resposta
        response_json = b"""{
                          "cobranca": {
                            "seuNumero": "00001",
                            "dataEmissao": "2024-11-11",
                            "dataVencimento": "2024-11-21",
                            "valorNominal": 2.5,
                            "tipoCobranca": "SIMPLES",
                            "situacao": "A_RECEBER",
                            "dataSituacao": "2024-11-11",
                            "arquivada": false,
                            "descontos": [
                              {
                                "codigo": "PERCENTUALDATAINFORMADA",
                                "quantidadeDias": 0,
                                "taxa": 1.2
                              }
                            ],
                            "multa": {
                              "codigo": "VALORFIXO",
                              "valor": 100
                            },
                            "mora": {
                              "codigo": "TAXAMENSAL",
                              "taxa": 4.5
                            },
                            "pagador": {
                              "cpfCnpj": "99999999999",
                              "tipoPessoa": "FISICA",
                              "nome": "NOME DO PAGADOR",
                              "endereco": "ENDERECO DO PAGADOR",
                              "bairro": "",
                              "cidade": "CIDADE DO PAGADOR",
                              "uf": "PR",
                              "cep": "80030000",
                              "email": "",
                              "numero": "",
                              "complemento": ""
                            }
                          },
                          "boleto": {
                            "nossoNumero": "3364699211",
                            "codigoBarras": "00000033641836128354683148168282409334777187",
                            "linhaDigitavel": "00000033641836534950656166811518570490033128415"
                          },
                          "pix": {
                            "txid": "336418361731333813000Uusr9kwpzFRNiz",
                            "pixCopiaECola": "000201010212261010014BR.GOV.BCB.PIX2579cdpj-sandbox.partners.uatinter.co/pj-s/v2/cobv/afad912c569348b6b6a3476ca4579a6d52040000530398654042.505802BR5901*6013Belo Horizont61089999999962070503***6304A5CC"
                          }
                        }"""

        mock_data_response = MagicMock()
        mock_data_response.read.return_value = response_json
        mock_data_response.status = 200

        # Configura o mock para a segunda chamada (dados), se token nao existe configura side_effect
        if token_file_is_exist():
            mock_https_connection.return_value.getresponse.return_value = (
                mock_data_response
            )
        else:
            mock_https_connection.return_value.getresponse.side_effect = [
                mock_token_response,
                mock_data_response,
            ]

        recupera_cobranca = RecuperaCobranca(
            Environment.SANDBOX, client_id, client_secret, cert
        )

        data = recupera_cobranca.recuperar("4a30390a-9242-4740-bd30-d941d3678a38")

        resposta = RespostaRecuperarCobranca(**json.loads(response_json))

        self.assertEqual(data["cobranca"], resposta.cobranca)
        self.assertEqual(data["boleto"], resposta.boleto)
        self.assertEqual(data["pix"], resposta.pix)


if __name__ == "__main__":
    unittest.main()
