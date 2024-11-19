import re


@classmethod
class BancoInterValidations(object):

    @staticmethod
    def validate_txid(txid):
        if re.match(r'^[a-zA-Z0-9]{26,35}$', txid):
            return True
        return False

    @staticmethod
    def validate_x_id_idempotente(id_idempotente):
        if re.match(
            r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
            id_idempotente
        ):
            return True
        return False

    @staticmethod
    def validate_x_conta_corrente(conta):
        if re.match(r"^[1-9][0-9]*$", conta):
            return True
        return False

    @staticmethod
    def validate_cpf_cnpj(cpf_cnpj):
        if re.match(r"^[0-9]{11}$|^[0-9]{14}$", cpf_cnpj):
            return True
        return False

    @staticmethod
    def validate_phone_number(number):
        if re.match(r"^\+?2?\d{9,15}$", number):
            return True
        return False
