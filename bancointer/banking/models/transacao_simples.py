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


    def __init__(
        self,
        cpmf: str,
        dataEntrada: str,
        tipoTransacao: TipoTransacao,
        tipoOperacao: TipoOperacao,
        valor: str,
        titulo: str,
        descricao: str,
    ):
        self.cpmf = cpmf
        self.dataEntrada = dataEntrada
        self.tipoTransacao = tipoTransacao
        self.tipoOperacao = tipoOperacao
        self.valor = valor
        self.titulo = titulo
        self.descricao = descricao


    def to_dict(self):
        return {
            '**dataEntrada': self.dataEntrada,
            'tipoTransacao': self.tipoTransacao,
            'tipoOperacao': self.tipoOperacao,
            'valor': self.valor,
            'titulo': self.titulo,
            'descricao': self.descricao
        }