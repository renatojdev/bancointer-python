# consultar_pix.py


from decouple import config

from bancointer.pix.pix.consulta_pix import ConsultaPix
from bancointer.utils.environment import Environment

dir_base_ssl = config("SSL_DIR_BASE")
cert = (dir_base_ssl + config("PUBLIC_KEY_V2"), dir_base_ssl + config("PRIVATE_KEY_V2"))
client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")
conta_corrente = config("X_INTER_CONTA_CORRENTE")

# Environment SANDBOX or PRODUCTION
app_env_name = config("APP_ENV")
env = Environment.get_environment_by_value(app_env_name.upper())

consulta_pix = ConsultaPix(env, client_id, client_secret, cert, conta_corrente)

response = consulta_pix.consultar("E00416968202412061443oJmW8hQsV3b")

print(f"Response from API: {response}")
