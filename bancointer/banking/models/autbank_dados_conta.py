# autbank_dados_conta.py


from dataclasses import dataclass


@dataclass()
class AutbankDadosConta(object):
    codIspb: str
    codAgencia: str
    nroConta: str
    cpfCnpj: str
    nome: str
    tipoConta: str
