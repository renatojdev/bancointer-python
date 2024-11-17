# test_emitir_cobranca.py

import unittest
from unittest.mock import patch, MagicMock
from bancointer.cobranca_v3.cobranca import EmiteCobranca
from decouple import config

from bancointer.cobranca_v3.models.cobranca import Cobranca
from bancointer.cobranca_v3.models.desconto import Desconto
from bancointer.cobranca_v3.models.message import Message
from bancointer.cobranca_v3.models.mora import Mora
from bancointer.cobranca_v3.models.multa import Multa
from bancointer.cobranca_v3.models.pessoa import Pessoa
from bancointer.cobranca_v3.models.tipo_pessoa import PersonType
from bancointer.cobranca_v3.models.resposta_emitir_cobranca import (
    RespostaEmitirCobranca,
)
from bancointer.cobranca_v3.models.solicitacao_emitir_cobranca import (
    SolicitacaoEmitirCobranca,
)
from bancointer.utils.environment import Environment
from bancointer.utils.token_utils import token_file_is_exist

client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")
cert = (
    config("SSL_DIR_BASE") + config("PUBLIC_KEY_V2"),
    config("SSL_DIR_BASE") + config("PRIVATE_KEY_V2"),
)

pessoa_pagador = Pessoa(
    "9" * 11,  # valido
    PersonType.FISICA,
    "NOME DO PAGADOR",
    "ENDERECO DO PAGADOR",
    "CIDADE DO PAGADOR",
    "PR",
    "80030000",
)  # OU FISICA # Pagador

desconto = Desconto("PERCENTUALDATAINFORMADA", 0, 1.2, 2)
multa = Multa("VALORFIXO", 0, 100)
mora = Mora("TAXAMENSAL", 0, 4.5)
message = Message("message 1", "message 2", "message 3", "", "message 5")

# Beneficiario final, mesmo que o pagador
beneficiario_final = Pessoa(
    "12345678901",
    PersonType.FISICA,
    "Nome do beneficiário",
    "Avenida Brasil, 1200",
    "Belo Horizonte",
    "MG",
    "30110000",
)

new_cobranca = Cobranca.criar_sobranca_simples(
    "0001", 2.5, "2024-11-21", pessoa_pagador
)
new_cobranca.desconto = desconto
new_cobranca.multa = multa
new_cobranca.mora = mora
new_cobranca.mensagem = message
new_cobranca.beneficiarioFinal = beneficiario_final

sol_cobranca = SolicitacaoEmitirCobranca(new_cobranca)


class TestEmitirCobranca(unittest.TestCase):

    @patch("http.client.HTTPSConnection")
    def test_01_emite_cobranca_success(self, mock_https_connection):
        # Mock da resposta para o token de acesso
        mock_token_response = MagicMock()
        mock_token_response.status = 200
        mock_token_response.read.return_value = b'{"access_token": "5e5b232a-381a-477d-83b5-4ac65b6a0679", "token_type": "Bearer", "expires_in": 3600, "scope": "boleto-cobranca.read boleto-cobranca.write", "expires_at": "2024-11-08 07:17:36.580932"}'

        # mock_https_connection.return_value.getresponse.return_value = mock_token_response

        # Cria um mock para a resposta
        request_code = b'{"codigoSolicitacao": "183e982a-34e5-4bc0-9643-def5432a"}'

        mock_data_response = MagicMock()
        mock_data_response.status = 200
        mock_data_response.read.return_value = request_code

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

        # Instancia a classe EmiteCobranca (aqui pode ser necessário usar a classe real)
        emite_cobranca = EmiteCobranca(Environment.SANDBOX, client_id, client_secret, cert)

        # Chama o metodo emitir
        data = emite_cobranca.emitir(sol_cobranca)

        resposta = RespostaEmitirCobranca()
        resposta.codigoSolicitacao = "183e982a-34e5-4bc0-9643-def5432a"

        # Verifica se os dados retornados estão corretos
        self.assertEqual(data, resposta)

        # Verifica se o metodo emitir foi chamado com os parâmetros corretos (se necessário)
        # mock_https_connection.assert_called_once_with(HOST_SANDBOX, port=443, context=ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT))

    @patch("http.client.HTTPSConnection")  # Mocka a classe MyHttpsClient
    def test_02_emite_cobranca_failure(self, mock_https_client_class):
        # Cria uma instância do mock para MyHttpsClient
        # mock_https_client = mock_https_client_class.return_value

        # Define o side_effect para simular uma exceção
        mock_https_client_class.return_value.getresponse.side_effect = Exception(
            "Ocorreu um erro no SDK"
        )

        # Instancia a classe DataFetcher
        emite_cobranca = EmiteCobranca(Environment.SANDBOX, client_id, client_secret, cert)

        # Verifica se a exceção é levantada corretamente
        with self.assertRaises(Exception) as context:
            emite_cobranca.emitir(sol_cobranca)

        self.assertEqual(str(context.exception), "Ocorreu um erro no SDK")


if __name__ == "__main__":
    unittest.main()
