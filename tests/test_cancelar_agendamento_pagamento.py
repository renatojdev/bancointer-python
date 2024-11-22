# test_cancelar_agendamento_pagamento.py


import unittest
from unittest.mock import MagicMock, patch

from decouple import config

from bancointer.banking.pagamento.cancela_agendamento_pagamento import (
    CancelaAgendamentoPagamento,
)
from bancointer.utils.environment import Environment
from bancointer.utils.token_utils import token_file_is_exist


class TestCancelaAgendamentoPagamento(unittest.TestCase):

    def setUp(self):
        self.client_id = config("CLIENT_ID")
        self.client_secret = config("CLIENT_SECRET")
        self.cert = (
            config("SSL_DIR_BASE") + config("PUBLIC_KEY_V2"),
            config("SSL_DIR_BASE") + config("PRIVATE_KEY_V2"),
        )
        self.conta_corrente = config("X_INTER_CONTA_CORRENTE")

    @patch("http.client.HTTPSConnection")
    def test_01_cancela_agendamento_pagamento_success(self, mock_https_connection):
        # Mock da resposta para o token de acesso
        mock_token_response = MagicMock()
        mock_token_response.read.return_value = b'{"access_token": "5e5b232a-381a-477d-83b5-4ac65b6a0679", "token_type": "Bearer", "expires_in": 3600, "scope": "boleto-cobranca.read boleto-cobranca.write", "expires_at": "2024-11-08 07:17:36.580932"}'
        mock_token_response.status = 200

        # Cria um mock para a resposta

        mock_data_response = MagicMock()
        mock_data_response.read.return_value = b"{}"
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

        cancela_cobranca = CancelaAgendamentoPagamento(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        data = cancela_cobranca.cancelar("4a30390a-9242-4740-bd30-d941d3678a38")

        self.assertEqual(data, {})

    @patch("http.client.HTTPSConnection")  # Mocka a classe MyHttpsClient
    def test_02_cancela_agendamento_pagamento_failure(self, mock_https_connection):
        # Mock da resposta para o token de acesso
        mock_token_response = MagicMock()
        mock_token_response.read.return_value = b'{"access_token": "5e5b232a-381a-477d-83b5-4ac65b6a0679", "token_type": "Bearer", "expires_in": 3600, "scope": "boleto-cobranca.read boleto-cobranca.write", "expires_at": "2024-11-08 07:17:36.580932"}'
        mock_token_response.status = 200

        mock_https_connection.return_value.getresponse.return_value = (
            mock_token_response
        )

        # Cria um mock para a resposta
        response_json = '{"codigo": 422, "descricao": {"title": "Problema no cancelamento de agendamento de boleto", "detail": "O status atual do boleto é AGENDADO_CANCELADO e não permite cancelamento.", "violacoes": []}}'

        mock_data_response = MagicMock()
        mock_data_response.read.return_value = response_json.encode("UTF-8")
        mock_data_response.status = 422  # Unprocessable Entity

        # Configura o mock para a segunda chamada (dados)
        mock_https_connection.return_value.getresponse.return_value = mock_data_response

        cancela_cobranca = CancelaAgendamentoPagamento(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        data = cancela_cobranca.cancelar("1783d19f-ab81-4a54-92a3-a0064f9b26ee")

        assert mock_https_connection.return_value.getresponse.call_count == 1

        self.assertEqual(422, data["codigo"])
        self.assertEqual(
            data["descricao"],
            {
                "codigo": 422,
                "descricao": {
                    "title": "Problema no cancelamento de agendamento de boleto",
                    "detail": "O status atual do boleto é AGENDADO_CANCELADO e não permite cancelamento.",
                    "violacoes": [],
                },
            },
        )

    @patch("http.client.HTTPSConnection")  # Mocka a classe MyHttpsClient
    def test_03_cancela_agendamento_pagamento_failure(self, mock_https_connection):
        # Mock da resposta para o token de acesso
        mock_token_response = MagicMock()
        mock_token_response.read.return_value = b'{"access_token": "5e5b232a-381a-477d-83b5-4ac65b6a0679", "token_type": "Bearer", "expires_in": 3600, "scope": "boleto-cobranca.read boleto-cobranca.write", "expires_at": "2024-11-08 07:17:36.580932"}'
        mock_token_response.status = 200

        mock_https_connection.return_value.getresponse.return_value = (
            mock_token_response
        )

        # Cria um mock para a resposta
        response_json = (
            '{"codigo": 501, "descricao": "Campo \'codigo_transacao\' é requerido."}'
        )

        mock_data_response = MagicMock()
        mock_data_response.read.return_value = response_json.encode("UTF-8")
        mock_data_response.status = 422  # Unprocessable Entity

        # Configura o mock para a segunda chamada (dados)
        mock_https_connection.return_value.getresponse.return_value = mock_data_response

        cancela_cobranca = CancelaAgendamentoPagamento(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        data = cancela_cobranca.cancelar("1783d19f")

        assert mock_https_connection.return_value.getresponse.call_count == 0

        # self.assertEqual(422, data["codigo"])
        self.assertEqual(
            data,
            {"codigo": 501, "descricao": "Campo 'codigo_transacao' é requerido."},
        )


if __name__ == "__main__":
    unittest.main()
