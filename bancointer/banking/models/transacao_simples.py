# transacao_simples.py

from bancointer.banking.models.tipo_operacao import TipoOperacao
from bancointer.banking.models.tipo_transacao import TipoTransacao


class TransacaoSimples(object):
    cpmf: str
    dataEntrada: str
    tipoTransacao: TipoTransacao
    tipoOperacao: TipoOperacao
    valor: str
    titulo: str
    descricao: str
