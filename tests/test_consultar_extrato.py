# test_consultar_extrato.py


import json
import unittest
from unittest.mock import MagicMock, patch

from decouple import config

from bancointer.banking.extrato import ConsultaExtrato
from bancointer.banking.models.resposta_consultar_extrato import (
    RespostaConsultarExtrato,
)
from bancointer.utils.environment import Environment
from bancointer.utils.token_utils import token_file_is_exist


class TestConsultarExtrato(unittest.TestCase):

    def setUp(self):
        self.client_id = config("CLIENT_ID")
        self.client_secret = config("CLIENT_SECRET")
        self.cert = (
            config("SSL_DIR_BASE") + config("PUBLIC_KEY_V2"),
            config("SSL_DIR_BASE") + config("PRIVATE_KEY_V2"),
        )
        self.conta_corrente = config("X_INTER_CONTA_CORRENTE")

    @patch("http.client.HTTPSConnection")
    def test_consultar_extrato_success(self, mock_https_connection):
        # Mock da resposta para o token de acesso
        mock_token_response = MagicMock()
        mock_token_response.read.return_value = b'{"access_token": "5e5b232a-381a-477d-83b5-4ac65b6a0679", "token_type": "Bearer", "expires_in": 3600, "scope": "boleto-cobranca.read boleto-cobranca.write", "expires_at": "2024-11-08 07:17:36.580932"}'
        mock_token_response.status = 200

        mock_https_connection.return_value.getresponse.return_value = (
            mock_token_response
        )

        # Cria um mock para a resposta
        response_json = """{"transacoes": [
                        {
                          "dataEntrada": "2023-11-02",
                          "tipoTransacao": "OUTROS",
                          "tipoOperacao": "D",
                          "valor": "10.00",
                          "titulo": "Ted Enviada",
                          "descricao": "341 0001  0000000123456 Fernanda Itau"
                        },
                        {
                          "dataEntrada": "2023-11-02",
                          "tipoTransacao": "OUTROS",
                          "tipoOperacao": "D",
                          "valor": "10.00",
                          "titulo": "Ted Enviada",
                          "descricao": "341 0001  0000000123456 Fernanda Itau"
                        },
                        {
                          "dataEntrada": "2023-11-12",
                          "tipoTransacao": "OUTROS",
                          "tipoOperacao": "D",
                          "valor": "50.00",
                          "titulo": "Pagamento Fatura Inter",
                          "descricao": "Pagamento De Fatura Cartão Inter"
                        },
                        {
                          "dataEntrada": "2023-11-12",
                          "tipoTransacao": "OUTROS",
                          "tipoOperacao": "C",
                          "valor": "50.00",
                          "titulo": "Est Pagamento Fatura Inter",
                          "descricao": "Pagamento De Fatura Cartão Inter"
                        },
                        {
                          "dataEntrada": "2023-11-12",
                          "tipoTransacao": "OUTROS",
                          "tipoOperacao": "D",
                          "valor": "7968.21",
                          "titulo": "Pagamento Fatura Inter",
                          "descricao": "Pagamento Fatura Cartão Inter"
                        },
                        {
                          "dataEntrada": "2023-11-12",
                          "tipoTransacao": "OUTROS",
                          "tipoOperacao": "C",
                          "valor": "7968.21",
                          "titulo": "Est Pagamento Fatura Inter",
                          "descricao": "Pagamento Fatura Cartão Inter"
                        },
                        {
                          "dataEntrada": "2023-11-12",
                          "tipoTransacao": "OUTROS",
                          "tipoOperacao": "D",
                          "valor": "21.70",
                          "titulo": "Pagamento Fatura Inter"
                        },
                        {
                          "dataEntrada": "2023-11-12",
                          "tipoTransacao": "OUTROS",
                          "tipoOperacao": "C",
                          "valor": "21.70",
                          "titulo": "Est Pagamento Fatura Inter"
                        },
                        {
                          "dataEntrada": "2023-11-12",
                          "tipoTransacao": "OUTROS",
                          "tipoOperacao": "D",
                          "valor": "1.00",
                          "titulo": "Pagamento Fatura Inter",
                          "descricao": "Pagamento Fatura Inter"
                        },
                        {
                          "dataEntrada": "2023-11-12",
                          "tipoTransacao": "OUTROS",
                          "tipoOperacao": "C",
                          "valor": "1.00",
                          "titulo": "Est Pagamento Fatura Inter",
                          "descricao": "Pagamento Fatura Inter"
                        },
                        {
                          "dataEntrada": "2023-11-12",
                          "tipoTransacao": "OUTROS",
                          "tipoOperacao": "D",
                          "valor": "37.21",
                          "titulo": "Pagam. Cemig",
                          "descricao": "Teste Lemes #01"
                        },
                        {
                          "dataEntrada": "2023-11-02",
                          "tipoTransacao": "OUTROS",
                          "tipoOperacao": "D",
                          "valor": "100.01",
                          "titulo": "Pagamento Darf"
                        },
                        {
                          "dataEntrada": "2023-11-15",
                          "tipoTransacao": "OUTROS",
                          "tipoOperacao": "C",
                          "valor": "6.66",
                          "titulo": "Pix Recebido Interno",
                          "descricao": "00019 0006063018 Nome-61248561000107"
                        },
                        {
                          "dataEntrada": "2023-11-15",
                          "tipoTransacao": "OUTROS",
                          "tipoOperacao": "C",
                          "valor": "6.67",
                          "titulo": "Pix Recebido Interno",
                          "descricao": "00019 0006063018 Nome-61248561000107"
                        },
                        {
                          "dataEntrada": "2023-11-15",
                          "tipoTransacao": "OUTROS",
                          "tipoOperacao": "C",
                          "valor": "1.00",
                          "titulo": "Transferencia A Credito",
                          "descricao": "00019 0009848428 Nome-90603455840"
                        }
                      ]
        }"""
        response_json = response_json.encode("utf-8")

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

        consulta_extrato = ConsultaExtrato(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        data = consulta_extrato.consultar("2024-09-01", "2024-09-09")

        resposta = RespostaConsultarExtrato(**json.loads(response_json))

        self.assertEqual(data, resposta.to_dict())


if __name__ == "__main__":
    unittest.main()
