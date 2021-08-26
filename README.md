#  Banco Inter Python
Este projeto consome a API do Banco Inter PJ de boletos registrados. Para acesso a documentação precisa estar logado no internet banking do Banco Inter. Para criar seu aplicativo, siga estas etapas simples:

* Faça login no Internet Banking (Banco Inter).
* Navegue até a seção APIs:
* Conta Digital > Aplicações > <em>**Nova Aplicação**</em>

**Referências:**

* Portal do desenvolvedor: https://developers.bancointer.com.br/
* Refrência da API: https://developers.bancointer.com.br/reference

##  Funcionalidades disponíveis
* Emissão de boletos
* Download de boletos
* Baixa de boletos
* Consulta detalhada de boletos através do nosso número

##  Instalação para utilização

```pip install bancointer-python```

ou

```python setup.py install```

##  Exemplos de Uso
Exemplos de utilização da API do Banco Inter para emissão, download e baixa de títulos bancários.

###  Emissão de Boleto
```
bi = BancoInter(
config("CPFCNPJ_BENEF"),
config("X-INTER-CONTA-CORRENTE"), cert)

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

reponse = bi.boleto(pagador=pagador, mensagem=mensagem, dataEmissao="2021-08-19", dataVencimento="2021-08-23", seuNumero="00001", valorNominal=9.9)

print(reponse)
```
### Download de Boleto
```
bi = BancoInter(
config("CPFCNPJ_BENEF"),
config("X-INTER-CONTA-CORRENTE"), cert)

reponse = bi.download(nosso_numero="00714151811", download_path=config("DOWNLOAD_PATH"))

print(reponse)
```
### Baixa de Boleto
```
bi = BancoInter(
config("CPFCNPJ_BENEF"),
config("X-INTER-CONTA-CORRENTE"), cert)

reponse = bi.baixa(nosso_numero="00714656116", motivo=Baixa.ACERTOS)

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