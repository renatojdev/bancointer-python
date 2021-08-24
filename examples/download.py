from bancointer.bancointer import BancoInter
from decouple import config


cert = (config("PUBLIC_KEY"), config("PRIVATE_KEY"))

bi = BancoInter(config("CPFCNPJ_BENEF"), config("X-INTER-CONTA-CORRENTE"), cert)

reponse = bi.download(nosso_numero="00714151811", download_path=config("DOWNLOAD_PATH"))

print(reponse)
