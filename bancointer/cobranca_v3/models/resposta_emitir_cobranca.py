# resposta_emitir_cobranca.py

from dataclasses import dataclass, field, asdict
from typing import Any, Dict


@dataclass
class RespostaEmitirCobranca(object):
    """
    Código Solicitação Nosso Número, atribuído automaticamente pelo banco na emissão do título.
    """

    codigoSolicitacao: str = None
    campos_adicionais: Dict[str, Any] = field(default_factory=dict)

    def add_campo_adicional(self, nome: str, valor: Any) -> None:
        """Adiciona um campo adicional ao dicionário de campos adicionais."""
        self.campos_adicionais[nome] = valor

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""
        return {k: v for k, v in asdict(self).items() if v is not None}
