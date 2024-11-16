# banking.py


class Banking(object):
    """Classe para transacoes API BANKING do Banco Inter PJ.
    Consulta de extrato da conta.
    """

    def __init__(self, cert):
        self.set_dt_end = None
        self.set_dt_ini = None
        self.cert = cert
        self.headers = {
            "Accept": "application/json",
            "Authorization": "Bearer xxxxxxxx-xxxxxxx-xxxxxxx-xxxxxxx",
        }

    def set_dt_ini(self, value):
        self.set_dt_ini = value

    def set_dt_end(self, value):
        self.set_dt_end = value

    def extrato(self, dt_ini=None, dt_end=None):
        pass
