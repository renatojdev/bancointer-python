# test_criar_webhook.py


import unittest
from unittest.mock import MagicMock, patch

from decouple import config

from bancointer.pix.webhook.cria_webhook import CriaWebHook
from bancointer.utils.environment import Environment
from bancointer.utils.token_utils import token_file_is_exist


class TestCriarWebhook(unittest.TestCase):

    def setUp(self):
        self.client_id = config("CLIENT_ID")
        self.client_secret = config("CLIENT_SECRET")
        self.cert = (
            config("SSL_DIR_BASE") + config("PUBLIC_KEY_V2"),
            config("SSL_DIR_BASE") + config("PRIVATE_KEY_V2"),
        )
        self.conta_corrente = config("X_INTER_CONTA_CORRENTE")

    @patch("http.client.HTTPSConnection")
    def test_criar_webhook_success(self, mock_https_connection):
        # Mock da resposta para o token de acesso
        mock_token_response = MagicMock()
        mock_token_response.read.return_value = b'{"access_token": "5e5b232a-381a-477d-83b5-4ac65b6a0679", "token_type": "Bearer", "expires_in": 3600, "scope": "boleto-cobranca.read boleto-cobranca.write", "expires_at": "2024-11-08 07:17:36.580932"}'
        mock_token_response.status = 200

        mock_https_connection.return_value.getresponse.return_value = (
            mock_token_response
        )

        # Cria um mock para a resposta
        response_json = b"""{}"""

        mock_data_response = MagicMock()
        mock_data_response.read.return_value = response_json
        mock_data_response.status = 204

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

        cria_webhook = CriaWebHook(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        data = cria_webhook.criar("5511999999999", "https://myendpoint.com")

        self.assertEqual(data, {})

    @patch("http.client.HTTPSConnection")
    def test_criar_webhook_key_failure(self, mock_https_connection):
        # Mock da resposta para o token de acesso
        mock_token_response = MagicMock()
        mock_token_response.read.return_value = b'{"access_token": "5e5b232a-381a-477d-83b5-4ac65b6a0679", "token_type": "Bearer", "expires_in": 3600, "scope": "boleto-cobranca.read boleto-cobranca.write", "expires_at": "2024-11-08 07:17:36.580932"}'
        mock_token_response.status = 200

        mock_https_connection.return_value.getresponse.return_value = (
            mock_token_response
        )

        # Cria um mock para a resposta
        response_json = b"""{}"""

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

        cria_webhook = CriaWebHook(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        data = cria_webhook.criar("xpto", "https://myendpoint.com")

        self.assertEqual(
            data, {"codigo": 502, "descricao": "Campo 'chave' é inválido."}
        )

    @patch("http.client.HTTPSConnection")
    def test_criar_webhook_webhook_failure(self, mock_https_connection):
        # Mock da resposta para o token de acesso
        mock_token_response = MagicMock()
        mock_token_response.read.return_value = b'{"access_token": "5e5b232a-381a-477d-83b5-4ac65b6a0679", "token_type": "Bearer", "expires_in": 3600, "scope": "boleto-cobranca.read boleto-cobranca.write", "expires_at": "2024-11-08 07:17:36.580932"}'
        mock_token_response.status = 200

        mock_https_connection.return_value.getresponse.return_value = (
            mock_token_response
        )

        # Cria um mock para a resposta
        response_json = b"""{}"""

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

        cria_webhook = CriaWebHook(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        data = cria_webhook.criar("5511999999999", "http://myendpoint.com")

        self.assertEqual(
            data,
            {
                "codigo": 502,
                "descricao": "Campo 'webhookUrl' é inválido. Deve iniciar com https://",
            },
        )


if __name__ == "__main__":
    unittest.main()
