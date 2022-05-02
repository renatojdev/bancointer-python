from bancointer.bancointer import BancoInter
from decouple import config


API_VERSION = 2
dir_base_ssl = config("SSL_DIR_BASE")

cert = (dir_base_ssl + config("PUBLIC_KEY_V"+ str(API_VERSION)), dir_base_ssl + config("PRIVATE_KEY_V"+ str(API_VERSION)))

bi = BancoInter(config("CPFCNPJ_BENEF"), config("X-INTER-CONTA-CORRENTE"), cert)

if API_VERSION == 1:
    bi.set_api_version(API_VERSION)

reponse = bi.download(nosso_numero="00813029727", download_path=config("DOWNLOAD_PATH"))

print(reponse)
