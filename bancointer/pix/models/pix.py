# pix.py


from dataclasses import dataclass, asdict
from typing import Any, Dict

from bancointer.pix.models.componentes_valor import ComponentesValor
from bancointer.pix.models.devolucao import Devolucao


@dataclass
class Pix(object):
    endToEndId: str  # req string (Id fim a fim da transação) [a-zA-Z0-9]{32}
    valor: str  # req string (Valor do Pix.) \d{1,10}\.\d{2}
    horario: str  # req string <date-time> (Horário)
    txid: str = None  # string (Id da Transação) [a-zA-Z0-9]{1,35}
    componentesValor: ComponentesValor | dict = (
        None  #  Elementos de composição do valor do Pix
    )
    chave: str = None  # string (Chave DICT do recebedor) <= 77 characters
    infoPagador: str = None  # 	string (Informação livre do pagador) <= 140 characters
    devolucoes: [Devolucao] = None  # array of objects (Devolucoes)

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""

        if self.componentesValor and not isinstance(self.componentesValor, dict):
            self.componentesValor = self.componentesValor.to_dict()

        return {k: v for k, v in asdict(self).items() if v is not None}
