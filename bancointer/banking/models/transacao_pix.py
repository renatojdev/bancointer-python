# transacao_pix.py


from dataclasses import dataclass

from bancointer.banking.models.aut_bank_erro import AutbankErro
from bancointer.banking.models.autbank_dados_conta import AutbankDadosConta
from bancointer.banking.models.status_transaco_pix import StatusTransacaoPix


@dataclass()
class TransacaoPix(object):
    contaCorrente: str
    recebedor: AutbankDadosConta
    erros: [AutbankErro]
    endToEnd: str
    valor: float
    status: StatusTransacaoPix
    dataHoraMovimento: str
    dataHoraSolicitacao: str
    chave: str
    codigoSolicitacao: str
