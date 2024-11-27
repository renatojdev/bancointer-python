# test_consultar_pagamento_pix.py


import json
import unittest
from unittest.mock import MagicMock, patch

from decouple import config

from bancointer.banking.models.resposta_consulta_pagamento_pix import (
    RespostaConsultaPagamentoPix,
)
from bancointer.banking.pix_pagamento.consulta_pagamento_pix import ConsultaPagamentoPix
from bancointer.utils.constants import GENERIC_EXCEPTION_MESSAGE
from bancointer.utils.environment import Environment
from bancointer.utils.token_utils import token_file_is_exist


class TestConsultarPagamentoPix(unittest.TestCase):

    def setUp(self):
        self.client_id = config("CLIENT_ID")
        self.client_secret = config("CLIENT_SECRET")
        self.cert = (
            config("SSL_DIR_BASE") + config("PUBLIC_KEY_V2"),
            config("SSL_DIR_BASE") + config("PRIVATE_KEY_V2"),
        )
        self.conta_corrente = config("X_INTER_CONTA_CORRENTE")

    @patch("http.client.HTTPSConnection")
    def test_consultar_pagamento_pix_success(self, mock_https_connection):
        # Mock da resposta para o token de acesso
        mock_token_response = MagicMock()
        mock_token_response.read.return_value = b'{"access_token": "5e5b232a-381a-477d-83b5-4ac65b6a0679", "token_type": "Bearer", "expires_in": 3600, "scope": "boleto-cobranca.read boleto-cobranca.write", "expires_at": "2024-11-08 07:17:36.580932"}'
        mock_token_response.status = 200

        mock_https_connection.return_value.getresponse.return_value = (
            mock_token_response
        )

        # Cria um mock para a resposta
        response_json = b"""{"transacaoPix": {"contaCorrente": "33641836", "recebedor": {}, "erros": [], "endToEnd": "ycBfckBuoeNi2vTb6mrpCYZtBBUZ6g79", "valor": 46.17, "status": "PAGO", "dataHoraMovimento": "2024-11-27T17:17:20.249Z", "dataHoraSolicitacao": "2024-11-27T17:17:20.249Z", "chave": "+5541943339900", "codigoSolicitacao": "ad930c2f-3d68-927e-23f4-98fe41de18fe"}, "historico": [{"status": "TRANSACAO_CRIADA", "dataHoraEvento": "2024-11-27T17:17:20.249Z"}, {"status": "TRANSACAO_APROVADA", "dataHoraEvento": "2024-11-27T17:17:20.249Z"}, {"status": "PIX_ENVIADO", "dataHoraEvento": "2024-11-27T17:17:20.249Z"}, {"status": "PIX_PAGO", "dataHoraEvento": "2024-11-27T17:17:20.249Z"}]}"""

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

        consulta_pagamento_pix = ConsultaPagamentoPix(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        data = consulta_pagamento_pix.consultar("4a30390a-9242-4740-bd30-d941d3678a38")

        resposta = RespostaConsultaPagamentoPix(**json.loads(response_json))

        self.assertEqual(data["transacaoPix"], resposta.transacaoPix)
        self.assertEqual(data["historico"], resposta.historico)

    @patch("http.client.HTTPSConnection")  # Mocka a classe MyHttpsClient
    def test_02_consultar_pagamento_pix_failure(self, mock_https_client_class):
        """Teste de lançamento de exception"""
        mock_https_client_class = mock_https_client_class.return_value

        # Define o side_effect para simular uma exceção
        mock_https_client_class.return_value.getresponse.side_effect = Exception(
            GENERIC_EXCEPTION_MESSAGE
        )

        # Instancia a classe IncluiPagamentoDarf
        consulta_pagamento_pix = ConsultaPagamentoPix(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        # Verifica se a exceção é levantada corretamente
        response = consulta_pagamento_pix.consultar("")

        self.assertEqual(
            response,
            {"codigo": 404, "descricao": "Campo 'codigo_solicitacao' é requerido.'"},
        )

    @patch("http.client.HTTPSConnection")  # Mocka a classe MyHttpsClient
    def test_03_consultar_pagamento_pix_failure(self, mock_https_client_class):
        """Teste de lançamento de exception"""
        mock_https_client_class = mock_https_client_class.return_value

        # Define o side_effect para simular uma exceção
        mock_https_client_class.return_value.getresponse.side_effect = Exception(
            GENERIC_EXCEPTION_MESSAGE
        )

        # Instancia a classe IncluiPagamentoDarf
        consulta_pagamento_pix = ConsultaPagamentoPix(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        # Verifica se a exceção é levantada corretamente
        response = consulta_pagamento_pix.consultar("x")

        self.assertEqual(
            response,
            {"codigo": 502, "descricao": "Campo 'codigo_solicitacao' é inválido.'"},
        )


if __name__ == "__main__":
    unittest.main()
