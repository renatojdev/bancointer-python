# test_resposta_requisicao_pagamento_pix.py


import unittest

from bancointer.banking.models.resposta_requisicao_pagamento_pix import (
    RespostaRequisicaoPagamentoPix,
)
from bancointer.banking.models.tipo_retorno_pagamento_pix import TipoRetornoPagamentoPix


class TestRespostaRequisicaoPagamentoPix(unittest.TestCase):

    def setUp(self):
        self.resposta_req_pag = RespostaRequisicaoPagamentoPix(
            TipoRetornoPagamentoPix.PROCESSADO,
            "c42f0787-02cb-4b31-827e-459ec9d7ece1",
            "2022-03-15",
            "2022-03-15",
        )

    def test_to_dict(self):
        resposta_req_pag_dict = self.resposta_req_pag.to_dict()

        # Using Assertions to Check Keys
        self.assertIn("tipoRetorno", resposta_req_pag_dict)
        self.assertIn("codigoSolicitacao", resposta_req_pag_dict)
        self.assertIn("dataPagamento", resposta_req_pag_dict)
        self.assertIn("dataOperacao", resposta_req_pag_dict)

        # Using Assertions to Check Values
        self.assertEqual(
            resposta_req_pag_dict["codigoSolicitacao"],
            "c42f0787-02cb-4b31-827e-459ec9d7ece1",
        )
        self.assertEqual(resposta_req_pag_dict["dataPagamento"], "2022-03-15")
        self.assertEqual(
            resposta_req_pag_dict["tipoRetorno"], TipoRetornoPagamentoPix.PROCESSADO
        )
        self.assertEqual(resposta_req_pag_dict["dataOperacao"], "2022-03-15")


if __name__ == "__main__":
    unittest.main()
