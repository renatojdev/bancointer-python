# test_resposta_consultar_saldo.py

import unittest

from bancointer.banking.models.resposta_consultar_saldo import RespostaConsultarSaldo


class TestRespostaConsultarSaldo(unittest.TestCase):

    def setUp(self):
        self.resposta_consultar_saldo = RespostaConsultarSaldo()
        self.resposta_consultar_saldo.bloqueadoCheque = 1.2
        self.resposta_consultar_saldo.disponivel = 1.3
        self.resposta_consultar_saldo.bloqueadoJudicialmente = 1.4
        self.resposta_consultar_saldo.bloqueadoAdministrativo = 1.5
        self.resposta_consultar_saldo.limite = 99999.88

    def test_to_dict(self):
        dict_resp_cons_saldo = self.resposta_consultar_saldo.to_dict()

        # Using Assertions to Check Keys
        self.assertIn("bloqueadoCheque", dict_resp_cons_saldo)
        self.assertIn("disponivel", dict_resp_cons_saldo)
        self.assertIn("bloqueadoJudicialmente", dict_resp_cons_saldo)
        self.assertIn("bloqueadoAdministrativo", dict_resp_cons_saldo)
        self.assertIn("limite", dict_resp_cons_saldo)

        # Using Assertions to Check Values
        self.assertEqual(dict_resp_cons_saldo["bloqueadoCheque"], 1.2)
        self.assertEqual(dict_resp_cons_saldo["disponivel"], 1.3)
        self.assertEqual(dict_resp_cons_saldo["bloqueadoJudicialmente"], 1.4)
        self.assertEqual(dict_resp_cons_saldo["bloqueadoAdministrativo"], 1.5)
        self.assertEqual(dict_resp_cons_saldo["limite"], 99999.88)


if __name__ == "__main__":
    unittest.main()
