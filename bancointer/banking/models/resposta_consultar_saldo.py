# resposta_consultar_saldo.py


from dataclasses import asdict, dataclass
from typing import Dict, Any


@dataclass
class RespostaConsultarSaldo(object):
    """Resposta de consulta de saldo."""

    bloqueadoCheque: float = None
    disponivel: float = None
    bloqueadoJudicialmente: float = None
    bloqueadoAdministrativo: float = None
    limite: float = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""
        return {k: v for k, v in asdict(self).items() if v is not None}
