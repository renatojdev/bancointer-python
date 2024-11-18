# test_pessoa.py

import json
import unittest

from bancointer.cobranca_v3.models.pessoa import Pessoa
from bancointer.cobranca_v3.models.tipo_pessoa import PersonType


class TestPessoa(unittest.TestCase):
    def setUp(self):
        self.person = Pessoa(
            "12345678901",
            PersonType.FISICA,
            "name person",
            "my address",
            "City",
            "PR",
            80030000,
            "bairro",
            "email@person.com",
            "41",
            "999999999",
            "1234",
            "address complement",
        )

    def test_to_dict(self):
        dict_person = self.person.to_dict()
        # Using Assertions to Check Keys
        self.assertIn("cpfCnpj", dict_person)
        self.assertIn("nome", dict_person)
        self.assertIn("endereco", dict_person)
        self.assertIn("numero", dict_person)
        self.assertIn("complemento", dict_person)
        self.assertIn("bairro", dict_person)
        self.assertIn("cidade", dict_person)
        self.assertIn("uf", dict_person)
        self.assertIn("cep", dict_person)
        self.assertIn("email", dict_person)
        self.assertIn("ddd", dict_person)
        self.assertIn("telefone", dict_person)
        self.assertIn("tipoPessoa", dict_person)
        # Using Assertions to Check Values
        self.assertEqual(dict_person["cpfCnpj"], "12345678901")
        self.assertEqual(dict_person["nome"], "name person")
        self.assertEqual(dict_person["endereco"], "my address")
        self.assertEqual(dict_person["numero"], "1234")
        self.assertEqual(dict_person["complemento"], "address complement")
        self.assertEqual(dict_person["bairro"], "bairro")
        self.assertEqual(dict_person["cidade"], "City")
        self.assertEqual(dict_person["uf"], "PR")
        self.assertEqual(dict_person["cep"], 80030000)
        self.assertEqual(dict_person["email"], "email@person.com")
        self.assertEqual(dict_person["ddd"], "41")
        self.assertEqual(dict_person["telefone"], "9" * 9)
        self.assertEqual(
            dict_person["tipoPessoa"], PersonType.FISICA.get_person_type_name()
        )

    def test_to_json(self):
        """Testa se o metodo to_json retorna uma string JSON valida."""
        json_person = self.person.to_json()
        # Verifica se o resultado é uma string
        self.assertIsInstance(json_person, str)

        # Verifica se a string JSON contém as chaves esperadas
        data = json.loads(json_person)
        self.assertEqual(data["cpfCnpj"], "12345678901")
        self.assertEqual(data["nome"], "name person")
        self.assertEqual(data["endereco"], "my address")
        self.assertEqual(data["numero"], "1234")
        self.assertEqual(data["complemento"], "address complement")
        self.assertEqual(data["bairro"], "bairro")
        self.assertEqual(data["cidade"], "City")
        self.assertEqual(data["uf"], "PR")
        self.assertEqual(data["cep"], 80030000)
        self.assertEqual(data["email"], "email@person.com")
        self.assertEqual(data["ddd"], "41")
        self.assertEqual(data["telefone"], "9" * 9)
        self.assertEqual(data["tipoPessoa"], PersonType.FISICA.get_person_type_name())

    def test_from_json(self):
        """Testa se o metodo from_json cria um objeto Discount corretamente."""
        json_person = self.person.to_json()
        new_person = Pessoa.from_json(json_person)

        # Verifica se o novo objeto é uma instância de Person
        self.assertIsInstance(new_person, Pessoa)

        # Verifica se os atributos do novo objeto correspondem aos originais
        self.assertEqual(new_person.cpfCnpj, self.person.cpfCnpj)
        self.assertEqual(new_person.nome, self.person.nome)
        self.assertEqual(new_person.endereco, self.person.endereco)
        self.assertEqual(new_person.number, self.person.number)
        self.assertEqual(new_person.complement, self.person.complement)
        self.assertEqual(new_person.neighborhood, self.person.neighborhood)
        self.assertEqual(new_person.cidade, self.person.cidade)
        self.assertEqual(new_person.uf, self.person.uf)
        self.assertEqual(new_person.cep, self.person.cep)
        self.assertEqual(new_person.email, self.person.email)
        self.assertEqual(new_person.ddd, self.person.ddd)
        self.assertEqual(new_person.phone, self.person.phone)
        self.assertEqual(
            new_person.tipoPessoa, self.person.tipoPessoa.get_person_type_name()
        )


if __name__ == "__main__":
    unittest.main()
