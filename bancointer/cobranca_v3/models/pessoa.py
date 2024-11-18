# pessoa.py

import json

from bancointer.cobranca_v3.models.tipo_pessoa import PersonType
from bancointer.utils.exceptions import Erro, BancoInterException


class Pessoa(object):

    def __init__(
        self,
        cpfCnpj,
        tipoPessoa: PersonType,
        nome,
        endereco,
        cidade,
        uf,
        cep,
        bairro="",
        email="",
        ddd="",
        telefone="",
        numero="",
        complemento="",
        *args,
        **kwargs,
    ):
        self.cpfCnpj = cpfCnpj
        self.nome = nome
        self.endereco = endereco
        self.number = numero
        self.complement = complemento
        self.neighborhood = bairro
        self.cidade = cidade
        self.uf = uf
        self.email = email
        self.phone = telefone
        self.cep = cep
        self.ddd = ddd
        self.tipoPessoa = tipoPessoa

    def __eq__(self, other):
        if not isinstance(other, Pessoa):
            return NotImplemented
        return self.cpfCnpj == other.cpfCnpj and self.nome == other.nome

    def to_dict(self):
        required_fields = [
            "cpfCnpj",
            "tipoPessoa",
            "nome",
            "endereco",
            "cidade",
            "uf",
            "cep",
        ]
        for campo in required_fields:
            if not hasattr(self, campo) or getattr(self, campo) is None:
                erro = Erro(404, f"O atributo 'pessoa.{campo}' é obrigatório.")
                raise BancoInterException("Ocorreu um erro no SDK", erro)

        return {
            "cpfCnpj": self.cpfCnpj,
            "nome": self.nome,
            "endereco": self.endereco,
            "numero": self.number,
            "complemento": self.complement,
            "bairro": self.neighborhood,
            "cidade": self.cidade,
            "uf": self.uf,
            "email": self.email,
            "telefone": self.phone,
            "cep": self.cep,
            "ddd": self.ddd,
            "tipoPessoa": self.tipoPessoa.get_person_type_name(),
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(json_person):
        data = json.loads(json_person)
        return Pessoa(**data)
