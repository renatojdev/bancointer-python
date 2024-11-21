# test_resposta_requisicao_pagamento.py


import unittest

from bancointer.banking.models.resposta_requisicao_pagamento import (
    RespostaRequisicaoPagamento,
)
from bancointer.banking.models.status_pagamento import StatusPagamento


class TestRespostaRequisicaoPagamento(unittest.TestCase):

    def setUp(self):
        self.resposta_req_pag = RespostaRequisicaoPagamento(
            2,
            StatusPagamento.EMPROCESSAMENTO,
            "8bbdede4-35db-4ec9-b652-e176841e62c8",
            "2024-11-22",
        )

    def test_to_dict(self):
        resposta_req_pag_dict = self.resposta_req_pag.to_dict()

        # Using Assertions to Check Keys
        self.assertIn("quantidadeAprovadores", resposta_req_pag_dict)
        self.assertIn("statusPagamento", resposta_req_pag_dict)
        self.assertIn("codigoTransacao", resposta_req_pag_dict)
        self.assertIn("dataAgendamento", resposta_req_pag_dict)

        # Using Assertions to Check Values
        self.assertEqual(resposta_req_pag_dict["quantidadeAprovadores"], 2)
        self.assertEqual(
            resposta_req_pag_dict["statusPagamento"], StatusPagamento.EMPROCESSAMENTO
        )
        self.assertEqual(
            resposta_req_pag_dict["codigoTransacao"],
            "8bbdede4-35db-4ec9-b652-e176841e62c8",
        )
        self.assertEqual(resposta_req_pag_dict["dataAgendamento"], "2024-11-22")


if __name__ == "__main__":
    unittest.main()
