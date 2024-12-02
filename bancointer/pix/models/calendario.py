# calendario.py


from dataclasses import dataclass, asdict
from typing import Any, Dict

from bancointer.utils.bancointer_validations import BancoInterValidations
from bancointer.utils.exceptions import Erro, BancoInterException


@dataclass()
class Calendario(object):
    dataDeVencimento: str  # date YYYY-MM-DD, segundo ISO 8601.
    expiracao: int = 3600
    criacao: str = None
    validadeAposVencimento: int = 30

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""

        # validations
        required_fields = ["dataDeVencimento"]
        for campo in required_fields:
            campo_value = getattr(self, campo)
            if not hasattr(self, campo) or campo_value is None or campo_value is "":
                erro = Erro(
                    404,
                    f"O atributo 'calendario.{campo}' é obrigatório.",
                )
                raise BancoInterException("Erro de validação", erro)

        if not BancoInterValidations.validate_date(self.dataDeVencimento):
            erro = Erro(
                502,
                f"O atributo 'calendario.dataDeVencimento' é inválido.",
            )
            raise BancoInterException("Erro de validação", erro)

        return {k: v for k, v in asdict(self).items() if v is not None}
