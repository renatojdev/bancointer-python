# pagar_pix_cobv.py


from decouple import config

from bancointer.pix.cob.paga_pix_cob import PagaPixCobrancaImediata
from bancointer.pix.pix.paga_pix_cobv import PagaPixCobrancaComVencimento
from bancointer.utils.environment import Environment

dir_base_ssl = config("SSL_DIR_BASE")
cert = (dir_base_ssl + config("PUBLIC_KEY_V2"), dir_base_ssl + config("PRIVATE_KEY_V2"))
client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")
conta_corrente = config("X_INTER_CONTA_CORRENTE")

# Environment SANDBOX or PRODUCTION
app_env_name = config("APP_ENV")
env = Environment.get_environment_by_value(app_env_name.upper())

paga_pix_cobv = PagaPixCobrancaComVencimento(
    env, client_id, client_secret, cert, conta_corrente
)

response = paga_pix_cobv.pagar("20.00", "OA3uMSCRI4sgWBaifS6mP2Fnrv8hx3")

print(f"Response from API: {response}")
