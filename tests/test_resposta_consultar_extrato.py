# test_resposta_consultar_extrato.py

import unittest

from bancointer.banking.models.resposta_consultar_extrato import (
    RespostaConsultarExtrato,
)


class TestRespostaConsultarExtrato(unittest.TestCase):

    def setUp(self):
        self.resposta_consultar_extrato = RespostaConsultarExtrato()
        self.resposta_consultar_extrato.transacoes = [
            {
                "dataEntrada": "2024-03-24",
                "tipoTransacao": "OUTROS",
                "tipoOperacao": "D",
                "valor": "1000.00",
                "titulo": "Debito Renda Fixa",
                "descricao": "Investimentos",
            },
            {
                "dataEntrada": "2024-03-24",
                "tipoTransacao": "OUTROS",
                "tipoOperacao": "D",
                "valor": "10.00",
                "titulo": "Ted Enviada",
            },
            {
                "dataEntrada": "2024-03-24",
                "tipoTransacao": "OUTROS",
                "tipoOperacao": "D",
                "valor": "10.00",
                "titulo": "Ted Enviada",
            },
            {
                "dataEntrada": "2024-03-24",
                "tipoTransacao": "OUTROS",
                "tipoOperacao": "D",
                "valor": "10.00",
                "titulo": "Ted Enviada",
            },
            {
                "dataEntrada": "2024-03-24",
                "tipoTransacao": "OUTROS",
                "tipoOperacao": "D",
                "valor": "1000.00",
                "titulo": "Debito Renda Fixa",
            },
            {
                "dataEntrada": "2024-03-24",
                "tipoTransacao": "ESTORNO",
                "tipoOperacao": "C",
                "valor": "1000.00",
                "titulo": "Estorno ",
                "descricao": "",
            },
            {
                "dataEntrada": "2024-03-24",
                "tipoTransacao": "OUTROS",
                "tipoOperacao": "D",
                "valor": "1000.00",
                "titulo": "Debito Renda Fixa",
            },
            {
                "dataEntrada": "2024-03-24",
                "tipoTransacao": "ESTORNO",
                "tipoOperacao": "C",
                "valor": "1000.00",
                "titulo": "Estorno ",
                "descricao": "",
            },
            {
                "dataEntrada": "2024-03-24",
                "tipoTransacao": "OUTROS",
                "tipoOperacao": "D",
                "valor": "1000.00",
                "titulo": "Debito Renda Fixa",
            },
            {
                "dataEntrada": "2024-03-24",
                "tipoTransacao": "ESTORNO",
                "tipoOperacao": "C",
                "valor": "1000.00",
                "titulo": "Estorno ",
                "descricao": "",
            },
            {
                "dataEntrada": "2024-03-24",
                "tipoTransacao": "OUTROS",
                "tipoOperacao": "D",
                "valor": "54.23",
                "titulo": "Pagam. Eletropaulo",
            },
            {"dataEntrada": "2024-03-24", "tipoOperacao": "D", "valor": "1000.00"},
            {"dataEntrada": "2024-03-24", "tipoOperacao": "C", "valor": "1000.00"},
            {
                "dataEntrada": "2024-03-25",
                "tipoTransacao": "PAGAMENTO",
                "tipoOperacao": "D",
                "valor": "107.61",
                "titulo": "Pagamento efetuado",
                "descricao": "AYMORE CREDITO, FINANCIAMENTO E INV S.A",
            },
            {
                "dataEntrada": "2024-03-25",
                "tipoTransacao": "OUTROS",
                "tipoOperacao": "D",
                "valor": "143.13",
                "titulo": "Pagamento De Convenio",
            },
            {
                "dataEntrada": "2024-03-25",
                "tipoTransacao": "OUTROS",
                "tipoOperacao": "D",
                "valor": "11.11",
                "titulo": "Ted Enviada",
            },
        ]

    def test_to_dict(self):
        dict_resp_cons_extrato = self.resposta_consultar_extrato.to_dict()

        # Using Assertions to Check Keys
        self.assertIn("dataEntrada", dict_resp_cons_extrato["transacoes"][0])
        self.assertIn("tipoTransacao", dict_resp_cons_extrato["transacoes"][0])
        self.assertIn("tipoOperacao", dict_resp_cons_extrato["transacoes"][0])
        self.assertIn("valor", dict_resp_cons_extrato["transacoes"][0])
        self.assertIn("titulo", dict_resp_cons_extrato["transacoes"][0])
        self.assertIn("descricao", dict_resp_cons_extrato["transacoes"][0])
        self.assertIn("descricao", dict_resp_cons_extrato["transacoes"][5])

        # Using Assertions to Check Values
        self.assertEqual(
            dict_resp_cons_extrato["transacoes"][0]["dataEntrada"], "2024-03-24"
        )
        self.assertEqual(
            dict_resp_cons_extrato["transacoes"][0]["tipoTransacao"], "OUTROS"
        )
        self.assertEqual(dict_resp_cons_extrato["transacoes"][0]["tipoOperacao"], "D")
        self.assertEqual(dict_resp_cons_extrato["transacoes"][0]["valor"], "1000.00")
        self.assertEqual(
            dict_resp_cons_extrato["transacoes"][0]["titulo"], "Debito Renda Fixa"
        )
        self.assertEqual(
            dict_resp_cons_extrato["transacoes"][0]["descricao"], "Investimentos"
        )
        self.assertEqual(dict_resp_cons_extrato["transacoes"][5]["descricao"], "")


if __name__ == "__main__":
    unittest.main()
