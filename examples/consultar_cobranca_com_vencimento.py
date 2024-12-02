# consultar_cobranca_com_vencimento.py


import sys

from decouple import config

from bancointer.pix.cobv.consulta_cobranca_com_vencimento import (
    ConsultaCobrancaComVencimento,
)
from bancointer.utils.environment import Environment

dir_base_ssl = config("SSL_DIR_BASE")
cert = (dir_base_ssl + config("PUBLIC_KEY_V2"), dir_base_ssl + config("PRIVATE_KEY_V2"))
client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")
conta_corrente = config("X_INTER_CONTA_CORRENTE")

# Environment SANDBOX or PRODUCTION
app_env_name = config("APP_ENV")
env = Environment.get_environment_by_value(app_env_name.upper())

# txid
request_txid = "fAfJEWnh6R8ppaJVeLfEaXj0ufn"

args = sys.argv

request_txid_param = None
if len(sys.argv) > 1:
    request_txid_param = args[1]

if request_txid_param is not None:
    request_txid = request_txid_param


consulta_cobv_venc = ConsultaCobrancaComVencimento(
    env, client_id, client_secret, cert, conta_corrente
)

response = consulta_cobv_venc.consultar(request_txid)

print(f"Response from API: {response}")
