# test_solicitar_devolucao.py


import json
import unittest
from unittest.mock import patch, MagicMock

from decouple import config

from bancointer.pix.models.devolucao import Devolucao
from bancointer.pix.pix.solicita_devolucao import SolicitaDevolucao
from bancointer.utils.constants import GENERIC_EXCEPTION_MESSAGE
from bancointer.utils.environment import Environment
from bancointer.utils.token_utils import token_file_is_exist


class TestSolicitarDevolucao(unittest.TestCase):

    def setUp(self):
        self.client_id = config("CLIENT_ID")
        self.client_secret = config("CLIENT_SECRET")
        self.cert = (
            config("SSL_DIR_BASE") + config("PUBLIC_KEY_V2"),
            config("SSL_DIR_BASE") + config("PRIVATE_KEY_V2"),
        )
        self.conta_corrente = config("X_INTER_CONTA_CORRENTE")

    @patch("http.client.HTTPSConnection")
    def test_01_solicita_devolucao_success(self, mock_https_connection):
        """Teste de emissão de cobrança"""
        # Mock da resposta para o token de acesso
        mock_token_response = MagicMock()
        mock_token_response.status = 200
        mock_token_response.read.return_value = b'{"access_token": "5e5b232a-381a-477d-83b5-4ac65b6a0679", "token_type": "Bearer", "expires_in": 3600, "scope": "boleto-cobranca.read boleto-cobranca.write", "expires_at": "2024-11-08 07:17:36.580932"}'

        # mock_https_connection.return_value.getresponse.return_value = mock_token_response

        # Cria um mock para a resposta
        busca_pagamento_response_bytes = b"""{"id": "11", "rtrId": "D00416968202412061705DtTa1zV6cQl", "valor": "20.00", "horario": {"solicitacao": "2024-12-06T20:05:45.624Z", "liquidacao": "2024-12-06T20:05:45.628Z"}, "status": "EM_PROCESSAMENTO", "natureza": "ORIGINAL"}"""

        mock_data_response = MagicMock()
        mock_data_response.status = 200
        mock_data_response.read.return_value = busca_pagamento_response_bytes

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

        # Instancia a classe SolicitaDevolucao
        solicita_devolucao = SolicitaDevolucao(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        # Chama o metodo solicitar devolução
        data_response = solicita_devolucao.solicitar(
            "E00416968202412061443oJmW8hQsV3b", "1", "20.00"
        )

        dict_response = json.loads(busca_pagamento_response_bytes)
        devolucao_response = Devolucao(**dict_response).to_dict()

        # Verifica se os dados retornados estão corretos
        self.assertEqual(data_response, devolucao_response)

    @patch("http.client.HTTPSConnection")  # Mocka a classe MyHttpsClient
    def test_02_solicita_devolucao_failure(self, mock_https_client_class):
        """Teste de lançamento de exception"""
        mock_https_client_class = mock_https_client_class.return_value

        # Define o side_effect para simular uma exceção
        mock_https_client_class.return_value.getresponse.side_effect = Exception(
            GENERIC_EXCEPTION_MESSAGE
        )

        # Instancia a classe SolicitaDevolucao
        solicita_devolucao = SolicitaDevolucao(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        # Verifica se a exceção é levantada corretamente
        with self.assertRaises(Exception) as context:
            solicita_devolucao.solicitar("", "", "")

        self.assertEqual(str(context.exception), GENERIC_EXCEPTION_MESSAGE)

    @patch("http.client.HTTPSConnection")  # Mocka a classe MyHttpsClient
    def test_03_solicita_devolucao_failure(self, mock_https_client_class):
        """Teste de buscar pagamento com parametro invalido"""

        solicita_devolucao = SolicitaDevolucao(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        busca_response = solicita_devolucao.solicitar("", "", "")

        self.assertEqual(
            busca_response,
            {
                "codigo": 404,
                "descricao": "O atributo 'solicitaDevolucao.e2eId' é obrigatório.",
            },
        )


if __name__ == "__main__":
    unittest.main()
