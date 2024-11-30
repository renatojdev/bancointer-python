# test_consultar_cobranca_imediata.py


import json
import unittest
from unittest.mock import patch, MagicMock

from decouple import config

from bancointer.pix.cob.consulta_cobranca_imediata import ConsultaCobrancaImediata
from bancointer.pix.models.resposta_solicitacao_cobranca import (
    RespostaSolicitacaoCobranca,
)
from bancointer.utils.environment import Environment
from bancointer.utils.token_utils import token_file_is_exist


class TestConsultarCobrancaImediata(unittest.TestCase):

    def setUp(self):
        self.client_id = config("CLIENT_ID")
        self.client_secret = config("CLIENT_SECRET")
        self.cert = (
            config("SSL_DIR_BASE") + config("PUBLIC_KEY_V2"),
            config("SSL_DIR_BASE") + config("PRIVATE_KEY_V2"),
        )
        self.conta_corrente = config("X_INTER_CONTA_CORRENTE")

    @patch("http.client.HTTPSConnection")
    def test_01_consultar_cobranca_imediata_success(self, mock_https_connection):
        """Teste de emissão de cobrança"""
        # Mock da resposta para o token de acesso
        mock_token_response = MagicMock()
        mock_token_response.status = 200
        mock_token_response.read.return_value = b'{"access_token": "5e5b232a-381a-477d-83b5-4ac65b6a0679", "token_type": "Bearer", "expires_in": 3600, "scope": "boleto-cobranca.read boleto-cobranca.write", "expires_at": "2024-11-08 07:17:36.580932"}'

        # Cria um mock para a resposta
        cob_imediata_response_bytes = b"""{
                              "calendario": {
                                "criacao": "2020-09-09T20:15:00.358Z",
                                "expiracao": 3600
                              },
                              "txid": "655dfdb1a4514b8fbb58254b958913fb",
                              "revisao": 1,
                              "loc": {
                                "id": 567,
                                "location": "pix.example.com/qr/1dd7f893a58e417287028dc33e21a403"
                              },
                              "location": "pix.example.com/qr/1dd7f893a58e417287028dc33e21a403",
                              "status": "CONCLUIDA",
                              "devedor": {
                                "cnpj": "12345678000195",
                                "nome": "Empresa de Servicos SA"
                              },
                              "valor": {
                                "original": "100.00",
                                "modalidadeAlteracao": 0
                              },
                              "chave": "40a0932d-1918-4eee-845d-35a2da1690dc",
                              "solicitacaoPagador": "Informar cartao fidelidade",
                              "pix": [
                                {
                                  "endToEndId": "E12345678202009091221kkkkkkkkkkk",
                                  "txid": "655dfdb1a4514b8fbb58254b958913fb",
                                  "valor": "110.00",
                                  "horario": "2020-09-09T20:15:00.358Z",
                                  "infoPagador": "0123456789",
                                  "devolucoes": [
                                    {
                                      "id": "123ABC",
                                      "rtrId": "Dxxxxxxxx202009091221kkkkkkkkkkk",
                                      "valor": "10.00",
                                      "horario": {
                                        "solicitacao": "2020-09-09T20:15:00.358Z"
                                      },
                                      "status": "EM_PROCESSAMENTO"
                                    }
                                  ]
                                }
                              ]
                            }"""

        mock_data_response = MagicMock()
        mock_data_response.status = 200
        mock_data_response.read.return_value = cob_imediata_response_bytes

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
        consulta_cob_imediata = ConsultaCobrancaImediata(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        # Chama o metodo emitir
        data = consulta_cob_imediata.consultar("655dfdb1a4514b8fbb58254b958913fb")

        payment_response = RespostaSolicitacaoCobranca(
            **json.loads(cob_imediata_response_bytes)
        ).to_dict()

        # Verifica se os dados retornados estão corretos
        self.assertEqual(data, payment_response)

    @patch("http.client.HTTPSConnection")  # Mocka a classe MyHttpsClient
    def test_02_consultar_cobranca_imediata_failure(self, mock_https_client_class):
        """Teste de consulta de cobranca imediata com txid inválido"""

        consulta_cobranca = ConsultaCobrancaImediata(
            Environment.SANDBOX,
            self.client_id,
            self.client_secret,
            self.cert,
            self.conta_corrente,
        )

        response = consulta_cobranca.consultar("txidInvalid")

        self.assertEqual(
            response, {"codigo": 502, "descricao": "Campo 'txid' é inválido."}
        )


if __name__ == "__main__":
    unittest.main()
