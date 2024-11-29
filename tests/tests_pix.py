# tests_pix.py


import unittest

from test_criar_cobranca_imediata import TestCriarCobrancaImediata
from test_consultar_cobranca_imediata import TestConsultarCobrancaImediata


# Tests Suites
def suite():
    my_suite = unittest.TestSuite()

    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestCriarCobrancaImediata)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestConsultarCobrancaImediata)
    )

    return my_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
