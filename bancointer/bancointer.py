import os
import requests
import codecs
from .baixa import Baixa
from .util import Util
import json
from pathlib import Path
from datetime import datetime, timedelta

class BancoInter(object):
    """Classe para transacoes (emissao, baixa, download) de boletos na API do Banco Inter PJ.
       Na emissao de boletos o padrao inicial e sem desconto, multa e juros de mora.
    """

    # Class attributes
    _SEM_DESCONTO = {
        "codigoDesconto": "NAOTEMDESCONTO",
        "taxa": 0,
        "valor": 0,
        "data": "",
    }
    _ISENTO_MULTA = {"codigoMulta": "NAOTEMMULTA", "valor": 0, "taxa": 0}
    _ISENTO_MORA = {"codigoMora": "ISENTO", "valor": 0, "taxa": 0}

    def __init__(self, base_url, base_url_token, client_id, client_secret, cert):
        """Metodo construtor da classe.

        Args:
            cpf_cnpj_beneficiario (str): cpf/cnpj do beneficiario do boleto
            x_inter_conta_corrente (str): numero da conta corrente do beneficiario do boleto.
            cert (tuple): (cert_file_path, key_file_path) PEM path do certificado digital e PEM path da chave publica.
        """
        self.desconto1 = self._SEM_DESCONTO
        self.desconto2 = self._SEM_DESCONTO
        self.desconto3 = self._SEM_DESCONTO
        self.multa = self._ISENTO_MULTA
        self.mora = self._ISENTO_MORA
        self.client_id = client_id
        self.client_secret = client_secret
        self.util = Util(
            base_url=base_url,
            base_url_token=base_url_token,
            client_id=client_id,
            client_secret=client_secret,
            cert=cert
        )

    # @property
    # def api_version(self):
    #     return self._API_VERSION

    # def set_base_url(self, value):
    #     self.base_url = value

    # def set_base_url_token(self, value):
    #     self.base_url_token = value

    # def set_api_version(self, api_version = 2):
    #     """Set API version, DEFAULT is API version 2."""
    #     self._API_VERSION = api_version

    # def _get_url(self, path):
    #     return f"{self.base_url}{path}"

    def set_desconto1(self, desconto1):
        """Dict para desconto no boleto.
        Código de Desconto do título.

        NAOTEMDESCONTO - Não tem desconto.
        VALORFIXODATAINFORMADA - Valor fixo até data informada.
        PERCENTUALDATAINFORMADA - Percentual até data informada.
        VALORANTECIPACAODIACORRIDO - Valor por antecipação (dia corrido).
        VALORANTECIPACAODIAUTIL - Valor por antecipação (dia útil).
        PERCENTUALVALORNOMINALDIACORRIDO - Percentual sobre o valor nominal por dia corrido.
        PERCENTUALVALORNOMINALDIAUTIL - Percentual sobre o valor nominal por dia útil.
        desconto1 = {
            "codigoDesconto": "ISENTO",
            "valor": 0,
            "taxa": 0
        }

        Args:
            desconto1 (dict): Dict de desconto a ser aplicado no boleto.
        """
        self.desconto1 = desconto1

    def set_desconto2(self, desconto2):
        """Dict para desconto no boleto.
        Código de Desconto do título.

        NAOTEMDESCONTO - Não tem desconto.
        VALORFIXODATAINFORMADA - Valor fixo até data informada.
        PERCENTUALDATAINFORMADA - Percentual até data informada.
        VALORANTECIPACAODIACORRIDO - Valor por antecipação (dia corrido).
        VALORANTECIPACAODIAUTIL - Valor por antecipação (dia útil).
        PERCENTUALVALORNOMINALDIACORRIDO - Percentual sobre o valor nominal por dia corrido.
        PERCENTUALVALORNOMINALDIAUTIL - Percentual sobre o valor nominal por dia útil.
        desconto2 = {
            "codigoDesconto": "ISENTO",
            "valor": 0,
            "taxa": 0
        }

        Args:
            desconto2 (dict): Dict de desconto a ser aplicado no boleto.
        """
        self.desconto2 = desconto2

    def set_desconto3(self, desconto3):
        """Dict para desconto no boleto.
        Codigo de Desconto do título.

        NAOTEMDESCONTO - Não tem desconto.
        VALORFIXODATAINFORMADA - Valor fixo até data informada.
        PERCENTUALDATAINFORMADA - Percentual até data informada.
        VALORANTECIPACAODIACORRIDO - Valor por antecipação (dia corrido).
        VALORANTECIPACAODIAUTIL - Valor por antecipação (dia útil).
        PERCENTUALVALORNOMINALDIACORRIDO - Percentual sobre o valor nominal por dia corrido.
        PERCENTUALVALORNOMINALDIAUTIL - Percentual sobre o valor nominal por dia útil.

        Args:
            desconto3 (dict): Dict de desconto a ser aplicado no boleto.
        """
        self.desconto3 = desconto3

    def set_multa(self, multa):
        """Codigo de Multa do título.

        NAOTEMMULTA - Não tem multa
        VALORFIXO – Valor Fixo
        PERCENTUAL - Percentual

        Args:
            multa (dict): Dict para configuracao de multa
        """
        self.multa = multa

    def set_mora(self, mora):
        """Codigo de Mora do titulo.

        VALORDIA - Valor ao dia
        TAXAMENSAL - Taxa mensal
        ISENTO - Não há mora

        Args:
            mora (dict): Dict para configuracao de juros de mora
        """
        self.mora = mora


    def boleto(
        self, pagador, mensagem, dataEmissao, dataVencimento, seuNumero, valorNominal
    ):
        """Metodo para emissao de boletos bancarios na API do Banco Inter.

           Saiba mais em: https://developers.bancointer.com.br/reference

        Args:
            pagador (dict): {
                "cpfCnpj": "99999999999", # valido
                "nome": "NOME DO PAGADOR",
                "email": "email@pagador.com",
                "telefone": "999999999",
                "cep": "99999999",
                "numero": "9999",
                "complemento": "",
                "bairro": "BAIRRO DO PAGADOR",
                "endereco": "ENDERECO DO PAGADOR",
                "cidade": "CURITIBA",
                "uf": "PR",
                "ddd": "99",
                "tipoPessoa": "JURIDICA" # OU FISICA
            }
            mensagem (dict): {
                "linha1": "linha1",
                "linha2": "linha2",
                "linha3": "linha3",
                "linha4": "linha4",
                "linha5": "linha5",
            }
            dataVencimento (str): "Y-m-d"
            seuNumero (str): seu numero de controle do documentp
            valorNominal (float): valor do boleto, ex: 100.50

        Returns:
            response: Corpo do response retornado pela API.
        """

        path = "boletos"

        json = {
            "pagador": pagador,
            "dataVencimento": dataVencimento,
            "numDiasAgenda": "30",
            "multa": self.multa,
            "mora": self.mora,
            "valorAbatimento": 0,
            "desconto1": self.desconto1,
            "desconto2": self.desconto2,
            "desconto3": self.desconto3,
            "seuNumero": seuNumero,
            "valorNominal": valorNominal,
            "mensagem": mensagem,
        }

        response = self.util.make_request_with_token(method="post", path=path, json=json)

        return response

    def download(self, nosso_numero, download_path):
        """Metodo para download de boletos emitidos.

        Args:
            nosso_numero (str): Nosso numero de identificacao do boleto
            download_path (str): Path completo para salvar o boleto. Ex: `C:\downloads`

        Returns:
            (bool): True em caso de sucesso ou False caso contrario.
        """
        path = f"boletos/{nosso_numero}/pdf"

        json = None

        response = self.util.make_request_with_token(method="get", path=path, json=json)

        file_path = download_path + os.sep + nosso_numero + ".pdf"

        return self.util.file_save(response, file_path)


    def baixa(self, nosso_numero, motivo: Baixa):
        """Metodo para baixa de boleto emitido.
        Dominio que descreve o tipo de baixa sendo solicitado.

        ACERTOS - Baixa por acertos
        PROTESTADO - Baixado por ter sido protestado
        DEVOLUCAO - Baixado para devolução
        PROTESTOAPOSBAIXA - Baixado por protesto após baixa
        PAGODIRETOAOCLIENTE - Baixado, pago direto ao cliente
        SUBISTITUICAO - Baixado por substituição
        FALTADESOLUCAO - Baixado por falta de solução
        APEDIDODOCLIENTE - Baixado a pedido do cliente

        Args:
            nosso_numero (str): Nosso numero de identificacao do boleto para baixa
            motivo (Baixa): Baixa Emum referente ao motivo da baixa do documento

        Returns:
            (response): Response da requisicao
        """
        act = "cancelar"
        json = {"motivoCancelamento": motivo.value}

        path = f"boletos/{nosso_numero}/{act}"

        response = self.util.make_request_with_token(method="post", path=path, json=json)

        return response

    def consulta(self, nosso_numero):
        """Recupera as informações detalhadas de um boleto através do `nosso_numero`.

        Args:
            nosso_numero (str): Nosso numero de identificação do boleto a ser recuperado

        Returns:
            dict: json-encoded of a response, `response.json()` dict com os dados do boleto.
        """
        path = f"boletos/{nosso_numero}"

        json = None

        response = self.util.make_request_with_token(method="get", path=path, json=json)

        return response.json()


