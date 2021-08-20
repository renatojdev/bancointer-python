from bancointer.bancointer import BancoInter
from bancointer.baixa import Baixa
from decouple import config


cert=(config("PUBLIC_KEY"), config("PRIVATE_KEY"))

bi = BancoInter(
    config("CPFCNPJ_BENEF"),
    config("X-INTER-CONTA-CORRENTE"), cert)

reponse = bi.baixa(nosso_numero="00714656116", motivo=Baixa.ACERTOS)

print(reponse)