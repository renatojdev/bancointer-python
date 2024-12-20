# recuperar_cobranca_pdf.py

import sys

from decouple import config

from bancointer.cobranca_v3.cobranca import RecuperaCobrancaPDF
from bancointer.utils.environment import Environment

dir_base_ssl = config("SSL_DIR_BASE")
cert = (dir_base_ssl + config("PUBLIC_KEY_V2"), dir_base_ssl + config("PRIVATE_KEY_V2"))
client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")
conta_corrente = config("X_INTER_CONTA_CORRENTE")

# Environment SANDBOX or PRODUCTION
app_env_name = config("APP_ENV")
env = Environment.get_environment_by_value(app_env_name.upper())

request_code = "1783d19f-ab81-4a54-92a3-a0064f9b26ee"

args = sys.argv

request_code_param = None
if len(sys.argv) > 1:
    request_code_param = args[1]

if request_code_param is not None:
    request_code = request_code_param

recupera_cobranca = RecuperaCobrancaPDF(
    env, client_id, client_secret, cert, conta_corrente
)

# response = recupera_cobranca.recuperar_pdf(request_code) # download to /tmp
response = recupera_cobranca.recuperar_pdf(request_code, config("DOWNLOAD_PATH"))

print(response)
