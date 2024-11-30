# devedor_recebedor_cobranca.py


from dataclasses import dataclass, asdict
from typing import Any, Dict


@dataclass()
class DevedorRecebedorCobranca(object):
    nome: str
    cpf: str = None
    cnpj: str = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""
        return {k: v for k, v in asdict(self).items() if v is not None}
