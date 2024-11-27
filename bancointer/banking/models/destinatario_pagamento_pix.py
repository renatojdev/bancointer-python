# destinatario_pagamento_pix.py


from dataclasses import dataclass, asdict
from typing import Dict, Any

from bancointer.banking.models.instituicao_financeira import InstituicaoFinanceira
from bancointer.banking.models.tipo_conta import TipoConta
from bancointer.banking.models.tipo_destinatario_pagamento_pix import (
    TipoDestinatarioPagamentoPix,
)
from bancointer.utils.bancointer_validations import BancoInterValidations
from bancointer.utils.exceptions import Erro, BancoInterException


@dataclass()
class DestinatarioPagamentoPix(object):

    tipo: TipoDestinatarioPagamentoPix
    contaCorrente: str = None
    tipoConta: TipoConta = None
    cpfCnpj: str = None
    agencia: str = None
    nome: str = None
    instituicaoFinanceira: InstituicaoFinanceira = None
    chave: str = None
    pixCopiaECola: str = None

    def to_dict(self) -> Dict[str, Any]:
        if not isinstance(self.tipo, str):
            self.tipo = self.tipo.value
        # chave is required
        if self.tipo == TipoDestinatarioPagamentoPix.CHAVE.value:
            if (
                self.chave is None
                or not isinstance(self.chave, str)
                or self.chave is ""
            ):
                erro = Erro(
                    404,
                    f"O atributo 'destinatarioPagamentoPix.chave' é obrigatório.",
                )
                raise BancoInterException("Erro de validação", erro)
            elif not BancoInterValidations.validate_pix_chave(self.chave):
                erro = Erro(
                    502,
                    f"O atributo 'destinatarioPagamentoPix.chave' é inválido.",
                )
                raise BancoInterException("Erro de validação", erro)

        # dados bancarios is required
        elif self.tipo == TipoDestinatarioPagamentoPix.DADOS_BANCARIOS.value:
            # validations
            required_fields = [
                "contaCorrente",
                "tipoConta",
                "cpfCnpj",
                "agencia",
                "nome",
                "instituicaoFinanceira",
            ]
            for campo in required_fields:
                campo_value = getattr(self, campo)
                if not hasattr(self, campo) or campo_value is None:
                    erro = Erro(
                        404,
                        f"O atributo 'destinatarioPagamentoPix.{campo}' é obrigatório.",
                    )
                    raise BancoInterException("Erro de validação", erro)
            self.tipoConta = self.tipoConta.value  # Serializable

            if not BancoInterValidations.validate_cpf_cnpj(self.cpfCnpj):
                erro = Erro(
                    502,
                    f"O atributo 'destinatarioPagamentoPix.cpfCnpj' é inválido.",
                )
                raise BancoInterException("Erro de validação", erro)

            # Validations
            if self.instituicaoFinanceira:
                if (
                    self.instituicaoFinanceira.ispb is None
                    or self.instituicaoFinanceira.ispb == ""
                    or len(self.instituicaoFinanceira.ispb) != 8
                ):
                    erro = Erro(
                        502,
                        f"O atributo 'destinatarioPagamentoPix.instituicaoFinanceira.ispb' é inválido.",
                    )
                    raise BancoInterException("Erro de validação", erro)

        # Pix copia e cola is required
        elif self.tipo == TipoDestinatarioPagamentoPix.PIX_COPIA_E_COLA.value:
            if (
                self.pixCopiaECola is None
                or not isinstance(self.pixCopiaECola, str)
                or self.pixCopiaECola is ""
            ):
                erro = Erro(
                    404,
                    f"O atributo 'destinatarioPagamentoPix.pixCopiaECola' é obrigatório.",
                )
                raise BancoInterException("Erro de validação", erro)

        """Converte a instância da classe em um dicionário, excluindo valores None."""
        return {k: v for k, v in asdict(self).items() if v is not None}
