# revisar_cobranca_com_vencimento.py


from decouple import config

from bancointer.pix.cobv.revisa_cobranca_com_vencimento import (
    RevisaCobrancaComVencimento,
)
from bancointer.pix.models.calendario import Calendario
from bancointer.pix.models.devedor_recebedor_cobranca import DevedorRecebedorCobranca
from bancointer.pix.models.info_adicional_cobranca_imediata import (
    InfoAdicionalCobrancaImediata,
)
from bancointer.pix.models.solicitacao_cobranca import (
    SolicitacaoCobranca,
)
from bancointer.pix.models.valor_cobranca import (
    ValorCobranca,
    Retirada,
    SaqueOuTroco,
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

# Create immediate cob
calendario = Calendario("2024-12-31")  # default: 3600

devedor_cobranca_imediata = DevedorRecebedorCobranca("João da Silva", cpf="12345678901")

retirada = Retirada(saque=SaqueOuTroco("20.00", "AGPSS", "12345678"))

valor_cobranca_imediata = ValorCobranca("46.17", retirada)

info_adic_cobranca_imediata = InfoAdicionalCobrancaImediata(
    "Campo 1", "Informação Adicional1 do PSP-Recebedor"
)

solicitacao_cob_imediata = SolicitacaoCobranca(
    calendario,
    valor_cobranca_imediata,
    "+5551983334490",
    solicitacaoPagador="Serviço realizado.",
    infoAdicionais=info_adic_cobranca_imediata,
    status="REMOVIDA_PELO_USUARIO_RECEBEDOR",
)

cria_cobranca_com_vencimento = RevisaCobrancaComVencimento(
    env, client_id, client_secret, cert, conta_corrente
)

response = cria_cobranca_com_vencimento.revisar(
    solicitacao_cob_imediata, "dpITRHIPs2S3yDgLNIOaEyZfuSy1RRFg"
)

print(f"Response from API: {response}")
