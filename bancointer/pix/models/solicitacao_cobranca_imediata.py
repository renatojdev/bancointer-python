# solicitacao_cobranca_imediata.py


from dataclasses import dataclass, asdict
from typing import Any, Dict

from bancointer.pix.models.calendario import Calendario
from bancointer.pix.models.devedor_cobranca_imediata import DevedorCobrancaImediata
from bancointer.pix.models.id_loc_payload import IdentificadorLocalizacaoPayload
from bancointer.pix.models.info_adicional_cobranca_imediata import (
    InfoAdicionalCobrancaImediata,
)
from bancointer.pix.models.valor_cobranca_imediata import ValorCobrancaImediata
from bancointer.utils.bancointer_validations import BancoInterValidations
from bancointer.utils.exceptions import Erro, BancoInterException


@dataclass()
class SolicitacaoCobrancaImediata(object):
    calendario: Calendario
    valor: ValorCobrancaImediata
    chave: str
    devedor: DevedorCobrancaImediata = None
    loc: IdentificadorLocalizacaoPayload = None
    solicitacaoPagador: str = None
    infoAdicionais: [InfoAdicionalCobrancaImediata] = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte a instância da classe em um dicionário, excluindo valores None."""

        # validations
        required_fields = ["calendario", "valor", "chave"]
        for campo in required_fields:
            campo_value = getattr(self, campo)
            if not hasattr(self, campo) or campo_value is None or campo_value is "":
                erro = Erro(
                    404,
                    f"O atributo 'solicitacaoCobrancaImediata.{campo}' é obrigatório.",
                )
                raise BancoInterException("Erro de validação", erro)

            if self.chave and not BancoInterValidations.validate_pix_chave(self.chave):
                erro = Erro(
                    502,
                    f"O atributo 'solicitacaoCobrancaImediata.chave' é inválido.",
                )
                raise BancoInterException("Erro de validação", erro)

        return {k: v for k, v in asdict(self).items() if v is not None}
