# boleto.py

import json
from json import JSONEncoder


class Boleto(object):
    def __init__(self, nossoNumero, codigoBarras, linhaDigitavel):
        self.nossoNumero = nossoNumero
        self.codigoBarras = codigoBarras
        self.linhaDigitavel = linhaDigitavel

    def __eq__(self, other):
        if not isinstance(other, Boleto):
            return NotImplemented
        return (
            self.nossoNumero == other.nossoNumero
            and self.codigoBarras == other.codigoBarras
        )

    def to_dict(self):
        return {
            "nossoNumero": self.nossoNumero,
            "codigoBarras": self.codigoBarras,
            "linhaDigitavel": self.linhaDigitavel,
        }

    def to_json(self):
        return json.dumps(self, cls=BoletoEncoder)

    @staticmethod
    def from_json(json_discount):
        data = json.loads(json_discount)
        return Boleto(**data)


class BoletoEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
