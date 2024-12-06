# tests_pix.py


import unittest

from test_criar_cobranca_imediata import TestCriarCobrancaImediata
from test_consultar_cobranca_imediata import TestConsultarCobrancaImediata
from test_revisar_cobranca_imediata import TestRevisarCobrancaImediata
from test_criar_cobranca_com_vencimento import TestCriarCobrancaComVencimento
from test_revisar_cobranca_com_vencimento import TestRevisarCobrancaComVencimento
from test_consultar_cobranca_com_vencimento import TestConsultarCobrancaComVencimento
from test_criar_webhook import TestCriarWebhook
from test_excluir_webhook import TestExcluirWebhook
from test_obter_webhook_cadastrado import TestObterWebhookCadastrado
from test_consultar_pix import TestConsultarPix


# Tests Suites
def suite():
    my_suite = unittest.TestSuite()

    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestCriarCobrancaImediata)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestRevisarCobrancaImediata)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestConsultarCobrancaImediata)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestCriarCobrancaComVencimento)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(
            TestRevisarCobrancaComVencimento
        )
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(
            TestConsultarCobrancaComVencimento
        )
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestCriarWebhook)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestObterWebhookCadastrado)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestExcluirWebhook)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestConsultarPix)
    )

    return my_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
