# test_mora.py

import unittest
import json

from bancointer.cobranca_v3.models.mora import Mora


class TestMora(unittest.TestCase):

    def setUp(self):
        """Message object for test purposes."""
        self.mora = Mora("TAXAMENSAL", 0, 1.2)

    def test_to_dict(self):
        dict_mora = self.mora.to_dict()
        # Using Assertions to Check Keys
        self.assertIn("codigo", dict_mora)
        self.assertIn("valor", dict_mora)
        self.assertIn("taxa", dict_mora)
        # Using Assertions to Check Values
        self.assertEqual(dict_mora["codigo"], "TAXAMENSAL")
        self.assertEqual(dict_mora["valor"], 0)
        self.assertEqual(dict_mora["taxa"], 1.2)

    def test_to_json(self):
        """Test whether the to_json method returns a valid JSON string."""
        json_mora = self.mora.to_json()
        # Verifica se o resultado é uma string
        self.assertIsInstance(json_mora, str)

        # Checks if the JSON string contains the expected keys
        data = json.loads(json_mora)
        self.assertEqual(data["codigo"], "TAXAMENSAL")
        self.assertEqual(data["valor"], 0)
        self.assertEqual(data["taxa"], 1.2)

    def test_from_json(self):
        """Test whether the from_json method creates a Message object correctly."""
        json_mora = self.mora.to_json()
        new_message = Mora.from_json(json_mora)

        # Checks if the new object is an instance of Message
        self.assertIsInstance(new_message, Mora)

        # Checks whether the attributes of the new object match the original ones
        self.assertEqual(new_message.codigo, self.mora.codigo)
        self.assertEqual(new_message.valor, self.mora.valor)
        self.assertEqual(new_message.taxa, self.mora.taxa)


if __name__ == "__main__":
    unittest.main()
