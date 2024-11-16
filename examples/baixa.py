# baixa.py

#############################################################
# THIS EXAMPLE HAS BEEN DEPRECATED. SEE: cancelar_cobranca.py
#############################################################

from bancointer.bancointer import BancoInter
from bancointer.cobranca_v3.models.tipo_baixa import TipoBaixa
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

# Ver cancelar_cobranca.py

reponse = bi.baixa(codigo_solicitacao=request_code, motivo_cancelamento=TipoBaixa.ACERTOS)

print(reponse)
