# recupera_cobranca.py

import sys

from decouple import config

from bancointer.cobranca_v3.cobranca.recupera_cobranca import RecuperaCobranca

dir_base_ssl = config("SSL_DIR_BASE")
cert = (dir_base_ssl + config("PUBLIC_KEY_V2"), dir_base_ssl + config("PRIVATE_KEY_V2"))
client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")

request_code = "1783d19f-ab81-4a54-92a3-a0064f9b26ee"

args = sys.argv

request_code_param = None
if len(sys.argv) > 1:
    request_code_param = args[1]

if request_code_param is not None:
    request_code = request_code_param

recupera_cobranca = RecuperaCobranca(client_id, client_secret, cert)

response = recupera_cobranca.recuperar(request_code)

print(f"Response from API: {response}")