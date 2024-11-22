# test_buscar_pagamento.py


import json
import unittest
from unittest.mock import patch, MagicMock

from decouple import config

from bancointer.banking.models.resposta_busca_pagamento import RespostaBuscaPagamento
from bancointer.banking.pagamento.busca_pagamento import BuscaPagamento
from bancointer.utils.constants import GENERIC_EXCEPTION_MESSAGE
from bancointer.utils.environment import Environment
from bancointer.utils.token_utils import token_file_is_exist


class TestBuscarPagamento(unittest.TestCase):

    def setUp(self):
        self.client_id = config("CLIENT_ID")
        self.client_secret = config("CLIENT_SECRET")
        self.cert = (
            config("SSL_DIR_BASE") + config("PUBLIC_KEY_V2"),
            config("SSL_DIR_BASE") + config("PRIVATE_KEY_V2"),
        )
        self.conta_corrente = config("X_INTER_CONTA_CORRENTE")

    @patch("http.client.HTTPSConnection")
    def test_01_busca_pagamento_success(self, mock_https_connection):
        """Teste de emissão de cobrança"""
        # Mock da resposta para o token de acesso
        mock_token_response = MagicMock()
        mock_token_response.status = 200
        mock_token_response.read.return_value = b'{"access_token": "5e5b232a-381a-477d-83b5-4ac65b6a0679", "token_type": "Bearer", "expires_in": 3600, "scope": "boleto-cobranca.read boleto-cobranca.write", "expires_at": "2024-11-08 07:17:36.580932"}'

        # mock_https_connection.return_value.getresponse.return_value = mock_token_response

        # Cria um mock para a resposta
        busca_pagamento_response_bytes = b"""[{"codigoTransacao": "6ad77a34-dfb4-4efa-a8c2-40c17c5346cd", "codigoBarra": "03395988500000666539201493990000372830030102", "tipo": "Pagamento", "dataVencimentoDigitada": "2024-11-19", "dataVencimentoTitulo": "2024-10-30", "dataInclusao": "20/11/2024 14:53:22", "dataPagamento": "2024-11-20", "valorPago": 2.5, "valorNominal": 666.53, "statusPagamento": "REALIZADO", "cpfCnpjBeneficiario": "99999999999999", "nomeBeneficiario": "BENEFICIARIO_EXEMPLO", "autenticacao": "849228769277280455958065168770"}, {"codigoTransacao": "ac72024e-6961-44ff-9f3a-bbc722c869f1", "codigoBarra": "03395988500000666539201493990000372830030102", "tipo": "Pagamento", "dataVencimentoDigitada": "2024-11-19", "dataVencimentoTitulo": "2024-10-30", "dataInclusao": "20/11/2024 13:11:42", "dataPagamento": "2024-11-20", "valorPago": 2.5, "valorNominal": 666.53, "statusPagamento": "REALIZADO", "cpfCnpjBeneficiario": "99999999999999", "nomeBeneficiario": "BENEFICIARIO_EXEMPLO", "autenticacao": "835425231784764457506088907486"}, {"codigoTransacao": "32a929a3-d3b9-4954-8f84-a593719dee2a", "codigoBarra": "03395988500000666539201493990000372830030102", "tipo": "Pagamento", "dataVencimentoDigitada": "2024-11-19", "dataVencimentoTitulo": "2024-10-30", "dataInclusao": "20/11/2024 14:27:17", "dataPagamento": "2024-11-20", "valorPago": 2.5, "valorNominal": 666.53, "statusPagamento": "REALIZADO", "cpfCnpjBeneficiario": "99999999999999", "nomeBeneficiario": "BENEFICIARIO_EXEMPLO", "autenticacao": "855825524582762960337333331946"}, {"codigoTransacao": "219ca015-85d2-4877-abe2-662a50c1f289", "codigoBarra": "03395988500000666539201493990000372830030102", "tipo": "Pagamento", "dataVencimentoDigitada": "2024-11-19", "dataVencimentoTitulo": "2024-10-30", "dataInclusao": "20/11/2024 14:27:32", "dataPagamento": "2024-11-20", "valorPago": 2.5, "valorNominal": 666.53, "statusPagamento": "REALIZADO", "cpfCnpjBeneficiario": "99999999999999", "nomeBeneficiario": "BENEFICIARIO_EXEMPLO", "autenticacao": "066676799964389077325873545399"}, {"codigoTransacao": "f1448ad4-51ef-4740-b776-9a83fccccc5c", "codigoBarra": "03395988500000666539201493990000372830030102", "tipo": "Pagamento", "dataVencimentoDigitada": "2024-11-19", "dataVencimentoTitulo": "2024-10-30", "dataInclusao": "20/11/2024 14:52:48", "dataPagamento": "2024-11-20", "valorPago": 2.5, "valorNominal": 666.53, "statusPagamento": "REALIZADO", "cpfCnpjBeneficiario": "99999999999999", "nomeBeneficiario": "BENEFICIARIO_EXEMPLO", "autenticacao": "886245494635955524615330131574"}, {"codigoTransacao": "7e3ba2fb-0846-4e37-ad6d-a4d69810be7f", "codigoBarra": "03395988500000666539201493990000372830030102", "tipo": "Pagamento", "dataVencimentoDigitada": "2024-11-19", "dataVencimentoTitulo": "2024-10-30", "dataInclusao": "20/11/2024 14:54:49", "dataPagamento": "2024-11-20", "valorPago": 2.5, "valorNominal": 666.53, "statusPagamento": "REALIZADO", "cpfCnpjBeneficiario": "99999999999999", "nomeBeneficiario": "BENEFICIARIO_EXEMPLO", "autenticacao": "226957124713287577416614589048"}, {"codigoTransacao": "cefff47c-d374-471a-a56f-6bc14d924722", "codigoBarra": "03395988500000666539201493990000372830030102", "tipo": "Pagamento", "dataVencimentoDigitada": "2024-11-19", "dataVencimentoTitulo": "2024-10-30", "dataInclusao": "20/11/2024 14:55:07", "dataPagamento": "2024-11-20", "valorPago": 2.5, "valorNominal": 666.53, "statusPagamento": "REALIZADO", "cpfCnpjBeneficiario": "99999999999999", "nomeBeneficiario": "BENEFICIARIO_EXEMPLO", "autenticacao": "483528489904730374070910000263"}, {"codigoTransacao": "a85210ff-b131-4972-a138-a8feadd35444", "codigoBarra": "03395988500000666539201493990000372830030102", "tipo": "Pagamento", "dataVencimentoDigitada": "2024-11-21", "dataVencimentoTitulo": "2024-10-30", "dataInclusao": "21/11/2024 05:00:01", "dataPagamento": "2024-11-21", "valorPago": 2.5, "valorNominal": 666.53, "statusPagamento": "REALIZADO", "cpfCnpjBeneficiario": "99999999999999", "nomeBeneficiario": "BENEFICIARIO_EXEMPLO", "autenticacao": "661847960316394685487549260472"}, {"codigoTransacao": "e0e43ce2-fcfe-4ee1-8e91-0d6418176c05", "codigoBarra": "03395988500000666539201493990000372830030102", "tipo": "Pagamento", "dataVencimentoDigitada": "2024-11-21", "dataVencimentoTitulo": "2024-10-30", "dataInclusao": "21/11/2024 05:00:01", "dataPagamento": "2024-11-21", "valorPago": 2.5, "valorNominal": 666.53, "statusPagamento": "REALIZADO", "cpfCnpjBeneficiario": "99999999999999", "nomeBeneficiario": "BENEFICIARIO_EXEMPLO", "autenticacao": "344127489139139842310631291129"}, {"codigoTransacao": "bc1059eb-2777-4676-b76b-d8e26c50e73c", "codigoBarra": "03395988500000666539201493990000372830030102", "tipo": "Pagamento", "dataVencimentoDigitada": "2024-11-21", "dataVencimentoTitulo": "2024-10-30", "dataInclusao": "21/11/2024 05:00:01", "dataPagamento": "2024-11-21", "valorPago": 2.5, "valorNominal": 666.53, "statusPagamento": "REALIZADO", "cpfCnpjBeneficiario": "99999999999999", "nomeBeneficiario": "BENEFICIARIO_EXEMPLO", "autenticacao": "607606833944677458383667541583"}, {"codigoTransacao": "72324a7f-0703-431f-a85a-97794f94e360", "codigoBarra": "03395988500000666539201493990000372830030102", "tipo": "Pagamento", "dataVencimentoDigitada": "2024-11-24", "dataVencimentoTitulo": "2024-10-30", "dataInclusao": "22/11/2024 07:03:11", "dataPagamento": "2024-11-24", "valorPago": 2.5, "valorNominal": 666.53, "statusPagamento": "AGENDADO_CANCELADO", "cpfCnpjBeneficiario": "99999999999999", "nomeBeneficiario": "BENEFICIARIO_EXEMPLO", "autenticacao": "154141137136282680396096145711"}]"""

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
        busca_pagamento = BuscaPagamento(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        # Chama o metodo emitir
        data_response = busca_pagamento.buscar(
            {
                "codBarraLinhaDigitavel": "03395988500000666539201493990000372830030102",
                "codigoTransacao": "ac72024e-6961-44ff-9f3a-bbc722c869f1",
                "dataInicio": "2024-11-01",
                "dataFim": "2024-11-22",
                "filtrarDataPor": "INCLUSAO",  # Enum: "INCLUSAO" "PAGAMENTO" "VENCIMENTO"
            }
        )

        dict_response = json.loads(busca_pagamento_response_bytes)
        response = {"pagamentos": dict_response}
        busca_pagamento_response = RespostaBuscaPagamento(**response).to_dict()

        # Verifica se os dados retornados estão corretos
        self.assertEqual(data_response, busca_pagamento_response)

    @patch("http.client.HTTPSConnection")  # Mocka a classe MyHttpsClient
    def test_02_busca_pagamento_failure(self, mock_https_client_class):
        """Teste de lançamento de exception"""
        mock_https_client_class = mock_https_client_class.return_value

        # Define o side_effect para simular uma exceção
        mock_https_client_class.return_value.getresponse.side_effect = Exception(
            GENERIC_EXCEPTION_MESSAGE
        )

        # Instancia a classe IncluiPagamentoCodBar
        busca_pagamento = BuscaPagamento(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        # Verifica se a exceção é levantada corretamente
        with self.assertRaises(Exception) as context:
            busca_pagamento.buscar(
                {
                    "dataInicio": "2024-11-01",
                    "dataFim": "2024-11-22",
                    "filtrarDataPor": "INCLUSAO",  # Enum: "INCLUSAO" "PAGAMENTO" "VENCIMENTO"
                }
            )

        self.assertEqual(str(context.exception), GENERIC_EXCEPTION_MESSAGE)

    @patch("http.client.HTTPSConnection")  # Mocka a classe MyHttpsClient
    def test_03_busca_pagamento_failure(self, mock_https_client_class):
        """Teste de buscar pagamento com parametro invalido"""

        busca_pagamento = BuscaPagamento(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        busca_response = busca_pagamento.buscar({})

        self.assertEqual(
            busca_response,
            {
                "codigo": 501,
                "descricao": "Campo 'query_params' é requerido.",
            },
        )


if __name__ == "__main__":
    unittest.main()
