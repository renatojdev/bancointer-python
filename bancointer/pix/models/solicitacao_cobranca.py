# solicitacao_cobranca.py


from dataclasses import dataclass, asdict
from typing import Any, Dict

from bancointer.pix.models.calendario import Calendario
from bancointer.pix.models.devedor_recebedor_cobranca import DevedorRecebedorCobranca
from bancointer.pix.models.id_loc_payload import IdentificadorLocalizacaoPayload
from bancointer.pix.models.info_adicional_cobranca_imediata import (
    InfoAdicionalCobrancaImediata,
)
from bancointer.pix.models.valor_cobranca import ValorCobranca
from bancointer.utils.bancointer_validations import BancoInterValidations
from bancointer.utils.exceptions import Erro, BancoInterException


@dataclass
class SolicitacaoCobranca(object):
    """Classe para solicitação de cobranca imediata ou com vencimento."""

    calendario: Calendario | dict
    valor: ValorCobranca | dict
    chave: str
    devedor: DevedorRecebedorCobranca = None
    loc: IdentificadorLocalizacaoPayload = None
    solicitacaoPagador: str = None
    infoAdicionais: [InfoAdicionalCobrancaImediata] = None
    status: str = None  # str 'REMOVIDA_PELO_USUARIO_RECEBEDOR'

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

        if type(self.calendario) is not dict:
            self.calendario = self.calendario.to_dict()
        if type(self.valor) is not dict:
            self.valor = self.valor.to_dict()

        return {k: v for k, v in asdict(self).items() if v is not None}
