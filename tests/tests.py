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
            (config("PUBLIC_KEY"), config("PRIVATE_KEY")),
        )

    def test_get_url(self):
        self.assertEqual(
            self.bancointer._get_url("/test"), f"{self.bancointer._BASE_URL}/test"
        )

    def test_headers(self):
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
        url = self.bancointer._get_url(path="boletos/00005/pdf")
        json = None
        request_mock.get(url=url, json=json)
        download = self.bancointer.download(
            nosso_numero="00005", download_path="/tmp/downloads"
        )
        self.assertEqual(download, json)

    @requests_mock.Mocker()
    def test_baixa(self, request_mock):
        url = self.bancointer._get_url(path="boletos/00005/baixas")
        json = {}
        request_mock.post(url=url, json=json)
        drop = self.bancointer.baixa(nosso_numero="00005", motivo=Baixa.ACERTOS)
        self.assertEqual(drop, json)


if __name__ == "__main__":
    unittest.main()
