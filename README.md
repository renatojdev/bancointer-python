#  Banco Inter Python
Este projeto utiliza a API do Banco Inter PJ de boletos registrados.

    [Portal do desenvolvedor](https://developers.bancointer.com.br/)
    [Refrência da API](https://developers.bancointer.com.br/reference)

##  Funcionalidades disponíveis
* Emissão de boletos
* Download de boletos
* Baixa de boletos

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
"cnpjCpf": "53982619599",
"nome": "JOAO DA SILVA",
"email": "email@pagador.com",
"telefone": "999999999",
"cep": "99999999",
"numero": "999",
"complemento": "",
"bairro": "BAIRRO",
"endereco": "ENDERECO",
"cidade": "CIDADE",
"uf": "PR",
"ddd": "99",
"tipoPessoa": "FISICA"
}
mensagem = {
"linha1": "linha1",
"linha2": "linha2",
"linha3": "linha3",
"linha4": "linha4",
"linha5": "linha5",
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