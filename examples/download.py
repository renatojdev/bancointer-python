# download.py

##################################################################
# THIS EXAMPLE HAS BEEN DEPRECATED. SEE: recuperar_cobranca_pdf.py
##################################################################

from bancointer.bancointer import BancoInter
from decouple import config


dir_base_ssl = config("SSL_DIR_BASE")

bi = BancoInter(
    config("API_SBX_COBRA_V3"),
    config("API_SBX_TOKEN_V2"),
    config("CLIENT_ID"),
    config("CLIENT_SECRET"),
    (dir_base_ssl + config("PUBLIC_KEY_V2"), dir_base_ssl + config("PRIVATE_KEY_V2")),
)

request_code = "ea209b84-2625-42fe-b6d5-820b496d4cc1"

# Ver recuperar_cobranca_pdf.py

response = bi.download(
    codigo_solicitacao=request_code, download_path=config("DOWNLOAD_PATH")
)

print(response)
