import unittest
import requests_mock

from bancointer.baixa import Baixa
from bancointer.bancointer import BancoInter
from decouple import config


class TestBancoInter(unittest.TestCase):
    """Use sandbox API for test purposes"""

    def setUp(self):
        self.bancointer = BancoInter(
            config("API_SBX_COBRA_V3"),
            config("API_SBX_TOKEN_V2"),
            config("CLIENT_ID"),
            config("CLIENT_SECRET"),
            (
                config("SSL_DIR_BASE") + config("PUBLIC_KEY_V2"),
                config("SSL_DIR_BASE") + config("PRIVATE_KEY_V2"),
            ),
        )

    def test_get_url(self):
        self.assertEqual(
            self.bancointer._get_url("/test"), f"{self.bancointer.base_url}/test"
        )

    def test_headers(self):
        if self.bancointer.api_version == 3:
            self.assertEqual(
                self.bancointer.util.headers,
                {
                    "Content-Type": "application/json",
                    # "Authorization": "Bearer " + self.bancointer.util.bearer_token,
                },
            )
        else:
            self.assertEqual(
                self.bancointer.util.headers,
                {
                    "x-inter-conta-corrente": self.bancointer.util.inter_conta_corrente,
                },
            )

    @requests_mock.Mocker()
    def test_boleto(self, request_mock):
        request_mock.post(
            config("API_SBX_TOKEN_V2"),
            json={
                "access_token": "fbe564fe-4c77-4998-ae4a-b945a0d131cc",
                "token_type": "Bearer",
                "expires_in": 3600,
                "scope": "boleto-cobranca.read boleto-cobranca.write",
                "expires_at": "2024-11-08 07:17:36.580932",
            },
        )
        url = self.bancointer._get_url(path="cobrancas")
        json = {
            "seuNumero": "00005",
            "nossoNumero": "00713491373",
            "codigoBarras": "07798872200000009000001112051011300713491373",
            "linhaDigitavel": "07790001161205101130707134913735887220000000900",
        }

        request_mock.post(url=url, json=json)
        boleto = self.bancointer.boleto(
            pagador={
                "cnpjCpf": "99999999999",  # valido
                "nome": "NOME DO PAGADOR",
                "email": "email@pagador.com",
                "telefone": "999999999",
                "cep": "99999999",
                "numero": "9999",
                "complemento": "",
                "bairro": "BAIRRO DO PAGADOR",
                "endereco": "ENDERECO DO PAGADOR",
                "cidade": "CURITIBA",
                "uf": "PR",
                "ddd": "99",
                "tipoPessoa": "JURIDICA",  # OU FISICA
            },
            mensagem={
                "linha1": "linha1",
                "linha2": "linha2",
                "linha3": "linha3",
                "linha4": "linha4",
                "linha5": "linha5",
            },
            dataEmissao="2021-08-24",
            dataVencimento="2021-08-30",
            seuNumero="00005",
            valorNominal=9,
        )

        self.assertEqual(boleto, json)

    @requests_mock.Mocker()
    def test_download(self, request_mock):
        request_mock.post(
            config("API_SBX_TOKEN_V2"),
            json={
                "access_token": "fbe564fe-4c77-4998-ae4a-b945a0d131cc",
                "token_type": "Bearer",
                "expires_in": 3600,
                "scope": "boleto-cobranca.read boleto-cobranca.write",
                "expires_at": "2024-11-08 07:17:36.580932",
            },
        )
        url = self.bancointer._get_url(path=f"cobrancas/00005/pdf")
        json = None
        request_mock.get(url=url, json=json)
        download = self.bancointer.download(
            codigo_solicitacao="00005", download_path="./docs"
        )
        self.assertEqual(download, json)

    @requests_mock.Mocker()
    def test_baixa(self, request_mock):
        request_mock.post(
            "https://cdpj-sandbox.partners.uatinter.co/oauth/v2/token",
            json={
                "access_token": "fbe564fe-4c77-4998-ae4a-b945a0d131cc",
                "token_type": "Bearer",
                "expires_in": 3600,
                "scope": "boleto-cobranca.read boleto-cobranca.write",
                "expires_at": "2024-11-08 07:17:36.580932",
            },
        )
        path = f"cobrancas/00005/baixas"
        if self.bancointer.api_version == 3:
            path = f"cobrancas/00005/cancelar"
        url = self.bancointer._get_url(path=path)
        json = {}
        request_mock.post(url=url, json=json)
        drop = self.bancointer.baixa(
            codigo_solicitacao="00005", motivo_cancelamento=Baixa.ACERTOS
        )
        self.assertEqual(drop, json)

    @requests_mock.Mocker()
    def test_consulta(self, request_mock):
        url = self.bancointer._get_url(path=f"cobrancas/000007")
        json = {
            "nomeBeneficiario": "BANCO INTER",
            "cnpjCpfBeneficiario": "00000000000000",
            "tipoPessoaBeneficiario": "JURIDICA",
            "dataHoraSituacao": "01/01/2020 00:00",
            "codigoBarras": "00000000000000000000000000000000000000000000",
            "linhaDigitavel": "00000000000000000000000000000000000000000000000",
            "dataVencimento": "30/01/2020",
            "dataEmissao": "01/01/2020",
            "descricao": "",
            "seuNumero": "0000",
            "valorNominal": 10,
            "nomePagador": "Nome do Pagador",
            "emailPagador": "pagador@email.com.br",
            "dddPagador": "00",
            "telefonePagador": "900000000",
            "tipoPessoaPagador": "FISICA",
            "cnpjCpfPagador": "00000000000",
            "codigoEspecie": "OUTROS",
            "dataLimitePagamento": "01/03/2020",
            "valorAbatimento": 0,
            "situacaoPagamento": "BAIXADO",
            "situacao": "PAGO",
            "valorTotalRecebimento": 10,
            "mensagem": {
                "linha1": "mensagem na linha 1",
                "linha2": "mensagem na linha 2",
                "linha3": "mensagem na linha 3",
                "linha4": "mensagem na linha 4",
                "linha5": "mensagem na linha 5",
            },
            "desconto1": {"codigo": "NAOTEMDESCONTO", "taxa": 0, "valor": 0},
            "desconto2": {"codigo": "NAOTEMDESCONTO", "taxa": 0, "valor": 0},
            "desconto3": {"codigo": "NAOTEMDESCONTO", "taxa": 0, "valor": 0},
            "multa": {"codigo": "NAOTEMMULTA", "taxa": 0, "valor": 0},
            "mora": {"codigo": "ISENTO", "taxa": 0, "valor": 0},
        }
        request_mock.get(url=url, json=json)
        consulta = self.bancointer.consulta(codigo_solicitacao="000007")
        self.assertEqual(consulta, json)
        self.assertEqual(consulta["situacao"], "PAGO")


if __name__ == "__main__":
    unittest.main()
