# test_requisicao_pagamento.py


import json
import unittest

from bancointer.banking.models.requisicao_pagamento import RequisicaoPagamento
from bancointer.utils.exceptions import BancoInterException

PAYMENT_REQUEST = b"""{
                      "codBarraLinhaDigitavel": "07797000000000000004501008460019310001802680",
                      "valorPagar": 26.80,
                      "dataPagamento": "2023-08-18",
                      "dataVencimento": "2021-07-27",
                      "cpfCnpjBeneficiario": "12345678912345"
                    }"""


class TestRequisicaoPagamento(unittest.TestCase):

    def setUp(self):
        """Cobranca object for test purposes."""
        self.payment_request = RequisicaoPagamento(**json.loads(PAYMENT_REQUEST))

    def test_to_dict(self):
        dict_cobra = self.payment_request.to_dict()
        # Using Assertions to Check Keys
        self.assertIn("codBarraLinhaDigitavel", dict_cobra)
        self.assertIn("valorPagar", dict_cobra)
        self.assertIn("dataPagamento", dict_cobra)
        self.assertIn("dataVencimento", dict_cobra)
        self.assertIn("cpfCnpjBeneficiario", dict_cobra)
        # Using Assertions to Check Values
        self.assertEqual(
            dict_cobra["codBarraLinhaDigitavel"],
            "07797000000000000004501008460019310001802680",
        )
        self.assertEqual(dict_cobra["valorPagar"], 26.80)
        self.assertEqual(dict_cobra["dataPagamento"], "2023-08-18")
        self.assertEqual(dict_cobra["dataVencimento"], "2021-07-27")
        self.assertEqual(dict_cobra["cpfCnpjBeneficiario"], "12345678912345")

    def test_to_dict_failures(self):
        # codBarraLinhaDigitavel required
        self.payment_request.codBarraLinhaDigitavel = None
        with self.assertRaises(BancoInterException) as contexto:
            self.payment_request.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'requisicaoPagamento.codBarraLinhaDigitavel' é obrigatório.",
        )
        # valorPagar required
        self.payment_request.codBarraLinhaDigitavel = (
            "07797000000000000004501008460019310001802680"
        )
        self.payment_request.valorPagar = None
        with self.assertRaises(BancoInterException) as contexto:
            self.payment_request.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'requisicaoPagamento.valorPagar' é obrigatório.",
        )
        # dataVencimento required
        self.payment_request.codBarraLinhaDigitavel = (
            "07797000000000000004501008460019310001802680"
        )
        self.payment_request.valorPagar = 26.80
        self.payment_request.dataVencimento = None
        with self.assertRaises(BancoInterException) as contexto:
            self.payment_request.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'requisicaoPagamento.dataVencimento' é obrigatório.",
        )

        # test invalid cases
        # valorPagar
        self.payment_request.valorPagar = 2.4
        self.payment_request.dataVencimento = "2021-07-27"
        with self.assertRaises(BancoInterException) as contexto:
            self.payment_request.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'requisicaoPagamento.valorPagar' é inválido. (de 2.5 até 99999999.99)",
        )
        # dataVencimento
        self.payment_request.valorPagar = 2.5
        self.payment_request.dataVencimento = "27/07/2024"
        with self.assertRaises(BancoInterException) as contexto:
            self.payment_request.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'requisicaoPagamento.dataVencimento' é inválido. Formato aceito: YYYY-MM-DD",
        )
        # cpfCnpjBeneficiario
        self.payment_request.valorPagar = 2.5
        self.payment_request.dataVencimento = "2021-07-27"
        self.payment_request.cpfCnpjBeneficiario = "9" * 19
        with self.assertRaises(BancoInterException) as contexto:
            self.payment_request.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'requisicaoPagamento.cpfCnpjBeneficiario' é inválido. Formato aceito: 12345678912345",
        )


if __name__ == "__main__":
    unittest.main()
