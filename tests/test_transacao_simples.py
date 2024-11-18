# test_transacao_simples.py

import unittest

from bancointer.banking.models.transacao_simples import TransacaoSimples


class TestTransacaoSimples(unittest.TestCase):

    def setUp(self):
        self.transacao_simples = TransacaoSimples(
            "",
            "2024-03-25",
            "PAGAMENTO",
            "D",
            "107.61",
            "Pagamento efetuado",
            "AYMORE CREDITO, FINANCIAMENTO E INV S.A",
        )

    def test_to_dict(self):
        dict_resp_simple_trans = self.transacao_simples.to_dict()

        # Using Assertions to Check Keys
        self.assertIn("dataEntrada", dict_resp_simple_trans)
        self.assertIn("tipoTransacao", dict_resp_simple_trans)
        self.assertIn("tipoOperacao", dict_resp_simple_trans)
        self.assertIn("valor", dict_resp_simple_trans)
        self.assertIn("titulo", dict_resp_simple_trans)
        self.assertIn("descricao", dict_resp_simple_trans)

        # Using Assertions to Check Values
        self.assertEqual(dict_resp_simple_trans["dataEntrada"], "2024-03-25")
        self.assertEqual(dict_resp_simple_trans["tipoTransacao"], "PAGAMENTO")
        self.assertEqual(dict_resp_simple_trans["tipoOperacao"], "D")
        self.assertEqual(dict_resp_simple_trans["valor"], "107.61")
        self.assertEqual(dict_resp_simple_trans["titulo"], "Pagamento efetuado")
        self.assertEqual(
            dict_resp_simple_trans["descricao"],
            "AYMORE CREDITO, FINANCIAMENTO E INV S.A",
        )


if __name__ == "__main__":
    unittest.main()
