# consultar_extrato.py

import sys

from decouple import config

from bancointer.banking.extrato import ConsultaExtrato

dir_base_ssl = config("SSL_DIR_BASE")
cert = (dir_base_ssl + config("PUBLIC_KEY_V2"), dir_base_ssl + config("PRIVATE_KEY_V2"))
client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")

consulta_extrato = ConsultaExtrato(client_id, client_secret, cert)

response = consulta_extrato.consultar("2024-05-02", "2024-11-14")

print(f"Response from API: {response}")
