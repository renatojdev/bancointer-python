# consultar_saldo.py

from decouple import config

from bancointer.banking.saldo import ConsultaSaldo
from bancointer.utils.environment import Environment

dir_base_ssl = config("SSL_DIR_BASE")
cert = (dir_base_ssl + config("PUBLIC_KEY_V2"), dir_base_ssl + config("PRIVATE_KEY_V2"))
client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")

# Environment SANDBOX or PRODUCTION
app_env_name = config("APP_ENV")
env = Environment.get_environment_by_value(app_env_name.upper())

consulta_saldo = ConsultaSaldo(env, client_id, client_secret, cert)

response = consulta_saldo.consultar("2024-11-18")

print(f"Response from API: {response}")
