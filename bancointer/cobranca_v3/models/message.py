# message.py

import json
from json import JSONEncoder


class Message(object):
    def __init__(self, linha1, linha2, linha3, linha4, linha5):
        self.linha1 = linha1
        self.linha2 = linha2
        self.linha3 = linha3
        self.linha4 = linha4
        self.linha5 = linha5

    def __eq__(self, other):
        if not isinstance(other, Message):
            return NotImplemented
        return (
            self.linha1 == other.linha1
            and self.linha2 == other.linha2
            and self.linha3 == other.linha3
            and self.linha4 == other.linha4
            and self.linha5 == other.linha5
        )

    def to_dict(self):
        return {
            "linha1": self.linha1,
            "linha2": self.linha2,
            "linha3": self.linha3,
            "linha4": self.linha4,
            "linha5": self.linha5,
        }

    def to_json(self):
        return json.dumps(self, cls=MessageEncoder)

    @staticmethod
    def from_json(json_message):
        data = json.loads(json_message)
        return Message(**data)


class MessageEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
