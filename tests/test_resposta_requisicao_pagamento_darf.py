# test_resposta_requisicao_pagamento_darf.py


import unittest

from bancointer.banking.models.resposta_requisicao_pagamento_darf import (
    RespostaRequisicaoPagamentoDarf,
)
from bancointer.banking.models.tipo_retorno import TipoRetorno


class TestRespostaRequisicaoPagamentoDarf(unittest.TestCase):

    def setUp(self):
        self.resposta_req_pag = RespostaRequisicaoPagamentoDarf(
            "12345678910433",
            "23/01/2022",
            TipoRetorno.PAGAMENTO.value,
            "8bbdede4-35db-4ec9-b652-e176841e62c8",
        )

    def test_to_dict(self):
        resposta_req_pag_dict = self.resposta_req_pag.to_dict()

        # Using Assertions to Check Keys
        self.assertIn("autenticacao", resposta_req_pag_dict)
        self.assertIn("dataPagamento", resposta_req_pag_dict)
        self.assertIn("tipoRetorno", resposta_req_pag_dict)
        self.assertIn("codigoSolicitacao", resposta_req_pag_dict)

        # Using Assertions to Check Values
        self.assertEqual(resposta_req_pag_dict["autenticacao"], "12345678910433")
        self.assertEqual(resposta_req_pag_dict["dataPagamento"], "23/01/2022")
        self.assertEqual(
            resposta_req_pag_dict["tipoRetorno"], TipoRetorno.PAGAMENTO.value
        )
        self.assertEqual(
            resposta_req_pag_dict["codigoSolicitacao"],
            "8bbdede4-35db-4ec9-b652-e176841e62c8",
        )


if __name__ == "__main__":
    unittest.main()
