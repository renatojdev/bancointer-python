# consulta.py

##############################################################
# THIS EXAMPLE HAS BEEN DEPRECATED. SEE: recuperar_cobranca.py
##############################################################

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

request_code = "1783d19f-ab81-4a54-92a3-a0064f9b26ee"

# Ver recuperar_cobranca.py
response = bi.consulta(codigo_solicitacao=request_code)

print(response)
