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

request_code = "09a0024a-836f-49ff-a9e5-a4c2c256ab0d"

response = bi.consulta(codigo_solicitacao=request_code)

print(response)
