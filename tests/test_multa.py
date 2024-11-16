# test_multa.py

import unittest
import json

from bancointer.cobranca_v3.models.multa import Multa


class TestMulta(unittest.TestCase):

    def setUp(self):
        """Message object for test purposes."""
        self.multa = Multa("PERCENTUAL", 2.1, 0)

    def test_to_dict(self):
        dict_multa = self.multa.to_dict()
        # Using Assertions to Check Keys
        self.assertIn("codigo", dict_multa)
        self.assertIn("valor", dict_multa)
        self.assertIn("taxa", dict_multa)
        # Using Assertions to Check Values
        self.assertEqual(dict_multa["codigo"], "PERCENTUAL")
        self.assertEqual(dict_multa["valor"], 0)
        self.assertEqual(dict_multa["taxa"], 2.1)

    def test_to_json(self):
        """Test whether the to_json method returns a valid JSON string."""
        json_multa = self.multa.to_json()
        # Verifica se o resultado é uma string
        self.assertIsInstance(json_multa, str)

        # Checks if the JSON string contains the expected keys
        data = json.loads(json_multa)
        self.assertEqual(data["codigo"], "PERCENTUAL")
        self.assertEqual(data["taxa"], 2.1)
        self.assertEqual(data["valor"], 0)

    def test_from_json(self):
        """Test whether the from_json method creates a Message object correctly."""
        json_multa = self.multa.to_json()
        new_message = Multa.from_json(json_multa)

        # Checks if the new object is an instance of Message
        self.assertIsInstance(new_message, Multa)

        # Checks whether the attributes of the new object match the original ones
        self.assertEqual(new_message.codigo, self.multa.codigo)
        self.assertEqual(new_message.taxa, self.multa.taxa)
        self.assertEqual(new_message.valor, self.multa.valor)


if __name__ == "__main__":
    unittest.main()
