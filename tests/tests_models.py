# tests_models.py


import unittest

from test_desconto import TestDesconto
from test_pessoa import TestPessoa
from test_message import TestMessage
from test_mora import TestMora
from test_multa import TestMulta
from test_resposta_emitir_cobranca import TestRespostaEmitirCobranca
from test_resposta_recuperar_cobranca import TestRespostaRecuperarCobranca
from test_solicitacao_emitir_cobranca import TestSolicitacaoEmitirCobranca
from test_pix import TestPix
from test_resposta_consultar_extrato import TestRespostaConsultarExtrato
from test_resposta_consultar_saldo import TestRespostaConsultarSaldo
from test_transacao_simples import TestTransacaoSimples


# Tests Suites
def suite():
    my_suite = unittest.TestSuite()
    # Cobranca
    my_suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestPessoa))
    my_suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestDesconto))
    my_suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestMessage))
    my_suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestMora))
    my_suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestMulta))
    my_suite.addTests(unittest.defaultTestLoader.loadTestsFromTestCase(TestPix))
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestRespostaEmitirCobranca)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestRespostaRecuperarCobranca)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestSolicitacaoEmitirCobranca)
    )
    # Banking
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestTransacaoSimples)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestRespostaConsultarSaldo)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestRespostaConsultarExtrato)
    )

    return my_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
