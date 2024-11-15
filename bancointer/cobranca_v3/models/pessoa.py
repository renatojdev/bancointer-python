# pessoa.py

import json

from bancointer.cobranca_v3.models.tipo_pessoa import PersonType


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
        **kwargs
    ):
        self.cpf_cnpj = cpfCnpj
        self.name = nome
        self.address = endereco
        self.number = numero
        self.complement = complemento
        self.neighborhood = bairro
        self.city = cidade
        self.uf = uf
        self.email = email
        self.phone = telefone
        self.zipCode = cep
        self.ddd = ddd
        self.person_type = tipoPessoa

    def __eq__(self, other):
        if not isinstance(other, Pessoa):
            return NotImplemented
        return self.cpf_cnpj == other.cpf_cnpj and self.name == other.name

    def to_dict(self):
        return {
            "cpfCnpj": self.cpf_cnpj,
            "nome": self.name,
            "endereco": self.address,
            "numero": self.number,
            "complemento": self.complement,
            "bairro": self.neighborhood,
            "cidade": self.city,
            "uf": self.uf,
            "email": self.email,
            "telefone": self.phone,
            "cep": self.zipCode,
            "ddd": self.ddd,
            "tipoPessoa": self.person_type.get_person_type_name(),
        }

    def to_json(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json(json_person):
        data = json.loads(json_person)
        return Pessoa(**data)
