# test_resposta_consulta_pagamento_pix.py


import unittest

from bancointer.banking.models.resposta_consulta_pagamento_pix import (
    RespostaConsultaPagamentoPix,
)

RESPOSTA_CONSULTA_PAGAMENTO_PIX_DICT = {
    "transacaoPix": {
        "contaCorrente": "33641836",
        "recebedor": {},
        "erros": [],
        "endToEnd": "ycBfckBuoeNi2vTb6mrpCYZtBBUZ6g79",
        "valor": 46.17,
        "status": "PAGO",
        "dataHoraMovimento": "2024-11-27T17:17:20.249Z",
        "dataHoraSolicitacao": "2024-11-27T17:17:20.249Z",
        "chave": "+5541943339900",
        "codigoSolicitacao": "ad930c2f-3d68-927e-23f4-98fe41de18fe",
    },
    "historico": [
        {"status": "TRANSACAO_CRIADA", "dataHoraEvento": "2024-11-27T17:17:20.249Z"},
        {"status": "TRANSACAO_APROVADA", "dataHoraEvento": "2024-11-27T17:17:20.249Z"},
        {"status": "PIX_ENVIADO", "dataHoraEvento": "2024-11-27T17:17:20.249Z"},
        {"status": "PIX_PAGO", "dataHoraEvento": "2024-11-27T17:17:20.249Z"},
    ],
}


class TestRespostaConsultaPagamentoPix(unittest.TestCase):

    def setUp(self):
        self.resposta_consulta_pagamento_pix = RespostaConsultaPagamentoPix(
            **RESPOSTA_CONSULTA_PAGAMENTO_PIX_DICT
        )

    def test_to_dict(self):
        resp_cons_pag_pix_dict = self.resposta_consulta_pagamento_pix.to_dict()

        # Using Assertions to Check Keys
        self.assertIn("transacaoPix", resp_cons_pag_pix_dict)
        self.assertIn("contaCorrente", resp_cons_pag_pix_dict["transacaoPix"])
        self.assertIn("recebedor", resp_cons_pag_pix_dict["transacaoPix"])
        self.assertIn("erros", resp_cons_pag_pix_dict["transacaoPix"])
        self.assertIn("endToEnd", resp_cons_pag_pix_dict["transacaoPix"])
        self.assertIn("valor", resp_cons_pag_pix_dict["transacaoPix"])
        self.assertIn("status", resp_cons_pag_pix_dict["transacaoPix"])
        self.assertIn("dataHoraMovimento", resp_cons_pag_pix_dict["transacaoPix"])
        self.assertIn("dataHoraSolicitacao", resp_cons_pag_pix_dict["transacaoPix"])
        self.assertIn("chave", resp_cons_pag_pix_dict["transacaoPix"])
        self.assertIn("codigoSolicitacao", resp_cons_pag_pix_dict["transacaoPix"])
        self.assertIn("historico", resp_cons_pag_pix_dict)
        self.assertIn("status", resp_cons_pag_pix_dict["historico"][0])
        self.assertIn("dataHoraEvento", resp_cons_pag_pix_dict["historico"][0])

        # Using Assertions to Check Values
        self.assertEqual(
            resp_cons_pag_pix_dict["transacaoPix"],
            self.resposta_consulta_pagamento_pix.transacaoPix,
        )
        self.assertEqual(resp_cons_pag_pix_dict["transacaoPix"]["valor"], 46.17)
        self.assertEqual(
            resp_cons_pag_pix_dict["transacaoPix"]["chave"], "+5541943339900"
        )
        self.assertEqual(
            resp_cons_pag_pix_dict["transacaoPix"]["codigoSolicitacao"],
            "ad930c2f-3d68-927e-23f4-98fe41de18fe",
        )
        self.assertEqual(
            resp_cons_pag_pix_dict["historico"],
            self.resposta_consulta_pagamento_pix.historico,
        )
        self.assertEqual(len(self.resposta_consulta_pagamento_pix.historico), 4)


if __name__ == "__main__":
    unittest.main()
