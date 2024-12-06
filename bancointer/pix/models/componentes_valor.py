# componentes_valor.py


from dataclasses import dataclass, asdict
from typing import Dict, Any

from bancointer.pix.models.valor_cobranca import SaqueOuTroco


class PixValorOriginal:
    valor: str  # req string (Valor original) \d{1,10}\.\d{2}

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""
        return {k: v for k, v in asdict(self).items() if v is not None}


class PixValor:
    valor: str  # required string \d{1,10}\.\d{2}

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""
        return {k: v for k, v in asdict(self).items() if v is not None}


class Paginacao:
    paginaAtual: int  # req >= 0
    itensPorPagina: int  # req >= 1
    quantidadeDePaginas: int  # req >=1
    quantidadeTotalDeItens: int  # req >=0


class PixValorAbatimento:
    abatimento: PixValor = None
    txIdPresente: bool = None
    devolucaoPresente: bool = None
    cpf: str = None
    cnpj: str = None
    paginacao: Paginacao = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class ComponentesValor(object):
    original: PixValorOriginal | dict = None
    saque: SaqueOuTroco | dict = None
    troco: SaqueOuTroco | dict = None
    juros: PixValor | dict = None
    multa: PixValor | dict = None
    pixValorAbatimento: PixValorAbatimento | dict = None
    desconto: PixValor | dict = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""

        if self.original:
            self.original = self.original.to_dict()
        if self.saque:
            self.saque = self.saque.to_dict()
        if self.troco:
            self.troco = self.troco.to_dict()
        if self.juros:
            self.juros = self.juros.to_dict()
        if self.multa:
            self.multa = self.multa.to_dict()
        if self.pixValorAbatimento:
            self.pixValorAbatimento = self.pixValorAbatimento.to_dict()
        if self.desconto:
            self.desconto = self.desconto.to_dict()

        return {k: v for k, v in asdict(self).items() if v is not None}
