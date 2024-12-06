# test_consultar_pix.py


import unittest
from unittest.mock import patch, MagicMock
from decouple import config

from bancointer.pix.pix.consulta_pix import ConsultaPix
from bancointer.utils.constants import GENERIC_EXCEPTION_MESSAGE
from bancointer.utils.environment import Environment
from bancointer.utils.token_utils import token_file_is_exist


class TestConsultarPix(unittest.TestCase):

    def setUp(self):
        self.client_id = config("CLIENT_ID")
        self.client_secret = config("CLIENT_SECRET")
        self.cert = (
            config("SSL_DIR_BASE") + config("PUBLIC_KEY_V2"),
            config("SSL_DIR_BASE") + config("PRIVATE_KEY_V2"),
        )
        self.conta_corrente = config("X_INTER_CONTA_CORRENTE")
        self.e2e_id = "E00416968202412061443oJmW8hQsV3b"

    @patch("http.client.HTTPSConnection")
    def test_01_consulta_pix_success(self, mock_https_connection):
        """Teste de emissão de cobrança"""
        # Mock da resposta para o token de acesso
        mock_token_response = MagicMock()
        mock_token_response.status = 200
        mock_token_response.read.return_value = b'{"access_token": "5e5b232a-381a-477d-83b5-4ac65b6a0679", "token_type": "Bearer", "expires_in": 3600, "scope": "boleto-cobranca.read boleto-cobranca.write", "expires_at": "2024-11-08 07:17:36.580932"}'

        # mock_https_connection.return_value.getresponse.return_value = mock_token_response

        # Cria um mock para a resposta
        cons_pix_response = b"""{"endToEndId": "E00416968202412061443oJmW8hQsV3b", "valor": "20.0", "horario": "2024-12-06T17:43:14.293Z", "txid": "cKSr6ramZAYHSHadpGfeVzektfj708an", "componentesValor": {"original": {"valor": "0.00"}, "saque": {"valor": "20.00", "modalidadeAgente": "AGPSS", "prestadorDoServicoDeSaque": "12345678"}}, "chave": "+5551983334490", "infoPagador": "pagamento SandBox", "devolucoes": []}"""

        mock_data_response = MagicMock()
        mock_data_response.status = 200
        mock_data_response.read.return_value = cons_pix_response

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

        # Instancia a classe EmiteCobranca (aqui pode ser necessário usar a classe real)
        consulta_pix = ConsultaPix(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        # Chama o metodo emitir
        data = consulta_pix.consultar(self.e2e_id)

        # Verifica se os dados retornados estão corretos
        self.assertEqual(
            data,
            {
                "chave": "+5551983334490",
                "componentesValor": {
                    "original": {"valor": "0.00"},
                    "saque": {
                        "modalidadeAgente": "AGPSS",
                        "prestadorDoServicoDeSaque": "12345678",
                        "valor": "20.00",
                    },
                },
                "devolucoes": [],
                "endToEndId": "E00416968202412061443oJmW8hQsV3b",
                "horario": "2024-12-06T17:43:14.293Z",
                "infoPagador": "pagamento SandBox",
                "txid": "cKSr6ramZAYHSHadpGfeVzektfj708an",
                "valor": "20.0",
            },
        )

    @patch("http.client.HTTPSConnection")  # Mocka a classe MyHttpsClient
    def test_02_consulta_pix_failure(self, mock_https_client_class):
        """Teste de lançamento de exception"""
        # Instancia a classe ConsultaPix
        consulta_pix = ConsultaPix(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        # Verifica se a exceção é levantada corretamente
        response = consulta_pix.consultar("e2e invalid")

        self.assertEqual(
            response, {"codigo": 502, "descricao": "Campo 'e2eId' é inválido."}
        )


if __name__ == "__main__":
    unittest.main()
