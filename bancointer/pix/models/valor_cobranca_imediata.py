# valor_cobranca_imediata.py


from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass()
class ValorCobrancaImediata(object):
    original: str  # required string (Valor) \d{1,10}\.\d{2}
    modalidadeAlteracao: int = (
        0  # integer <int32> default 0 | 1 - Trata-se de um campo que determina se o valor final do documento pode ser alterado pelo pagador. Na ausência desse campo, assume-se que não se pode alterar o valor do documento de cobrança, ou seja, assume-se o valor 0. Se o campo estiver presente e com valor 1, então está determinado que o valor final da cobrança pode ter seu valor alterado pelo pagador.
    )

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""
        return {k: v for k, v in asdict(self).items() if v is not None}
