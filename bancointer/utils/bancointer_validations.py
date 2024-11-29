# bancointer_validations.py


import re


class BancoInterValidations(object):

    @staticmethod
    def validate_txid(txid):
        if txid is not None and isinstance(txid, str) and txid is not "":
            if re.match(r"^[a-zA-Z0-9]{26,35}$", txid):
                return True
        return False

    @staticmethod
    def validate_x_id_idempotente(id_idempotente):
        if re.match(
            r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
            id_idempotente,
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
        if re.match(r"^[0-9]{11}$|^[0-9]{14}$|^[0-9]{18}$", cpf_cnpj):
            return True
        return False

    @staticmethod
    def validate_phone_number(number):
        if re.match(r"^\+?2?\d{9,15}$", number):
            return True
        return False

    @staticmethod
    def validate_date(date):
        # Pattern YYYY-MM-DD
        if re.match(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$", date):
            return True
        else:
            return False

    @staticmethod
    def is_valid_num_dias_agenda(num_dias_agenda):
        return isinstance(num_dias_agenda, int) and 0 <= num_dias_agenda <= 60

    @staticmethod
    def is_valid_valor_nominal(numero):
        if isinstance(numero, str):
            numero = float(numero)
        if isinstance(numero, float):
            if 2.5 <= numero <= 99999999.99:
                return True
            else:
                return False
        return False

    @staticmethod
    def validate_string_range(s, min_chars=1, max_chars=100):
        padrao = rf"^.{{{min_chars},{max_chars}}}$"

        if re.match(padrao, s):
            return True
        else:
            return False

    @staticmethod
    def validate_transaction_code(transaction_code):
        # Pattern [0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}
        if (
            transaction_code is not None
            and isinstance(transaction_code, str)
            and transaction_code is not ""
        ):
            if re.match(
                r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
                transaction_code,
            ):
                return True
        return False

    @staticmethod
    def validate_pix_chave(chave):
        """
        Valida tipo de chaves PIX. Exemplos de tipos: Se email: email do recebedor (ex: fulano.da.silva@example.com)
        Se CPF/CNPJ: 12345678900 / 00038166000105 Se número do telefone celular: +55DD9XXXXXXXX (formato internacional)
        Se EVP: 123e4567-e12b-12d1-a456-426655440000
        """
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        cpf_regex = r"^\d{3}\.\d{3}\.\d{3}-\d{2}$|^\d{11}$"
        cnpj_regex = r"^\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}$|^\d{14}$"
        telefone_regex = r"^\+55\d{2}9\d{8}$"
        evp_regex = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"

        pattern = (
            rf"({email_regex}|{cpf_regex}|{cnpj_regex}|{telefone_regex}|{evp_regex})"
        )

        if re.match(pattern, chave):
            return True
        else:
            return False
