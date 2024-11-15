# multa.py

import json
from json import JSONEncoder
from numbers import Number


class Multa(object):
    def __init__(self, codigo, taxa, valor):
        self.codigo: str = codigo
        self.taxa: str = taxa
        self.valor: Number = valor

    def __eq__(self, other):
        if not isinstance(other, Multa):
            return NotImplemented
        return (
            self.codigo == other.codigo
            and self.taxa == other.taxa
            and self.valor == other.valor
        )

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "valor": self.valor,
            "taxa": self.taxa,
        }

    def to_json(self):
        return json.dumps(self, cls=MultaEncoder)

    @staticmethod
    def from_json(json_multa):
        data = json.loads(json_multa)
        return Multa(**data)


class MultaEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
