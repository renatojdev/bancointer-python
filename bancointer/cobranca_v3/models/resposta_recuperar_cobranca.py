# # resposta_recuperar_cobranca.py.py

from dataclasses import dataclass, field, asdict
from typing import Any, Dict

from bancointer.cobranca_v3.models import Pix
from bancointer.cobranca_v3.models import Boleto
from bancointer.cobranca_v3.models import Cobranca


@dataclass
class RespostaRecuperarCobranca(object):
    """
        Código Solicitação Nosso Número, atribuído automaticamente pelo banco na emissão do título.

        Example:
            {
      "cobranca": {
        "seuNumero": "00001",
        "dataEmissao": "2024-11-11",
        "dataVencimento": "2024-11-21",
        "valorNominal": 2.5,
        "tipoCobranca": "SIMPLES",
        "situacao": "A_RECEBER",
        "dataSituacao": "2024-11-11",
        "arquivada": false,
        "descontos": [
          {
            "codigo": "PERCENTUALDATAINFORMADA",
            "quantidadeDias": 0,
            "taxa": 1.2
          }
        ],
        "multa": {
          "codigo": "VALORFIXO",
          "valor": 100
        },
        "mora": {
          "codigo": "TAXAMENSAL",
          "taxa": 4.5
        },
        "pagador": {
          "cpfCnpj": "99999999999",
          "tipoPessoa": "FISICA",
          "nome": "NOME DO PAGADOR",
          "endereco": "ENDERECO DO PAGADOR",
          "bairro": "",
          "cidade": "CIDADE DO PAGADOR",
          "uf": "PR",
          "cep": "80030000",
          "email": "",
          "numero": "",
          "complemento": ""
        }
      },
      "boleto": {
        "nossoNumero": "3364699211",
        "codigoBarras": "00000033641836128354683148168282409334777187",
        "linhaDigitavel": "00000033641836534950656166811518570490033128415"
      },
      "pix": {
        "txid": "336418361731333813000Uusr9kwpzFRNiz",
        "pixCopiaECola": "000201010212261010014BR.GOV.BCB.PIX2579cdpj-sandbox.partners.uatinter.co/pj-s/v2/cobv/afad912c569348b6b6a3476ca4579a6d52040000530398654042.505802BR5901*6013Belo Horizont61089999999962070503***6304A5CC"
      }
    }
    """

    # def __init__(self, cobranca, boleto, pix):
    cobranca: Cobranca = None
    boleto: Boleto = None
    pix: Pix = None
    campos_adicionais: Dict[str, Any] = field(default_factory=dict)

    def add_campo_adicional(self, nome: str, valor: Any) -> None:
        """Adiciona um campo adicional ao dicionário de campos adicionais."""
        self.campos_adicionais[nome] = valor

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""
        return {k: v for k, v in asdict(self).items() if v is not None}
