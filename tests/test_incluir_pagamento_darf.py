# test_incluir_pagamento_darf.py


import json
import unittest
from unittest.mock import MagicMock, patch

from decouple import config

from bancointer.banking.models.requisicao_pagamento_darf import RequisicaoPagamentoDarf
from bancointer.banking.models.resposta_requisicao_pagamento_darf import (
    RespostaRequisicaoPagamentoDarf,
)
from bancointer.banking.pagamento.inclui_pagamento_darf import IncluiPagamentoDarf
from bancointer.utils.constants import GENERIC_EXCEPTION_MESSAGE
from bancointer.utils.environment import Environment
from bancointer.utils.token_utils import token_file_is_exist


class TestIncluirPagamentoDarf(unittest.TestCase):

    def setUp(self):
        self.client_id = config("CLIENT_ID")
        self.client_secret = config("CLIENT_SECRET")
        self.cert = (
            config("SSL_DIR_BASE") + config("PUBLIC_KEY_V2"),
            config("SSL_DIR_BASE") + config("PRIVATE_KEY_V2"),
        )
        self.conta_corrente = config("X_INTER_CONTA_CORRENTE")
        self.payment_request = b"""{
                                "cnpjCpf": "90022400664",
                                "codigoReceita": "0220",
                                "dataVencimento": "2022-01-30",
                                "descricao": "Pagamento DARF Janeiro",
                                "nomeEmpresa": "Minha Empresa",
                                "telefoneEmpresa": "031999911111",
                                "periodoApuracao": "2020-01-31",
                                "valorPrincipal": 47.14,
                                "valorMulta": 27.48,
                                "valorJuros": 10.11,
                                "referencia": "13609400849201739"
                            }"""

    @patch("http.client.HTTPSConnection")
    def test_01_inclui_pagamento_darf_success(self, mock_https_connection):
        """Teste de emissão de cobrança"""
        # Mock da resposta para o token de acesso
        mock_token_response = MagicMock()
        mock_token_response.status = 200
        mock_token_response.read.return_value = b'{"access_token": "5e5b232a-381a-477d-83b5-4ac65b6a0679", "token_type": "Bearer", "expires_in": 3600, "scope": "boleto-cobranca.read boleto-cobranca.write", "expires_at": "2024-11-08 07:17:36.580932"}'

        # mock_https_connection.return_value.getresponse.return_value = mock_token_response

        # Cria um mock para a resposta
        payment_response_bytes = b"""{
                                    "autenticacao": "12345678910433",
                                    "dataPagamento": "23/01/2022",
                                    "tipoRetorno": "PAGAMENTO",
                                    "codigoSolicitacao": "8bbdede4-35db-4ec9-b652-e176841e62c8"
                                }"""

        mock_data_response = MagicMock()
        mock_data_response.status = 200
        mock_data_response.read.return_value = payment_response_bytes

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

        # Instancia a classe IncluiPagamentoDarf
        inclui_pagamento = IncluiPagamentoDarf(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        # Chama o metodo emitir
        data = inclui_pagamento.incluir(
            RequisicaoPagamentoDarf(**json.loads(self.payment_request))
        )

        payment_response = RespostaRequisicaoPagamentoDarf(
            **json.loads(payment_response_bytes)
        )

        # Verifica se os dados retornados estão corretos
        self.assertEqual(data, payment_response)

    @patch("http.client.HTTPSConnection")  # Mocka a classe MyHttpsClient
    def test_02_inclui_pagamento_darf_failure(self, mock_https_client_class):
        """Teste de lançamento de exception"""
        mock_https_client_class = mock_https_client_class.return_value

        # Define o side_effect para simular uma exceção
        mock_https_client_class.return_value.getresponse.side_effect = Exception(
            GENERIC_EXCEPTION_MESSAGE
        )

        # Instancia a classe IncluiPagamentoDarf
        inclui_pagamento = IncluiPagamentoDarf(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        # Verifica se a exceção é levantada corretamente
        with self.assertRaises(Exception) as context:
            inclui_pagamento.incluir(
                RequisicaoPagamentoDarf(**json.loads(self.payment_request))
            )

        self.assertEqual(str(context.exception), GENERIC_EXCEPTION_MESSAGE)


if __name__ == "__main__":
    unittest.main()
