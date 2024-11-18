# test_resposta_emitir_cobranca.py

import unittest

from bancointer.cobranca_v3.models import RespostaEmitirCobranca

REQUEST_CODE = "e0a856b7-02f1-4008-9999-77f30e42d621"


class TestRespostaEmitirCobranca(unittest.TestCase):

    def setUp(self):
        self.resposta_emitir_cobranca = RespostaEmitirCobranca()
        self.resposta_emitir_cobranca.codigoSolicitacao = REQUEST_CODE

    def test_to_dict(self):
        dict_sol_cobra = self.resposta_emitir_cobranca.to_dict()

        # Using Assertions to Check Keys
        self.assertIn("codigoSolicitacao", dict_sol_cobra)

        # Using Assertions to Check Values
        self.assertEqual(dict_sol_cobra["codigoSolicitacao"], REQUEST_CODE)

    def test_add_campo_adicional(self):
        self.resposta_emitir_cobranca.add_campo_adicional("campo_add_1", 1)
        self.resposta_emitir_cobranca.add_campo_adicional("campo_add_2", 2)
        self.resposta_emitir_cobranca.add_campo_adicional("campo_add_3", 3)

        # Using Assertions to Check Keys
        self.assertIn("campo_add_1", self.resposta_emitir_cobranca.campos_adicionais)
        self.assertIn("campo_add_2", self.resposta_emitir_cobranca.campos_adicionais)
        self.assertIn("campo_add_3", self.resposta_emitir_cobranca.campos_adicionais)

        # Using Assertions to Check Values
        resp_cobra_dict = self.resposta_emitir_cobranca.to_dict()
        self.assertEqual(resp_cobra_dict["campos_adicionais"]["campo_add_1"], 1)
        self.assertEqual(resp_cobra_dict["campos_adicionais"]["campo_add_2"], 2)
        self.assertEqual(resp_cobra_dict["campos_adicionais"]["campo_add_3"], 3)


if __name__ == "__main__":
    unittest.main()
