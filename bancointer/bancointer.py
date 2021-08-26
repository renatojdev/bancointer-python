import os
import requests
import codecs
from .baixa import Baixa


class BancoInter(object):
    """Classe para transacoes (emissao, baixa, download) de boletos na API do Banco Inter PJ.

    Na emissao de boletos o padrao inicial e sem desconto, multa e juros de mora.
    """

    # Class attributes
    _BASE_URL = "https://apis.bancointer.com.br/openbanking/v1/certificado/"
    _SEM_DESCONTO = {
        "codigoDesconto": "NAOTEMDESCONTO",
        "taxa": 0,
        "valor": 0,
        "data": "",
    }
    _ISENTO_MULTA = {"codigoMulta": "NAOTEMMULTA", "valor": 0, "taxa": 0}
    _ISENTO_MORA = {"codigoMora": "ISENTO", "valor": 0, "taxa": 0}

    def __init__(self, cpf_cnpj_beneficiario, x_inter_conta_corrente, cert):
        """Metodo construtor da classe.

        Args:
            cpf_cnpj_beneficiario (str): cpf/cnpj do beneficiario do boleto
            x_inter_conta_corrente (str): numero da conta corrente do beneficiario do boleto.
            cert (tuple): (cert_file_path, key_file_path) PEM path do certificado digital e PEM path da chave publica.
        """
        self.cpf_cnpj_beneficiario = cpf_cnpj_beneficiario
        self.inter_conta_corrente = x_inter_conta_corrente
        self.cert = cert
        self.desconto1 = self._SEM_DESCONTO
        self.desconto2 = self._SEM_DESCONTO
        self.desconto3 = self._SEM_DESCONTO
        self.multa = self._ISENTO_MULTA
        self.mora = self._ISENTO_MORA

    def _get_url(self, path):
        return f"{self._BASE_URL}{path}"

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

    @property
    def headers(self):
        return {"x-inter-conta-corrente": self.inter_conta_corrente}

    def _request(self, method, path, json, **kwargs):
        """Executa as requisicoes na API do Banco Inter conforme os parametros de entrada.

        Args:
            method (str): Metodo de requisicao GET / POST.
            path (str): URL / endpoint para a requisicao
            json (dict): Json para ser enviado no POST.

        Returns:
            dict or int: Retorna json response caso exista ou status code do response.
        """
        if method == "get" or json == None:
            request = requests.request(
                method=method,
                url=self._get_url(path),
                headers=self.headers,
                **kwargs,
            )
            return request

        request = requests.request(
            method=method,
            url=self._get_url(path),
            headers=self.headers,
            json=json,
            **kwargs,
        )
        try:
            return request.json()
        except ValueError:  # empty response
            return request.status_code

    def boleto(
        self, pagador, mensagem, dataEmissao, dataVencimento, seuNumero, valorNominal
    ):
        """Metodo para emissao de boletos bancarios na API do Banco Inter.

           Saiba mais em: https://developers.bancointer.com.br/reference

        Args:
            pagador (dict): {
                "cnpjCpf": "99999999999", # valido
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
            dataEmissao (str): "Y-m-d"
            dataVencimento (str): "Y-m-d"
            seuNumero (str): seu numero de controle do documentp
            valorNominal (float): valor do boleto, ex: 100.50

        Returns:
            response: Corpo do response retornado pela API.
        """

        path = "boletos"

        json = {
            "cnpjCPFBeneficiario": self.cpf_cnpj_beneficiario,
            "pagador": pagador,
            "dataEmissao": dataEmissao,
            "dataVencimento": dataVencimento,
            "dataLimite": "TRINTA",
            "numDiasAgenda": "TRINTA",
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

        response = self._request(method="post", path=path, json=json, cert=self.cert)

        return response

    def _response_save(self, response, file_path):
        if response.content:

            try:
                with open(file_path, "wb") as out_file:
                    out_file.write(codecs.decode(response.content, "base64"))
                out_file.close()
            except Exception as e:
                print("bancointer.Except: ", e)
                return False
            return True

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

        response = self._request(method="get", path=path, json=json, cert=self.cert)

        file_path = download_path + os.sep + nosso_numero + ".pdf"

        return self._response_save(response, file_path)

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
        path = f"boletos/{nosso_numero}/baixas"

        json = {"codigoBaixa": motivo.value}

        response = self._request(method="post", path=path, json=json, cert=self.cert)

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

        response = self._request(method="get", path=path, json=json, cert=self.cert)

        return response.json()
