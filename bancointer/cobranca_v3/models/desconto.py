# desconto.py

import json
from json import JSONEncoder


class Desconto(object):
    def __init__(self, codigo, quantidadeDias, taxa, valor):
        self.codigo = codigo
        self.quantidadeDias = quantidadeDias
        self.taxa = taxa
        self.valor = valor

    def __eq__(self, other):
        if not isinstance(other, Desconto):
            return NotImplemented
        return (
            self.codigo == other.codigo
            and self.quantidadeDias == other.quantidadeDias
            and self.taxa == other.taxa
            and self.valor == other.valor
        )

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "taxa": self.taxa,
            "quantidadeDias": self.quantidadeDias,
            "valor": self.valor,
        }

    def to_json(self):
        return json.dumps(self, cls=DescontoEncoder)

    @staticmethod
    def from_json(json_discount):
        data = json.loads(json_discount)
        return Desconto(**data)


class DescontoEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
