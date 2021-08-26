from bancointer.bancointer import BancoInter
from decouple import config


cert = (config("PUBLIC_KEY"), config("PRIVATE_KEY"))

bi = BancoInter(config("CPFCNPJ_BENEF"), config("X-INTER-CONTA-CORRENTE"), cert)

reponse = bi.consulta(nosso_numero="00709421471")

print(reponse['situacao'])

