# test_cobranca.py

import unittest
import json

from bancointer.cobranca_v3.models import Cobranca, Pessoa, PersonType
from bancointer.utils.exceptions import BancoInterException


class TestCobranca(unittest.TestCase):

    def setUp(self):
        """Cobranca object for test purposes."""
        pessoa_pagador = Pessoa(
            "9" * 11,  # valido
            PersonType.FISICA,
            "NOME DO PAGADOR",
            "ENDERECO DO PAGADOR",
            "CIDADE DO PAGADOR",
            "PR",
            "80030000",
        )  # OU FISICA # Pagador
        self.cobranca = Cobranca.criar_sobranca_simples(
            "0001", 2.5, "2024-11-21", pessoa_pagador
        )

    def test_to_dict(self):
        dict_cobra = self.cobranca.to_dict()
        # Using Assertions to Check Keys
        self.assertIn("seuNumero", dict_cobra)
        self.assertIn("valorNominal", dict_cobra)
        self.assertIn("dataVencimento", dict_cobra)
        # Using Assertions to Check Values
        self.assertEqual(dict_cobra["seuNumero"], "0001")
        self.assertEqual(dict_cobra["valorNominal"], 2.5)
        self.assertEqual(dict_cobra["dataVencimento"], "2024-11-21")

    def test_to_dict_failures(self):
        # invalid seuNumero
        cobranca = Cobranca.criar_sobranca_simples("9" * 16, 2.5, "2024-11-21", {})
        with self.assertRaises(BancoInterException) as contexto:
            cobranca.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'cobranca.seuNumero' é inválido. (de 1 a 15)",
        )
        # invalid valorNominal
        cobranca = Cobranca.criar_sobranca_simples(
            "0001", 100000000.00, "2024-11-21", {}
        )
        with self.assertRaises(BancoInterException) as contexto:
            cobranca.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'cobranca.valorNominal' é inválido. (de 2.5 até 99999999.99)",
        )
        # invalid dataVencimento
        cobranca = Cobranca.criar_sobranca_simples("0001", 2.5, "21/11/2024", {})
        with self.assertRaises(BancoInterException) as contexto:
            cobranca.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'cobranca.dataVencimento' é inválido. Formato aceito: YYYY-MM-DD",
        )  # invalid date
        # invalid numDiasAgenda
        cobranca = Cobranca.criar_sobranca_simples("0001", 2.5, "2024-11-21", {})
        cobranca.numDiasAgenda = 62
        with self.assertRaises(BancoInterException) as contexto:
            cobranca.to_dict()
        self.assertEqual(
            str(contexto.exception.erro.descricao),
            "O atributo 'cobranca.numDiasAgenda' é inválido. (de 0 até 60)",
        )

    def test_to_json(self):
        """Test whether the to_json method returns a valid JSON string."""
        json_cobra = self.cobranca.to_json()
        self.assertIsInstance(json_cobra, str)

        # Checks if the JSON string contains the expected keys
        data = json.loads(json_cobra)
        self.assertEqual(data["seuNumero"], "0001")
        self.assertEqual(data["valorNominal"], 2.5)
        self.assertEqual(data["dataVencimento"], "2024-11-21")

    def test_from_json(self):
        """Test whether the from_json method creates a Message object correctly."""
        json_cobra = self.cobranca.to_json()
        new_cobranca = Cobranca.from_json(json_cobra)

        # Checks if the new object is an instance of Message
        self.assertIsInstance(new_cobranca, Cobranca)

        # Checks whether the attributes of the new object match the original ones
        self.assertEqual(new_cobranca.seuNumero, self.cobranca.seuNumero)
        self.assertEqual(new_cobranca.dataEmissao, self.cobranca.dataEmissao)
        self.assertEqual(new_cobranca.dataVencimento, self.cobranca.dataVencimento)
        self.assertEqual(new_cobranca.valorNominal, self.cobranca.valorNominal)
        self.assertEqual(new_cobranca.numDiasAgenda, self.cobranca.numDiasAgenda)
        self.assertEqual(new_cobranca.pagador, self.cobranca.pagador.to_dict())


if __name__ == "__main__":
    unittest.main()
