# tests_banking.py


import unittest

from test_consultar_extrato import TestConsultarExtrato
from test_consultar_extrato_pdf import TestConsultarExtratoPDF
from test_consultar_saldo import TestConsultarSaldo


# Tests Suites
def suite():
    my_suite = unittest.TestSuite()

    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestConsultarSaldo)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestConsultarExtrato)
    )
    my_suite.addTests(
        unittest.defaultTestLoader.loadTestsFromTestCase(TestConsultarExtratoPDF)
    )

    return my_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
