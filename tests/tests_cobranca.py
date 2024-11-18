# tests_cobranca.py


import unittest

from test_recuperar_cobranca_pdf import TestRecuperaCobrancaPDF
from test_recuperar_cobranca import TestRecuperaCobranca
from test_emitir_cobranca import TestEmitirCobranca
from test_cancelar_cobranca import TestCancelaCobranca


# Tests Suites
def suite():
    my_suite = unittest.TestSuite()

    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestEmitirCobranca)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestCancelaCobranca)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestRecuperaCobranca)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestRecuperaCobrancaPDF)
    )

    return my_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
