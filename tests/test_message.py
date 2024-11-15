# test_message.py

import unittest
import json

from bancointer.cobranca_v3.models.message import Message


class TestMessage(unittest.TestCase):

    def setUp(self):
        """Message object for test purposes."""
        self.message = Message(
            "message 1", "message 2", "message 3", "message 4", "message 5"
        )

    def test_to_json(self):
        """Test whether the to_json method returns a valid JSON string."""
        json_message = self.message.to_json()
        # Verifica se o resultado é uma string
        self.assertIsInstance(json_message, str)

        # Checks if the JSON string contains the expected keys
        data = json.loads(json_message)
        self.assertEqual(data["linha1"], "message 1")
        self.assertEqual(data["linha2"], "message 2")
        self.assertEqual(data["linha3"], "message 3")
        self.assertEqual(data["linha4"], "message 4")
        self.assertEqual(data["linha5"], "message 5")

    def test_from_json(self):
        """Test whether the from_json method creates a Message object correctly."""
        json_message = self.message.to_json()
        new_message = Message.from_json(json_message)

        # Checks if the new object is an instance of Message
        self.assertIsInstance(new_message, Message)

        # Checks whether the attributes of the new object match the original ones
        self.assertEqual(new_message.linha1, self.message.linha1)
        self.assertEqual(new_message.linha2, self.message.linha2)
        self.assertEqual(new_message.linha3, self.message.linha3)
        self.assertEqual(new_message.linha4, self.message.linha4)
        self.assertEqual(new_message.linha5, self.message.linha5)


if __name__ == "__main__":
    unittest.main()
