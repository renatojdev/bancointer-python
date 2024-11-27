# aut_bank_erro.py


from dataclasses import dataclass


@dataclass()
class AutbankErro(object):
    codigoErro: str
    descricacaoErro: str
    codigoErroComplementar: str
