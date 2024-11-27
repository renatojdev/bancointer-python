# test_incluir_pagamento_pix.py


import json
import unittest
from unittest.mock import MagicMock, patch

from decouple import config

from bancointer.banking.models.destinatario_pagamento_pix import (
    DestinatarioPagamentoPix,
)
from bancointer.banking.models.instituicao_financeira import InstituicaoFinanceira
from bancointer.banking.models.requisicao_pagamento_pix import RequisicaoPagamentoPix
from bancointer.banking.models.resposta_requisicao_pagamento_pix import (
    RespostaRequisicaoPagamentoPix,
)
from bancointer.banking.models.tipo_conta import TipoConta
from bancointer.banking.models.tipo_destinatario_pagamento_pix import (
    TipoDestinatarioPagamentoPix,
)
from bancointer.banking.pix_pagamento.inclui_pagamento_pix import IncluiPagamentoPix
from bancointer.utils.environment import Environment
from bancointer.utils.token_utils import token_file_is_exist


class TestIncluirPagamentoPix(unittest.TestCase):

    def setUp(self):
        self.client_id = config("CLIENT_ID")
        self.client_secret = config("CLIENT_SECRET")
        self.cert = (
            config("SSL_DIR_BASE") + config("PUBLIC_KEY_V2"),
            config("SSL_DIR_BASE") + config("PRIVATE_KEY_V2"),
        )
        self.conta_corrente = config("X_INTER_CONTA_CORRENTE")
        self.payment_pix_request = b"""{"valor": 46.17, "destinatario": {"tipo": "CHAVE", "chave": "+5541943339900"}}"""

    @patch("http.client.HTTPSConnection")
    def test_01_inclui_pagamento_pix_success(self, mock_https_connection):
        """Teste de inclusão de pagamento PIX"""
        # Mock da resposta para o token de acesso
        mock_token_response = MagicMock()
        mock_token_response.status = 200
        mock_token_response.read.return_value = b'{"access_token": "5e5b232a-381a-477d-83b5-4ac65b6a0679", "token_type": "Bearer", "expires_in": 3600, "scope": "boleto-cobranca.read boleto-cobranca.write", "expires_at": "2024-11-08 07:17:36.580932"}'

        # mock_https_connection.return_value.getresponse.return_value = mock_token_response

        # Cria um mock para a resposta
        payment_response_bytes = b"""{"tipoRetorno": "PROCESSADO", "codigoSolicitacao": "7c2efdec-fd68-b916-14ad-4917d4addda8", "dataPagamento": "2024-11-24", "dataOperacao": "2024-11-24"}"""

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

        # Instancia a classe IncluiPagamentoCodBar
        inclui_pagamento = IncluiPagamentoPix(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
            "x-id",
        )

        # Chama o metodo emitir
        req_pix_pay = RequisicaoPagamentoPix(**json.loads(self.payment_pix_request))
        req_pix_pay.destinatario = DestinatarioPagamentoPix(
            TipoDestinatarioPagamentoPix.CHAVE, chave="+5541943339900"
        )
        data = inclui_pagamento.incluir(req_pix_pay)

        payment_response = RespostaRequisicaoPagamentoPix(
            **json.loads(payment_response_bytes)
        )

        # Verifica se os dados retornados estão corretos
        self.assertEqual(data, payment_response.to_dict())

    @patch("http.client.HTTPSConnection")
    def test_02_inclui_pagamento_pix_success(self, mock_https_connection):
        """Teste de inclusão de pagamento PIX"""
        # Mock da resposta para o token de acesso
        mock_token_response = MagicMock()
        mock_token_response.status = 200
        mock_token_response.read.return_value = b'{"access_token": "5e5b232a-381a-477d-83b5-4ac65b6a0679", "token_type": "Bearer", "expires_in": 3600, "scope": "boleto-cobranca.read boleto-cobranca.write", "expires_at": "2024-11-08 07:17:36.580932"}'

        # mock_https_connection.return_value.getresponse.return_value = mock_token_response

        # Cria um mock para a resposta
        payment_response_bytes = b"""{"tipoRetorno": "PROCESSADO", "codigoSolicitacao": "7c2efdec-fd68-b916-14ad-4917d4addda8", "dataPagamento": "2024-11-24", "dataOperacao": "2024-11-24"}"""

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

        # Instancia a classe IncluiPagamentoCodBar
        inclui_pagamento = IncluiPagamentoPix(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
            "x-id",
        )

        # Chama o metodo emitir
        req_pix_pay = RequisicaoPagamentoPix(**json.loads(self.payment_pix_request))
        req_pix_pay.destinatario = DestinatarioPagamentoPix(
            TipoDestinatarioPagamentoPix.DADOS_BANCARIOS,
            cpfCnpj="43214321321",
            contaCorrente="321",
            agencia="0001",
            tipoConta=TipoConta.CONTA_POUPANCA,
            nome="Nome da Pessoa",
            instituicaoFinanceira=InstituicaoFinanceira("23132190"),
        )
        data = inclui_pagamento.incluir(req_pix_pay)

        payment_response = RespostaRequisicaoPagamentoPix(
            **json.loads(payment_response_bytes)
        )

        # Verifica se os dados retornados estão corretos
        self.assertEqual(data, payment_response.to_dict())

    @patch("http.client.HTTPSConnection")
    def test_03_inclui_pagamento_pix_failure(self, mock_https_connection):
        """Teste de inclusão de pagamento PIX"""
        # Instancia a classe IncluiPagamentoPix
        inclui_pagamento = IncluiPagamentoPix(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
            "x-id",
        )

        # Chama o metodo emitir
        req_pix_pay = RequisicaoPagamentoPix(**json.loads(self.payment_pix_request))
        req_pix_pay.destinatario = DestinatarioPagamentoPix(
            TipoDestinatarioPagamentoPix.DADOS_BANCARIOS,
            cpfCnpj="3214321321",
            contaCorrente="321",
            agencia="0001",
            tipoConta=TipoConta.CONTA_POUPANCA,
            nome="Nome da Pessoa",
            instituicaoFinanceira=InstituicaoFinanceira("31223122"),
        )
        data = inclui_pagamento.incluir(req_pix_pay)

        # Verifica se os dados retornados estão corretos
        self.assertEqual(
            data,
            {
                "codigo": 502,
                "descricao": "O atributo 'destinatarioPagamentoPix.cpfCnpj' é inválido.",
            },
        )

    @patch("http.client.HTTPSConnection")
    def test_04_inclui_pagamento_pix_failure(self, mock_https_connection):
        """Teste de inclusão de pagamento PIX"""
        # Instancia a classe IncluiPagamentoPix
        inclui_pagamento = IncluiPagamentoPix(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
            "x-id",
        )

        # Chama o metodo emitir
        req_pix_pay = RequisicaoPagamentoPix(**json.loads(self.payment_pix_request))
        req_pix_pay.destinatario = DestinatarioPagamentoPix(
            TipoDestinatarioPagamentoPix.DADOS_BANCARIOS,
            cpfCnpj="43214321321",
            contaCorrente="321",
            agencia="0001",
            tipoConta=TipoConta.CONTA_POUPANCA,
            nome="Nome da Pessoa",
            instituicaoFinanceira=InstituicaoFinanceira("3122"),
        )
        data = inclui_pagamento.incluir(req_pix_pay)

        # Verifica se os dados retornados estão corretos
        self.assertEqual(
            data,
            {
                "codigo": 502,
                "descricao": "O atributo 'destinatarioPagamentoPix.instituicaoFinanceira.ispb' é inválido.",
            },
        )


if __name__ == "__main__":
    unittest.main()
