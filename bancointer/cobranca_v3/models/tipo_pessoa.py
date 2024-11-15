# tipo_pessoa.py

from enum import Enum


class PersonType(Enum):
    FISICA = 1
    JURIDICA = 2

    def get_person_type_name(self):
        return self.name
