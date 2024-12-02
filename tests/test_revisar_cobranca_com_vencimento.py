# test_revisar_cobranca_com_vencimento.py


import json
import unittest
from unittest.mock import MagicMock, patch

from decouple import config

from bancointer.pix.cobv.revisa_cobranca_com_vencimento import (
    RevisaCobrancaComVencimento,
)
from bancointer.pix.models.resposta_solicitacao_cobranca import (
    RespostaSolicitacaoCobranca,
)
from bancointer.pix.models.solicitacao_cobranca import (
    SolicitacaoCobranca,
)
from bancointer.utils.constants import GENERIC_EXCEPTION_MESSAGE
from bancointer.utils.environment import Environment
from bancointer.utils.token_utils import token_file_is_exist


class TestRevisarCobrancaComVencimento(unittest.TestCase):

    def setUp(self):
        self.client_id = config("CLIENT_ID")
        self.client_secret = config("CLIENT_SECRET")
        self.cert = (
            config("SSL_DIR_BASE") + config("PUBLIC_KEY_V2"),
            config("SSL_DIR_BASE") + config("PRIVATE_KEY_V2"),
        )
        self.conta_corrente = config("X_INTER_CONTA_CORRENTE")
        self.cobv_com_vencimento_request_bytes = b"""{
                                                "calendario": {
                                                    "criacao": "2020-09-09T20:15:00.358Z",
                                                    "dataDeVencimento": "2020-12-31",
                                                    "validadeAposVencimento": 30
                                                  },
                                                  "valor": {
                                                    "original": "567.89"
                                                  },
                                                  "chave": "a1f4102e-a446-4a57-bcce-6fa48899c1d1",
                                                  "solicitacaoPagador": "Informar cartao fidelidade"
                                                }"""

    @patch("http.client.HTTPSConnection")
    def test_01_revisar_cobranca_com_vencimento_success(self, mock_https_connection):
        """Teste de emissão de cobrança"""
        # Mock da resposta para o token de acesso
        mock_token_response = MagicMock()
        mock_token_response.status = 200
        mock_token_response.read.return_value = b'{"access_token": "5e5b232a-381a-477d-83b5-4ac65b6a0679", "token_type": "Bearer", "expires_in": 3600, "scope": "boleto-cobranca.read boleto-cobranca.write", "expires_at": "2024-11-08 07:17:36.580932"}'

        # mock_https_connection.return_value.getresponse.return_value = mock_token_response

        # Cria um mock para a resposta
        cobv_venc_response_bytes = b"""{
                                  "calendario": {
                                    "criacao": "2020-09-09T20:15:00.358Z",
                                    "dataDeVencimento": "2020-12-31",
                                    "validadeAposVencimento": 30
                                  },
                                  "txid": "7978c0c97ea847e78e8849634473c1f1",
                                  "revisao": 0,
                                  "loc": {
                                    "id": 789,
                                    "location": "pix.example.com/qr/v2/cobv/9d36b84fc70b478fb95c12729b90ca25",
                                    "tipoCob": "cobv"
                                  },
                                  "status": "ATIVA",
                                  "devedor": {
                                    "logradouro": "Rua 15, Numero 1, Bairro Luz",
                                    "cidade": "Belo Horizonte",
                                    "uf": "MG",
                                    "cep": "99000750",
                                    "cnpj": "12345678000195",
                                    "nome": "Empresa de Servicos SA"
                                  },
                                  "recebedor": {
                                    "logradouro": "Rua 15 Numero 1200, Bairro Sao Luiz",
                                    "cidade": "Sao Paulo",
                                    "uf": "SP",
                                    "cep": "70800100",
                                    "cnpj": "56989000019533",
                                    "nome": "Empresa de Logistica SA"
                                  },
                                  "valor": {
                                    "original": "567.89"
                                  },
                                  "chave": "a1f4102e-a446-4a57-bcce-6fa48899c1d1",
                                  "solicitacaoPagador": "Informar cartao fidelidade"
                                }"""

        mock_data_response = MagicMock()
        mock_data_response.status = 200
        mock_data_response.read.return_value = cobv_venc_response_bytes

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

        # Instancia a classe RevisaCobrancaComVencimento
        cria_cobv_com_vencimento = RevisaCobrancaComVencimento(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        # Chama o metodo criar cobrança com vencimento
        data = cria_cobv_com_vencimento.revisar(
            SolicitacaoCobranca(**json.loads(self.cobv_com_vencimento_request_bytes)),
            "7978c0c97ea847e78e8849634473c1f1",
        )

        payment_response = RespostaSolicitacaoCobranca(
            **json.loads(cobv_venc_response_bytes)
        ).to_dict()

        # Verifica se os dados retornados estão corretos
        self.assertEqual(data, payment_response)

    @patch("http.client.HTTPSConnection")
    def test_02_revisar_cobranca_com_vencimento_txid_success(
        self, mock_https_connection
    ):
        """Teste de emissão de cobrança"""
        # Mock da resposta para o token de acesso
        mock_token_response = MagicMock()
        mock_token_response.status = 200
        mock_token_response.read.return_value = b'{"access_token": "5e5b232a-381a-477d-83b5-4ac65b6a0679", "token_type": "Bearer", "expires_in": 3600, "scope": "boleto-cobranca.read boleto-cobranca.write", "expires_at": "2024-11-08 07:17:36.580932"}'

        # mock_https_connection.return_value.getresponse.return_value = mock_token_response

        # Cria um mock para a resposta
        cobv_venc_response_bytes = b"""{
          "calendario": {
            "criacao": "2020-09-09T20:15:00.358Z",
            "dataDeVencimento": "2020-12-31",
            "validadeAposVencimento": 30
          },
          "txid": "7978c0c97ea847e78e8849634473c1f1",
          "revisao": 0,
          "loc": {
            "id": 789,
            "location": "pix.example.com/qr/v2/cobv/9d36b84fc70b478fb95c12729b90ca25",
            "tipoCob": "cobv"
          },
          "status": "ATIVA",
          "devedor": {
            "logradouro": "Rua 15, Numero 1, Bairro Luz",
            "cidade": "Belo Horizonte",
            "uf": "MG",
            "cep": "99000750",
            "cnpj": "12345678000195",
            "nome": "Empresa de Servicos SA"
          },
          "recebedor": {
            "logradouro": "Rua 15 Numero 1200, Bairro Sao Luiz",
            "cidade": "Sao Paulo",
            "uf": "SP",
            "cep": "70800100",
            "cnpj": "56989000019533",
            "nome": "Empresa de Logistica SA"
          },
          "valor": {
            "original": "567.89"
          },
          "chave": "a1f4102e-a446-4a57-bcce-6fa48899c1d1",
          "solicitacaoPagador": "Informar cartao fidelidade"
        }"""

        mock_data_response = MagicMock()
        mock_data_response.status = 200
        mock_data_response.read.return_value = cobv_venc_response_bytes

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

        # Instancia a classe CriaCobrancaComVencimento
        cria_cobv_com_vencimento = RevisaCobrancaComVencimento(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        # Chama o metodo criar cobranca imediata com txid
        data = cria_cobv_com_vencimento.revisar(
            SolicitacaoCobranca(**json.loads(self.cobv_com_vencimento_request_bytes)),
            "7978c0c97ea847e78e8849634473c1f1",
        )

        payment_response = RespostaSolicitacaoCobranca(
            **json.loads(cobv_venc_response_bytes)
        ).to_dict()

        # Verifica se os dados retornados estão corretos
        self.assertEqual(data, payment_response)

    @patch("http.client.HTTPSConnection")  # Mocka a classe MyHttpsClient
    def test_03_revisar_cobranca_com_vencimento_txid_failure(
        self, mock_https_client_class
    ):
        """Teste de lançamento de exception"""
        mock_https_client_class = mock_https_client_class.return_value

        # Define o side_effect para simular uma exceção
        mock_https_client_class.return_value.getresponse.side_effect = Exception(
            GENERIC_EXCEPTION_MESSAGE
        )

        # Instancia a classe RevisaCobrancaComVencimento
        cria_cobv_com_vencimento = RevisaCobrancaComVencimento(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        # Verifica se a exceção é levantada corretamente
        response = cria_cobv_com_vencimento.revisar(
            SolicitacaoCobranca(**json.loads(self.cobv_com_vencimento_request_bytes)),
            "txid_invalid",
        )

        self.assertEqual(
            response, {"codigo": 502, "descricao": "Campo 'txid' é inválido."}
        )

    @patch("http.client.HTTPSConnection")  # Mocka a classe MyHttpsClient
    def test_04_revisar_cobranca_com_vencimento_failure(self, mock_https_client_class):
        """Teste de lançamento de exception"""
        mock_https_client_class = mock_https_client_class.return_value

        # Define o side_effect para simular uma exceção
        mock_https_client_class.return_value.getresponse.side_effect = Exception(
            GENERIC_EXCEPTION_MESSAGE
        )

        # Instancia a classe RevisaCobrancaComVencimento
        cria_cobv_com_vencimento = RevisaCobrancaComVencimento(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        # Verifica se a exceção é levantada corretamente
        with self.assertRaises(Exception) as context:
            cria_cobv_com_vencimento.revisar(
                SolicitacaoCobranca(
                    **json.loads(self.cobv_com_vencimento_request_bytes)
                ),
                "",
            )

        self.assertEqual(str(context.exception), GENERIC_EXCEPTION_MESSAGE)

    @patch("http.client.HTTPSConnection")  # Mocka a classe MyHttpsClient
    def test_05_revisar_cobranca_com_vencimento_chave_failure(
        self, mock_https_client_class
    ):
        """Teste de lançamento de exception"""
        # Instancia a classe RevisaCobrancaComVencimento
        cria_cobv_com_vencimento = RevisaCobrancaComVencimento(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        # required
        cob_imediata_request = json.loads(self.cobv_com_vencimento_request_bytes)
        cob_imediata_request["chave"] = ""

        # Verifica se a exceção é levantada corretamente
        response = cria_cobv_com_vencimento.revisar(
            SolicitacaoCobranca(**cob_imediata_request), ""
        )

        self.assertEqual(
            response,
            {
                "codigo": 404,
                "descricao": "O atributo 'solicitacaoCobrancaImediata.chave' é obrigatório.",
            },
        )

        # invalid
        cob_imediata_request["chave"] = "xpto"

        response = cria_cobv_com_vencimento.revisar(
            SolicitacaoCobranca(**cob_imediata_request), ""
        )

        self.assertEqual(
            response,
            {
                "codigo": 502,
                "descricao": "O atributo 'solicitacaoCobrancaImediata.chave' é inválido.",
            },
        )


if __name__ == "__main__":
    unittest.main()
