#  Banco Inter Python
Este projeto consome a API do Banco Inter PJ de boletos registrados. Para acesso a documentação precisa estar logado no internet banking do Banco Inter. Para criar seu aplicativo, siga estas etapas simples:

* Faça login no Internet Banking (Banco Inter).
* Navegue até a seção APIs:
* Conta Digital > Aplicações > <em>**Nova Aplicação**</em>

**Atualizado para a API versão 3**

* Crie um arquivo `.env` com os seguitntes atributos na aplicação que irá usar este projeto.

```
    # Application Environment - SANDBOX or PRODUCTION
    APP_ENV=SANDBOX
    CPFCNPJ_BENEF='Número CPF OU CNPJ da conta no banco inter'
    X_INTER_CONTA_CORRENTE='Numero da conta corrente'
    # SANDBOX
    API_SBX_TOKEN_V2=https://cdpj-sandbox.partners.uatinter.co/oauth/v2/token
    API_SBX_COBRA_V3=https://cdpj-sandbox.partners.uatinter.co/cobranca/v3/
    # PRODUCTION
    API_URL_TOKEN_V2=https://cdpj.partners.bancointer.com.br/oauth/v2/token
    API_URL_COBRA_V3=https://cdpj.partners.bancointer.com.br/cobranca/v3/
    API_URL_COBRA_V2=https://cdpj.partners.bancointer.com.br/cobranca/v2/
    API_URL_COBRA_V1=https://apis.bancointer.com.br/openbanking/v1/certificado/
    SSL_DIR_BASE='Diretorio base dos arquivos SSL'
    PUBLIC_KEY_V1='Path do arquivo public key da versão 1'
    PRIVATE_KEY_V1='Path do Arquivo private key da versão 1'
    PUBLIC_KEY_V2='Path do arquivo public key da versão 2'
    PRIVATE_KEY_V2='Path do Arquivo private key da versão 2'
    DOWNLOAD_PATH='Path do diretorio que os arquivos PDF de download serão salvos'
    CLIENT_ID='Chave client id da sua app no banco inter'
    CLIENT_SECRET='Chave client secret da sua app no banco inter'
```

**Referências:**

* Portal do desenvolvedor: https://developers.inter.co/
* Referência da API: https://developers.inter.co/references/token

##  Funcionalidades disponíveis
    * API Cobrança (Boleto com Pix)
        - Emissão de boletos
        - Download de boletos
        - Baixa de boletos
        - Consulta detalhada de boletos

###  Novas funcionalidades a serem implementadas
    * Recursos da Api Banking
        * Extrato
            - Consultar extrato
    * Recursos da Api Pix

##  Instalação para utilização

```pip install bancointer-python```

ou

```python setup.py install```

##  Exemplos de Uso
Exemplos de utilização da API do Banco Inter (SANDBOX) para emissão, download e baixa de títulos bancários. Veja a pasta `examples/`.

- Importe as dependências necessárias:

```
from decouple import config

dir_base_ssl = config("SSL_DIR_BASE")

# Objeto Banco Inter para operações na API
dir_base_ssl = config("SSL_DIR_BASE")
cert = (dir_base_ssl + config("PUBLIC_KEY_V2"), dir_base_ssl + config("PRIVATE_KEY_V2"))
client_id = config("CLIENT_ID")
client_secret = config("CLIENT_SECRET")

# Environment SANDBOX or PRODUCTION
app_env_name = config("APP_ENV")
env = Environment.get_environment_by_value(app_env_name.upper())
```

###  Emissão de Boleto
```
payer = Pessoa(
    "9" * 11,  # valido
    PersonType.FISICA,
    "NOME DO PAGADOR",
    "ENDERECO DO PAGADOR",
    "CIDADE DO PAGADOR",
    "PR",
    "80030000",
)  # OU FISICA
# Pagador

discount = Desconto("PERCENTUALDATAINFORMADA", 0, 1.2, 2)
multa = Multa("VALORFIXO", 0, 100)
mora = Mora("TAXAMENSAL", 0, 4.5)
message = Message("message 1", "message 2", "message 3", "", "message 5")

# Beneficiario final, mesmo que o pagador
beneficiario_final = Pessoa(
    "12345678901",
    PersonType.FISICA,
    "Nome do beneficiário",
    "Avenida Brasil, 1200",
    "Belo Horizonte",
    "MG",
    "30110000",
)

cobranca = Cobranca.criar_sobranca_simples("0001", 2.5, "2024-11-22", payer)
cobranca.multa = multa
cobranca.desconto = discount
cobranca.beneficiarioFinal = beneficiario_final

sol_new_cobranca = SolicitacaoEmitirCobranca(cobranca)

emite_cobranca = EmiteCobranca(env, client_id, client_secret, cert)
resposta = emite_cobranca.emitir(sol_new_cobranca)

print(resposta)
```
### Consultar dados do Boleto
```
request_code = "1783d19f-ab81-4a54-92a3-a0064f9b26ee"

recupera_cobranca = RecuperaCobranca(env, client_id, client_secret, cert)

response = recupera_cobranca.recuperar(request_code)
```
### Download de Boleto
```
request_code = "1783d19f-ab81-4a54-92a3-a0064f9b26ee"

recupera_cobranca = RecuperaCobrancaPDF(env, client_id, client_secret, cert)

response = recupera_cobranca.recuperar_pdf(request_code, config("DOWNLOAD_PATH"))
```
### Baixa de Boleto
```
request_code = "1783d19f-ab81-4a54-92a3-a0064f9b26ee"

cancela_cobranca = CancelaCobranca(env, client_id, client_secret, cert)

response = cancela_cobranca.cancelar(request_code, Baixa.ACERTOS.value)
```
## Contribua com este projeto

Clone o repositório do projeto

> $ git clone https://github.com/renatojdev/bancointer-python.git

Se não tiver o pipenv instalado, para instalar:
> $ pip install -U pipenv

Instale as dependências
> $ make install


## Dependências

- [Python 3.7+](https://www.python.org/downloads/release/python-374/)
- [Pipenv](https://github.com/kennethreitz/pipenv)

## Licença

[MIT](http://en.wikipedia.org/wiki/MIT_License)