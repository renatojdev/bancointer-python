# mora.py

import json
from json import JSONEncoder
from numbers import Number


class Mora(object):
    def __init__(self, codigo: str, valor: Number, taxa: Number, *args, **kwargs):
        self.codigo = codigo
        self.valor = valor
        self.taxa = taxa

    def __eq__(self, other):
        if not isinstance(other, Mora):
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
        return json.dumps(self, cls=MoraEncodigor)

    @staticmethod
    def from_json(json_discount):
        data = json.loads(json_discount)
        return Mora(**data)


class MoraEncodigor(JSONEncoder):
    def default(self, o):
        return o.__dict__
