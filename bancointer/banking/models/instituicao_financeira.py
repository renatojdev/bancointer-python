# instituicao_financeira.py


from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass()
class InstituicaoFinanceira(object):

    ispb: str  # Código ISPB, de 8 dígitos, dos bancos

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""
        return {k: v for k, v in asdict(self).items() if v is not None}
