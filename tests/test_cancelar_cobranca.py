# test_cancelar_cobranca.py

import unittest
from unittest.mock import MagicMock, patch

from decouple import config

from bancointer import TipoBaixa
from bancointer.cobranca_v3.cobranca.cancela_cobranca import CancelaCobranca
from bancointer.utils.environment import Environment
from bancointer.utils.token_utils import token_file_is_exist

client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")
cert = (
    config("SSL_DIR_BASE") + config("PUBLIC_KEY_V2"),
    config("SSL_DIR_BASE") + config("PRIVATE_KEY_V2"),
)


class TestCancelaCobranca(unittest.TestCase):

    @patch("bancointer.utils.http_utils.http.client.HTTPSConnection")
    def test_01_cancela_cobranca_success(self, mock_https_connection):
        # Mock da resposta para o token de acesso
        mock_token_response = MagicMock()
        mock_token_response.read.return_value = b'{"access_token": "5e5b232a-381a-477d-83b5-4ac65b6a0679", "token_type": "Bearer", "expires_in": 3600, "scope": "boleto-cobranca.read boleto-cobranca.write", "expires_at": "2024-11-08 07:17:36.580932"}'
        mock_token_response.status = 200

        # Cria um mock para a resposta

        mock_data_response = MagicMock()
        mock_data_response.read.return_value = b"{}"
        mock_data_response.status = 202

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

        cancela_cobranca = CancelaCobranca(
            Environment.SANDBOX, client_id, client_secret, cert
        )

        data = cancela_cobranca.cancelar(
            "4a30390a-9242-4740-bd30-d941d3678a38", TipoBaixa.DEVOLUCAO
        )

        self.assertEqual(data, {})

    @patch("http.client.HTTPSConnection")  # Mocka a classe MyHttpsClient
    def test_02_cancela_cobranca_failure(self, mock_https_connection):

        # Mock da resposta para o token de acesso
        mock_token_response = MagicMock()
        mock_token_response.read.return_value = b'{"access_token": "5e5b232a-381a-477d-83b5-4ac65b6a0679", "token_type": "Bearer", "expires_in": 3600, "scope": "boleto-cobranca.read boleto-cobranca.write", "expires_at": "2024-11-08 07:17:36.580932"}'
        mock_token_response.status = 200

        mock_https_connection.return_value.getresponse.return_value = (
            mock_token_response
        )

        # Cria um mock para a resposta
        response_json = '{"title": "Requisição inválida", "detail": "A cobrança não pode ser cancelada, pois se encontra na situação CANCELADO", "timestamp": "2024-11-13T15:00:56.191475203-03:00","violacoes": [{}]}'

        mock_data_response = MagicMock()
        mock_data_response.read.return_value = response_json.encode("UTF-8")
        mock_data_response.status = 400

        # Configura o mock para a segunda chamada (dados)
        mock_https_connection.return_value.getresponse.return_value = mock_data_response

        cancela_cobranca = CancelaCobranca(
            Environment.SANDBOX, client_id, client_secret, cert
        )

        data = cancela_cobranca.cancelar(
            "1783d19f-ab81-4a54-92a3-a0064f9b26ee", TipoBaixa.ACERTOS
        )

        # Verifica se a exceção é levantada corretamente
        # with self.assertRaises(ErroApi) as context:
        #     cancela_cobranca.cancelar("1783d19f-ab81-4a54-92a3-a0064f9b26ee", Baixa.ACERTOS.value)

        # self.assertEqual(str(context.exception), "Ocorreu um erro no SDK")

        assert mock_https_connection.return_value.getresponse.call_count == 1

        self.assertEqual(400, data['codigo'])
        self.assertEqual(
            data['descricao'],
            {
                "title": "Requisição inválida",
                "detail": "A cobrança não pode ser cancelada, pois se encontra na situação CANCELADO",
                "timestamp": "2024-11-13T15:00:56.191475203-03:00",
                "violacoes": [{}],
            },
        )


if __name__ == "__main__":
    unittest.main()
