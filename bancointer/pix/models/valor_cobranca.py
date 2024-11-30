# valor_cobranca.py


from dataclasses import dataclass, asdict
from typing import Dict, Any

from bancointer.pix.models.desconto_cobranca import DescontoCobranca


@dataclass
class SaqueOuTroco:
    valor: str  # req string (Valor do saque) \d{1,10}\.\d{2}
    modalidadeAgente: str  # Modalidade Agente AGTEC - Agente Estabelecimento Comercial.
    # AGTOT - Agente Outra Espécie de Pessoa Jurídica ou Correspondente no País.
    # AGPSS - Agente Facilitador de Serviço de Saque.
    prestadorDoServicoDeSaque: str  # ISPB do Facilitador de Serviço de Saque
    modalidadeAlteracao: 0 | 1 = 0


@dataclass
class Retirada:
    saque: SaqueOuTroco = None
    troco: SaqueOuTroco = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class ValorCobranca(object):
    original: str  # required string (Valor) \d{1,10}\.\d{2}
    retirada: Retirada | dict = None
    modalidadeAlteracao: 0 | 1 = (
        0  # integer <int32> default 0 | 1 - Trata-se de um campo que determina se o valor final do documento pode ser alterado pelo pagador. Na ausência desse campo, assume-se que não se pode alterar o valor do documento de cobrança, ou seja, assume-se o valor 0. Se o campo estiver presente e com valor 1, então está determinado que o valor final da cobrança pode ter seu valor alterado pelo pagador.
    )
    desconto: DescontoCobranca = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""

        if self.retirada:
            self.original = "0.00"  # quando o saque ou troco estiver presente
            self.retirada = self.retirada.to_dict()

        return {k: v for k, v in asdict(self).items() if v is not None}
