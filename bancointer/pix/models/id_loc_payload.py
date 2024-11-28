# id_loc_payload.py


from dataclasses import dataclass, asdict
from typing import Any, Dict

from bancointer.pix.models.tipo_cobranca import TipoCobranca


@dataclass
class IdentificadorLocalizacaoPayload(object):
    id: int
    tipoCob: TipoCobranca
    criacao: str
    location: str = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""
        return {k: v for k, v in asdict(self).items() if v is not None}
