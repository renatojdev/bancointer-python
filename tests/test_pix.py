# test_pix.py

import unittest
import json

from bancointer.cobranca_v3.models import Pix


TXID = "336418361731693413000jHo3g7F0F2XXcE"
PIX_COPIA_E_COLA = "000201010212261010014BR.GOV.BCB.PIX2579cdpj-sandbox.partners.uatinter.co/pj-s/v2/cobv/9ba336dffb5d483c995e08e586da6cad52040000530398654042.505802BR5901*6013Belo Horizont61089999999962070503***630439AC"


class TestPix(unittest.TestCase):

    def setUp(self):
        """Message object for test purposes."""
        self.pix = Pix(TXID, PIX_COPIA_E_COLA)

    def test_to_dict(self):
        dict_pix = self.pix.to_dict()
        # Using Assertions to Check Keys
        self.assertIn("txid", dict_pix)
        self.assertIn("pixCopiaECola", dict_pix)
        # Using Assertions to Check Values
        self.assertEqual(dict_pix["txid"], TXID)
        self.assertEqual(dict_pix["pixCopiaECola"], PIX_COPIA_E_COLA)

    def test_to_json(self):
        """Test whether the to_json method returns a valid JSON string."""
        json_pix = self.pix.to_json()
        # Verifica se o resultado é uma string
        self.assertIsInstance(json_pix, str)

        # Checks if the JSON string contains the expected keys
        data = json.loads(json_pix)
        self.assertEqual(data["txid"], TXID)
        self.assertEqual(data["pixCopiaECola"], PIX_COPIA_E_COLA)

    def test_from_json(self):
        """Test whether the from_json method creates a Message object correctly."""
        json_pix = self.pix.to_json()
        new_message = Pix.from_json(json_pix)

        # Checks if the new object is an instance of Message
        self.assertIsInstance(new_message, Pix)

        # Checks whether the attributes of the new object match the original ones
        self.assertEqual(new_message.txid, self.pix.txid)
        self.assertEqual(new_message.pixCopiaECola, self.pix.pixCopiaECola)


if __name__ == "__main__":
    unittest.main()
