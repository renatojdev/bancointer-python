import unittest

from bancointer.banking.models.resposta_busca_pagamento_darf import (
    RespostaBuscaPagamentoDarf,
)

BUSCA_PAGAMENTOS_DARF_DICT = {
    "pagamentos": [
        {
            "tipoDarf": "PRETO",
            "valor": 47.14,
            "valorMulta": 0.0,
            "valorJuros": 0.0,
            "valorTotal": 47.14,
            "tipo": "Darf",
            "periodoApuracao": "2024-10-31",
            "dataPagamento": "2024-11-21",
            "referencia": "13609400849201739",
            "dataVencimento": "2024-11-30",
            "codigoReceita": "0220",
            "statusPagamento": "REALIZADO",
            "dataInclusao": "2024-11-21 15:17:58",
            "cnpjCpf": "90022400664",
            "codigoSolicitacao": "9e392015-c8a0-45c6-9dee-054f33e90ffa",
        },
        {
            "tipoDarf": "PRETO",
            "valor": 47.14,
            "valorMulta": 0.0,
            "valorJuros": 0.0,
            "valorTotal": 47.14,
            "tipo": "Darf",
            "periodoApuracao": "2024-10-31",
            "dataPagamento": "2024-11-21",
            "referencia": "13609400849201739",
            "dataVencimento": "2024-11-30",
            "codigoReceita": "0220",
            "statusPagamento": "REALIZADO",
            "dataInclusao": "2024-11-21 15:19:40",
            "cnpjCpf": "90022400664",
            "codigoSolicitacao": "ea4a165c-71cc-b8aa-39db-36b9a4f4987c",
        },
        {
            "tipoDarf": "PRETO",
            "valor": 47.14,
            "valorMulta": 0.0,
            "valorJuros": 0.0,
            "valorTotal": 47.14,
            "tipo": "Darf",
            "periodoApuracao": "2024-10-31",
            "dataPagamento": "2024-11-21",
            "referencia": "13609400849201739",
            "dataVencimento": "2024-11-30",
            "codigoReceita": "0220",
            "statusPagamento": "REALIZADO",
            "dataInclusao": "2024-11-21 15:21:54",
            "cnpjCpf": "90022400664",
            "codigoSolicitacao": "b3cfb393-5b50-d10f-0ba1-77cf3bd7536b",
        },
    ]
}


class TestRespostaRespostaBuscaPagamentoDarf(unittest.TestCase):

    def setUp(self):
        self.resposta_busca_pagamento = RespostaBuscaPagamentoDarf(
            **BUSCA_PAGAMENTOS_DARF_DICT
        )

    def test_to_dict(self):
        dict_busca_pagamento = self.resposta_busca_pagamento.to_dict()

        # Using Assertions to Check Keys
        self.assertIn("tipoDarf", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("valor", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("valorMulta", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("valorJuros", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("valorTotal", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("tipo", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("periodoApuracao", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("dataPagamento", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("referencia", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("dataVencimento", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("statusPagamento", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("dataInclusao", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("cnpjCpf", dict_busca_pagamento["pagamentos"][0])
        self.assertIn("codigoSolicitacao", dict_busca_pagamento["pagamentos"][0])

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


if __name__ == "__main__":
    unittest.main()
