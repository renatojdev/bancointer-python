# pix.py

import json
from json import JSONEncoder


class Pix(object):
    def __init__(self, txid, pixCopiaECola):
        self.txid = txid
        self.pixCopiaECola = pixCopiaECola

    def __eq__(self, other):
        if not isinstance(other, Pix):
            return NotImplemented
        return self.txid == other.txid

    def to_dict(self):
        return {"txid": self.txid, "pixCopiaECola": self.pixCopiaECola}

    def to_json(self):
        return json.dumps(self, cls=PixEncoder)

    @staticmethod
    def from_json(json_discount):
        data = json.loads(json_discount)
        return Pix(**data)


class PixEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
