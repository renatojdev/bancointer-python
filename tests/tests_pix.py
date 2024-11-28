# tests_pix.py


import unittest

from test_criar_cobranca_imediata import TestCriarCobrancaImediata


# Tests Suites
def suite():
    my_suite = unittest.TestSuite()

    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestCriarCobrancaImediata)
    )

    return my_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
