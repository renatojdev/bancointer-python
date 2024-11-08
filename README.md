#  Banco Inter Python
Este projeto consome a API do Banco Inter PJ de boletos registrados. Para acesso a documentação precisa estar logado no internet banking do Banco Inter. Para criar seu aplicativo, siga estas etapas simples:

* Faça login no Internet Banking (Banco Inter).
* Navegue até a seção APIs:
* Conta Digital > Aplicações > <em>**Nova Aplicação**</em>

**Atualizado para a API versão 3**

* Crie um arquivo `.env` com os seguitntes atributos na aplicação que irá usar este projeto.

```
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
from bancointer.bancointer import BancoInter
from decouple import config

dir_base_ssl = config("SSL_DIR_BASE")

# Objeto Banco Inter para operações na API
bi = BancoInter(
    config("API_SBX_COBRA_V3"),
    config("API_SBX_TOKEN_V2"),
    config("CLIENT_ID"),
    config("CLIENT_SECRET"),
    (dir_base_ssl + config("PUBLIC_KEY_V2"), dir_base_ssl + config("PRIVATE_KEY_V2")),
)
```

###  Emissão de Boleto
```
pagador = {
"cnpjCpf": "99999999999999",
"nome": "Nome do Pagador",
"email": "email@pagador.com",
"telefone": "999999999",
"cep": "99999999",
"numero": "999",
"complemento": "",
"bairro": "Bairro do Pagador",
"endereco": "Endereço do Pagador",
"cidade": "Cidade do Pagador",
"uf": "PR",
"ddd": "99",
"tipoPessoa": "FISICA"
}
mensagem = {
"linha1": "Mensagem da linha1",
"linha2": "Mensagem da linha2",
"linha3": "Mensagem da linha3",
"linha4": "Mensagem da linha4",
"linha5": "Mensagem da linha5",
}

reponse = bi.boleto(pagador=pagador, mensagem=mensagem, dataEmissao=None, dataVencimento="2024-11-21", seuNumero="00001", valorNominal=2.5)

print(reponse)
```
### Download de Boleto
```
reponse = bi.download(codigo_solicitacao="ea209b84-2625-42fe-b6d5-820b496d4cc1", download_path=config("DOWNLOAD_PATH"))

print(reponse)
```
### Baixa de Boleto
```
reponse = bi.baixa(codigo_solicitacao="ea209b84-2625-42fe-b6d5-820b496d4cc1", motivo=Baixa.ACERTOS)

print(reponse)
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