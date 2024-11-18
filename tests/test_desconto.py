# test_desconto.py

import unittest
import json

from bancointer.cobranca_v3.models.desconto import Desconto


class TestDesconto(unittest.TestCase):

    def setUp(self):
        """Configura um objeto Discount para os testes."""
        self.desconto = Desconto("VALORFIXODATAINFORMADA", 11, 0.15, 100.0)

    def test_to_dict(self):
        dict_discount = self.desconto.to_dict()
        # Using Assertions to Check Keys
        self.assertIn("taxa", dict_discount)
        self.assertIn("codigo", dict_discount)
        self.assertIn("quantidadeDias", dict_discount)
        self.assertIn("valor", dict_discount)
        # Using Assertions to Check Values
        self.assertEqual(dict_discount["taxa"], 0.15)
        self.assertEqual(dict_discount["codigo"], "VALORFIXODATAINFORMADA")
        self.assertEqual(dict_discount["quantidadeDias"], 11)
        self.assertEqual(dict_discount["valor"], 100)

    def test_to_json(self):
        """Testa se o metodo to_json retorna uma string JSON valida."""
        json_discount = self.desconto.to_json()
        # Verifica se o resultado é uma string
        self.assertIsInstance(json_discount, str)

        # Verifica se a string JSON contém as chaves esperadas
        data = json.loads(json_discount)
        self.assertEqual(data["codigo"], "VALORFIXODATAINFORMADA")
        self.assertEqual(data["quantidadeDias"], 11)
        self.assertEqual(data["taxa"], 0.15)
        self.assertEqual(data["valor"], 100.0)

    def test_from_json(self):
        """Testa se o metodo from_json cria um objeto Discount corretamente."""
        json_discount = self.desconto.to_json()
        new_discount = Desconto.from_json(json_discount)

        # Verifica se o novo objeto é uma instância de Discount
        self.assertIsInstance(new_discount, Desconto)

        # Verifica se os atributos do novo objeto correspondem aos originais
        self.assertEqual(new_discount.codigo, self.desconto.codigo)
        self.assertEqual(new_discount.quantidadeDias, self.desconto.quantidadeDias)
        self.assertEqual(new_discount.taxa, self.desconto.taxa)
        self.assertEqual(new_discount.valor, self.desconto.valor)


if __name__ == "__main__":
    unittest.main()
