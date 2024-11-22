# test_requisicao_pagamento_darf.py


import json
import unittest

from bancointer.banking.models.requisicao_pagamento_darf import RequisicaoPagamentoDarf
from bancointer.utils.exceptions import BancoInterException

PAYMENT_REQUEST = b"""{
                        "cnpjCpf": "90022400664",
                        "codigoReceita": "0220",
                        "dataVencimento": "2022-01-30",
                        "descricao": "Pagamento DARF Janeiro",
                        "nomeEmpresa": "Minha Empresa",
                        "telefoneEmpresa": "031999911111",
                        "periodoApuracao": "2020-01-31",
                        "valorPrincipal": 47.14,
                        "valorMulta": 27.48,
                        "valorJuros": 10.11,
                        "referencia": "13609400849201739"
                    }"""


class TestRequisicaoPagamentoDarf(unittest.TestCase):

    def setUp(self):
        """Cobranca object for test purposes."""
        self.payment_request = RequisicaoPagamentoDarf(**json.loads(PAYMENT_REQUEST))

    def test_to_dict(self):
        dict_cobra = self.payment_request.to_dict()
        # Using Assertions to Check Keys
        self.assertIn("cnpjCpf", dict_cobra)
        self.assertIn("codigoReceita", dict_cobra)
        self.assertIn("dataVencimento", dict_cobra)
        self.assertIn("descricao", dict_cobra)
        self.assertIn("nomeEmpresa", dict_cobra)
        self.assertIn("telefoneEmpresa", dict_cobra)
        self.assertIn("periodoApuracao", dict_cobra)
        self.assertIn("valorPrincipal", dict_cobra)
        self.assertIn("valorMulta", dict_cobra)
        self.assertIn("valorJuros", dict_cobra)
        self.assertIn("referencia", dict_cobra)
        # Using Assertions to Check Values
        self.assertEqual(dict_cobra["cnpjCpf"], "90022400664")
        self.assertEqual(dict_cobra["codigoReceita"], "0220")
        self.assertEqual(dict_cobra["dataVencimento"], "2022-01-30")
        self.assertEqual(dict_cobra["descricao"], "Pagamento DARF Janeiro")
        self.assertEqual(dict_cobra["nomeEmpresa"], "Minha Empresa")

    def test_to_dict_failures(self):
        # cnpjCpf required
        self.payment_request.cnpjCpf = None
        with self.assertRaises(BancoInterException) as contexto:
            self.payment_request.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'requisicaoPagamentoDarf.cnpjCpf' é obrigatório.",
        )
        # codigoReceita required
        self.payment_request.cnpjCpf = "90022400664"
        self.payment_request.codigoReceita = None
        with self.assertRaises(BancoInterException) as contexto:
            self.payment_request.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'requisicaoPagamentoDarf.codigoReceita' é obrigatório.",
        )

        # test invalid cases
        # codigoReceita
        self.payment_request.codigoReceita = "123"
        with self.assertRaises(BancoInterException) as contexto:
            self.payment_request.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'requisicaoPagamentoDarf.codigoReceita' é inválido. (=4 characters)",
        )
        # nomeEmpresa
        self.payment_request.codigoReceita = "1473"
        self.payment_request.nomeEmpresa = "NE" * 51
        with self.assertRaises(BancoInterException) as contexto:
            self.payment_request.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'requisicaoPagamentoDarf.nomeEmpresa' é inválido. Formato aceito: (<= 100 characters)",
        )
        # referencia
        self.payment_request.nomeEmpresa = "Minha Empresa"
        self.payment_request.referencia = "C" * 31
        with self.assertRaises(BancoInterException) as contexto:
            self.payment_request.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'requisicaoPagamentoDarf.referencia' é inválido. Formato aceito: (<= 30 characters)",
        )


if __name__ == "__main__":
    unittest.main()
