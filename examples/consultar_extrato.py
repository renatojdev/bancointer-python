# consultar_extrato.py

from decouple import config

from bancointer.banking.extrato import ConsultaExtrato
from bancointer.utils.ambient import Ambient

dir_base_ssl = config("SSL_DIR_BASE")
cert = (dir_base_ssl + config("PUBLIC_KEY_V2"), dir_base_ssl + config("PRIVATE_KEY_V2"))
client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")

consulta_extrato = ConsultaExtrato(Ambient.SANDBOX, client_id, client_secret, cert)

response = consulta_extrato.consultar("2024-11-04", "2024-11-14")

print(f"Response from API: {response}")
