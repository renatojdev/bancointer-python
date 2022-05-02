from bancointer.bancointer import BancoInter
from bancointer.baixa import Baixa
from decouple import config


API_VERSION = 2
dir_base_ssl = config("SSL_DIR_BASE")

cert = (dir_base_ssl + config("PUBLIC_KEY_V"+ str(API_VERSION)), dir_base_ssl + config("PRIVATE_KEY_V"+ str(API_VERSION)))

bi = BancoInter(config("CPFCNPJ_BENEF"), config("X-INTER-CONTA-CORRENTE"), cert)

if API_VERSION == 1:
    bi.set_api_version(API_VERSION)

reponse = bi.baixa(nosso_numero="00813028679", motivo=Baixa.ACERTOS)

print(reponse)
