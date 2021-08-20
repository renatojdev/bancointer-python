from bancointer.bancointer import BancoInter
from decouple import config


cert=(config("PUBLIC_KEY"), config("PRIVATE_KEY"))

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

MULTA = {
    "codigoMulta": "PERCENTUAL ",
    "valor": 2.0,
    "taxa": 0
}

MORA = {
    "codigoMora": "TAXAMENSAL",
    "valor": 0,
    "taxa": 1.0
}

bi.set_multa(multa=MULTA)

bi.set_mora(mora=MORA)

reponse = bi.boleto(pagador=pagador, mensagem=mensagem, dataEmissao="2021-08-19", dataVencimento="2021-08-26", seuNumero="00001", valorNominal=9.9)

print(reponse)