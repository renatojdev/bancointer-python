# constants.py

"""Arquivo para armazenar constantes utilizadas na aplicação."""

# SANDBOX
HOST_SANDBOX = "cdpj-sandbox.partners.uatinter.co"
URL_BASE_SANDBOX = "https://cdpj-sandbox.partners.uatinter.co"

# Host and URL Base
HOST = "cdpj.partners.bancointer.com.br"
URL_BASE = "https://cdpj.partners.bancointer.com.br"


# Documentação do Certificado
DOC_CERTIFICADO = (
    "https://developers.bancointer.com.br/v4/docs/onde-obter-o-certificado"
)

# URLs de Autenticação
URL_TOKEN = f"{URL_BASE}/oauth/v2/token"

# URLs de Banking
URL_BANKING = f"{URL_BASE}/banking/v2"
URL_BANKING_SALDO = f"{URL_BANKING}/saldo"
URL_BANKING_EXTRATO = f"{URL_BANKING}/extrato"
URL_BANKING_EXTRATO_ENRIQUECIDO = f"{URL_BANKING_EXTRATO}/completo"
URL_BANKING_EXTRATO_PDF = f"{URL_BANKING_EXTRATO}/exportar"
URL_BANKING_PAGAMENTO = f"{URL_BANKING}/pagamento"
URL_BANKING_PAGAMENTO_DARF = f"{URL_BANKING_PAGAMENTO}/darf"
URL_BANKING_PAGAMENTO_LOTE = f"{URL_BANKING_PAGAMENTO}/lote"
URL_BANKING_PAGAMENTO_PIX = f"{URL_BANKING_PAGAMENTO}/pix"
URL_BANKING_TED = f"{URL_BANKING}/ted"
URL_BANKING_WEBHOOK = f"{URL_BANKING}/webhooks"

# URLs de PIX
URL_PIX = f"{URL_BASE}/pix/v2"
URL_PIX_PIX = f"{URL_PIX}/pix"
URL_PIX_LOCATIONS = f"{URL_PIX}/loc"
URL_PIX_COBRANCAS_IMEDIATAS = f"{URL_PIX}/cob"
URL_PIX_COBRANCA_COM_VENCIMENTO = f"{URL_PIX}/cobv"
URL_PIX_WEBHOOK = f"{URL_PIX}/webhook"
URL_PIX_WEBHOOK_CALLBACKS = f"{URL_PIX_WEBHOOK}/callbacks"

# URLs de Boletos
URL_BOLETOS = f"{URL_BASE}/cobranca/v2/boletos"
URL_BOLETOS_SUMARIO = f"{URL_BOLETOS}/sumario"
URL_BOLETOS_WEBHOOK = f"{URL_BOLETOS}/webhook"
URL_BOLETOS_WEBHOOK_CALLBACKS = f"{URL_BOLETOS_WEBHOOK}/callbacks"

# URLs de Cobranças
URL_COBRANCAS = f"{URL_BASE}/cobranca/v3/cobrancas"
URL_COBRANCAS_SUMARIO = f"{URL_COBRANCAS}/sumario"
URL_COBRANCAS_WEBHOOK = f"{URL_COBRANCAS}/webhook"
URL_COBRANCAS_WEBHOOK_CALLBACKS = f"{URL_COBRANCAS_WEBHOOK}/callbacks"

# PATHS
PATH_TOKEN = f"/oauth/v2/token"
PATH_COBRANCAS = f"/cobranca/v3/cobrancas"
PATH_EXTRATO = f"/banking/v2/extrato"

# Escopos
ESCOPO_BOLETO_COBRANCA_READ = "boleto-cobranca.read"
ESCOPO_BOLETO_COBRANCA_WRITE = "boleto-cobranca.write"

ESCOPO_EXTRATO_READ = "extrato.read"
ESCOPO_PAGAMENTO_BOLETO_READ = "pagamento-boleto.read"
ESCOPO_PAGAMENTO_BOLETO_WRITE = "pagamento-boleto.write"
ESCOPO_PAGAMENTO_DARF_WRITE = "pagamento-darf.write"

ESCOPO_PAGAMENTOS_LOTE_READ = "pagamento-lote.read"
ESCOPO_PAGAMENTOS_LOTE_WRITE = "pagamento-lote.write"

ESCOPO_PAGAMENTO_PIX_WRITE = "pagamento-pix.write"

ESCOPO_BANKING_WEBHOOK_BANKING_READ = "webhook-banking.read"
ESCOPO_BANKING_WEBHOOK_BANKING_WRITE = "webhook-banking.write"

ESCOPO_PIX_COB_READ = "cob.read"
ESCOPO_PIX_COB_WRITE = "cob.write"

ESCOPO_PIX_COBV_READ = "cobv.read"
ESCOPO_PIX_COBV_WRITE = "cobv.write"

ESCOPO_PIX_PIX_READ = "pix.read"
ESCOPO_PIX_PIX_WRITE = "pix.write"

ESCOPO_PIX_LOCATION_READ = "payloadlocation.read"
ESCOPO_PIX_LOCATION_WRITE = "payloadlocation.write"

ESCOPO_PIX_WEBHOOK_READ = "webhook.read"
ESCOPO_PIX_WEBHOOK_WRITE = "webhook.write"

# Outras Constantes
DAYS_TO_EXPIRE = 30

CERTIFICATE_EXCEPTION_MESSAGE = "Erro no Certificado!"
GENERIC_EXCEPTION_MESSAGE = "Erro durante execução do SDK!"
