# test_buscar_pagamento_darf.py


import json
import unittest
from unittest.mock import patch, MagicMock

from decouple import config

from bancointer.banking.models.resposta_busca_pagamento_darf import (
    RespostaBuscaPagamentoDarf,
)
from bancointer.banking.pagamento.busca_pagamento_darf import BuscaPagamentoDarf
from bancointer.utils.constants import GENERIC_EXCEPTION_MESSAGE
from bancointer.utils.environment import Environment
from bancointer.utils.token_utils import token_file_is_exist


class TestBuscarPagamentoDarf(unittest.TestCase):

    def setUp(self):
        self.client_id = config("CLIENT_ID")
        self.client_secret = config("CLIENT_SECRET")
        self.cert = (
            config("SSL_DIR_BASE") + config("PUBLIC_KEY_V2"),
            config("SSL_DIR_BASE") + config("PRIVATE_KEY_V2"),
        )
        self.conta_corrente = config("X_INTER_CONTA_CORRENTE")

    @patch("http.client.HTTPSConnection")
    def test_01_busca_pagamento_darf_success(self, mock_https_connection):
        """Teste de emissão de cobrança"""
        # Mock da resposta para o token de acesso
        mock_token_response = MagicMock()
        mock_token_response.status = 200
        mock_token_response.read.return_value = b'{"access_token": "5e5b232a-381a-477d-83b5-4ac65b6a0679", "token_type": "Bearer", "expires_in": 3600, "scope": "boleto-cobranca.read boleto-cobranca.write", "expires_at": "2024-11-08 07:17:36.580932"}'

        # mock_https_connection.return_value.getresponse.return_value = mock_token_response

        # Cria um mock para a resposta
        busca_pagamento_response_bytes = b"""[{"tipoDarf": "PRETO", "valor": 47.14, "valorMulta": 0.0, "valorJuros": 0.0, "valorTotal": 47.14, "tipo": "Darf", "periodoApuracao": "2024-10-31", "dataPagamento": "2024-11-21", "referencia": "13609400849201739", "dataVencimento": "2024-11-30", "codigoReceita": "0220", "statusPagamento": "REALIZADO", "dataInclusao": "2024-11-21 15:17:58", "cnpjCpf": "90022400664", "codigoSolicitacao": "9e392015-c8a0-45c6-9dee-054f33e90ffa"}, {"tipoDarf": "PRETO", "valor": 47.14, "valorMulta": 0.0, "valorJuros": 0.0, "valorTotal": 47.14, "tipo": "Darf", "periodoApuracao": "2024-10-31", "dataPagamento": "2024-11-21", "referencia": "13609400849201739", "dataVencimento": "2024-11-30", "codigoReceita": "0220", "statusPagamento": "REALIZADO", "dataInclusao": "2024-11-21 15:19:40", "cnpjCpf": "90022400664", "codigoSolicitacao": "ea4a165c-71cc-b8aa-39db-36b9a4f4987c"}, {"tipoDarf": "PRETO", "valor": 47.14, "valorMulta": 0.0, "valorJuros": 0.0, "valorTotal": 47.14, "tipo": "Darf", "periodoApuracao": "2024-10-31", "dataPagamento": "2024-11-21", "referencia": "13609400849201739", "dataVencimento": "2024-11-30", "codigoReceita": "0220", "statusPagamento": "REALIZADO", "dataInclusao": "2024-11-21 15:21:54", "cnpjCpf": "90022400664", "codigoSolicitacao": "b3cfb393-5b50-d10f-0ba1-77cf3bd7536b"}]"""

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

        # Instancia a classe IncluiPagamentoCodBar
        busca_pagamento_darf = BuscaPagamentoDarf(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        # Chama o metodo emitir
        data_response = busca_pagamento_darf.buscar(
            {
                "codigoSolicitacao": "9e392015-c8a0-45c6-9dee-054f33e90ffa",
                "codigoReceita": "0220",
                "dataInicio": "2024-11-01",
                "dataFim": "2024-11-22",
            }
        )

        dict_response = json.loads(busca_pagamento_response_bytes)
        response = {"pagamentos": dict_response}
        busca_pagamento_response = RespostaBuscaPagamentoDarf(**response).to_dict()

        # Verifica se os dados retornados estão corretos
        self.assertEqual(data_response, busca_pagamento_response)

    @patch("http.client.HTTPSConnection")  # Mocka a classe MyHttpsClient
    def test_02_busca_pagamento_darf_failure(self, mock_https_client_class):
        """Teste de lançamento de exception"""
        mock_https_client_class = mock_https_client_class.return_value

        # Define o side_effect para simular uma exceção
        mock_https_client_class.return_value.getresponse.side_effect = Exception(
            GENERIC_EXCEPTION_MESSAGE
        )

        # Instancia a classe IncluiPagamentoCodBar
        busca_pagamento_darf = BuscaPagamentoDarf(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        # Verifica se a exceção é levantada corretamente
        with self.assertRaises(Exception) as context:
            busca_pagamento_darf.buscar(
                {
                    "dataInicio": "2024-11-01",
                    "dataFim": "2024-11-22",
                    "filtrarDataPor": "INCLUSAO",  # Enum: "INCLUSAO" "PAGAMENTO" "VENCIMENTO"
                }
            )

        self.assertEqual(str(context.exception), GENERIC_EXCEPTION_MESSAGE)

    @patch("http.client.HTTPSConnection")  # Mocka a classe MyHttpsClient
    def test_03_busca_pagamento_darf_failure(self, mock_https_client_class):
        """Teste de buscar pagamento com parametro invalido"""

        busca_pagamento_darf = BuscaPagamentoDarf(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        busca_response = busca_pagamento_darf.buscar({})

        self.assertEqual(
            busca_response,
            {
                "codigo": 501,
                "descricao": "Campo 'query_params' é requerido.",
            },
        )


if __name__ == "__main__":
    unittest.main()
