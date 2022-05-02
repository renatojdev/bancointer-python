import unittest
import requests_mock

from bancointer.baixa import Baixa
from bancointer.bancointer import BancoInter
from decouple import config


class TestBancoInter(unittest.TestCase):
    def setUp(self):
        self.bancointer = BancoInter(
            config("CPFCNPJ_BENEF"),
            config("X-INTER-CONTA-CORRENTE"),
            (config("PUBLIC_KEY_V1"), config("PRIVATE_KEY_V1")),
        )
        self.bancointer.set_api_version(1)
        self.bancointer.set_base_url("https://apis.bancointer.com.br/openbanking/v1/certificado/")

    def test_get_url(self):
        self.assertEqual(
            self.bancointer._get_url("/test"), f"{self.bancointer.base_url}/test"
        )

    def test_headers(self):
        if self.bancointer.api_version == 2:
            self.assertEqual(
                self.bancointer.headers,
                {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + self.bancointer.bearer_token
                }
            )
        else:
            self.assertEqual(
                self.bancointer.headers,
                {
                    "x-inter-conta-corrente": self.bancointer.inter_conta_corrente,
                },
            )

    @requests_mock.Mocker()
    def test_boleto(self, request_mock):
        url = self.bancointer._get_url(path="boletos")
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
        url = self.bancointer._get_url(path=f"boletos/00005/pdf")
        json = None
        request_mock.get(url=url, json=json)
        download = self.bancointer.download(
            nosso_numero="00005", download_path="/tmp/downloads"
        )
        self.assertEqual(download, json)

    @requests_mock.Mocker()
    def test_baixa(self, request_mock):
        path = f"boletos/00005/baixas"
        if self.bancointer.api_version == 2: path = f"boletos/00005/cancelar"
        url = self.bancointer._get_url(path=path)
        json = {}
        request_mock.post(url=url, json=json)
        drop = self.bancointer.baixa(nosso_numero="00005", motivo=Baixa.ACERTOS)
        self.assertEqual(drop, json)

    @requests_mock.Mocker()
    def test_consulta(self, request_mock):
        url = self.bancointer._get_url(path=f"boletos/000007")
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
        consulta = self.bancointer.consulta(nosso_numero="000007")
        self.assertEqual(consulta, json)
        self.assertEqual(consulta["situacao"], "PAGO")


if __name__ == "__main__":
    unittest.main()
