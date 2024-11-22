import unittest

from bancointer.banking.models.resposta_busca_pagamento import RespostaBuscaPagamento

BUSCA_PAGAMENTOS_DICT = {
    "pagamentos": [
        {
            "codigoTransacao": "6ad77a34-dfb4-4efa-a8c2-40c17c5346cd",
            "codigoBarra": "03395988500000666539201493990000372830030102",
            "tipo": "Pagamento",
            "dataVencimentoDigitada": "2024-11-19",
            "dataVencimentoTitulo": "2024-10-30",
            "dataInclusao": "20/11/2024 14:53:22",
            "dataPagamento": "2024-11-20",
            "valorPago": 2.5,
            "valorNominal": 666.53,
            "statusPagamento": "REALIZADO",
            "cpfCnpjBeneficiario": "99999999999999",
            "nomeBeneficiario": "BENEFICIARIO_EXEMPLO",
            "autenticacao": "849228769277280455958065168770",
        },
        {
            "codigoTransacao": "ac72024e-6961-44ff-9f3a-bbc722c869f1",
            "codigoBarra": "03395988500000666539201493990000372830030102",
            "tipo": "Pagamento",
            "dataVencimentoDigitada": "2024-11-19",
            "dataVencimentoTitulo": "2024-10-30",
            "dataInclusao": "20/11/2024 13:11:42",
            "dataPagamento": "2024-11-20",
            "valorPago": 2.5,
            "valorNominal": 666.53,
            "statusPagamento": "REALIZADO",
            "cpfCnpjBeneficiario": "99999999999999",
            "nomeBeneficiario": "BENEFICIARIO_EXEMPLO",
            "autenticacao": "835425231784764457506088907486",
        },
        {
            "codigoTransacao": "32a929a3-d3b9-4954-8f84-a593719dee2a",
            "codigoBarra": "03395988500000666539201493990000372830030102",
            "tipo": "Pagamento",
            "dataVencimentoDigitada": "2024-11-19",
            "dataVencimentoTitulo": "2024-10-30",
            "dataInclusao": "20/11/2024 14:27:17",
            "dataPagamento": "2024-11-20",
            "valorPago": 2.5,
            "valorNominal": 666.53,
            "statusPagamento": "REALIZADO",
            "cpfCnpjBeneficiario": "99999999999999",
            "nomeBeneficiario": "BENEFICIARIO_EXEMPLO",
            "autenticacao": "855825524582762960337333331946",
        },
        {
            "codigoTransacao": "72324a7f-0703-431f-a85a-97794f94e360",
            "codigoBarra": "03395988500000666539201493990000372830030102",
            "tipo": "Pagamento",
            "dataVencimentoDigitada": "2024-11-24",
            "dataVencimentoTitulo": "2024-10-30",
            "dataInclusao": "22/11/2024 07:03:11",
            "dataPagamento": "2024-11-24",
            "valorPago": 2.5,
            "valorNominal": 666.53,
            "statusPagamento": "AGENDADO_CANCELADO",
            "cpfCnpjBeneficiario": "99999999999999",
            "nomeBeneficiario": "BENEFICIARIO_EXEMPLO",
            "autenticacao": "154141137136282680396096145711",
        },
    ]
}


class TestRespostaRespostaBuscaPagamento(unittest.TestCase):

    def setUp(self):
        self.resposta_busca_pagamento = RespostaBuscaPagamento(**BUSCA_PAGAMENTOS_DICT)

    def test_to_dict(self):
        dict_busca_pagamento = self.resposta_busca_pagamento.to_dict()

        # Using Assertions to Check Keys
        self.assertIn("codigoTransacao", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("codigoBarra", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("tipo", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("dataVencimentoDigitada", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("dataVencimentoTitulo", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("dataInclusao", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("dataPagamento", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("valorPago", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("valorNominal", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("statusPagamento", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("cpfCnpjBeneficiario", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("nomeBeneficiario", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("autenticacao", dict_busca_pagamento["pagamentos"][0])

        # Using Assertions to Check Values
        self.assertEqual(
            dict_busca_pagamento["pagamentos"][0],
            self.resposta_busca_pagamento.pagamentos[0],
        )
        self.assertEqual(
            dict_busca_pagamento["pagamentos"][1],
            self.resposta_busca_pagamento.pagamentos[1],
        )
        self.assertEqual(
            dict_busca_pagamento["pagamentos"][2],
            self.resposta_busca_pagamento.pagamentos[2],
        )
        self.assertEqual(
            dict_busca_pagamento["pagamentos"][3],
            self.resposta_busca_pagamento.pagamentos[3],
        )


if __name__ == "__main__":
    unittest.main()
