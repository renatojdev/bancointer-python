# date_utils.py

from datetime import datetime


class DateUtils(object):

    def periodo_dates_extrato_e_valido(self, data_inicio, data_fim):
        # Definindo as datas de início e fim
        # data_inicio = '2024-01-01'  # Formato: 'YYYY-MM-DD'
        # data_fim = '2024-03-01'

        # Convertendo as strings para objetos datetime
        inicio = datetime.strptime(data_inicio, "%Y-%m-%d")
        fim = datetime.strptime(data_fim, "%Y-%m-%d")

        # Calculando a diferença entre as datas
        diferenca = (fim - inicio).days

        # Verificando se a diferença é maior que 90 dias
        if diferenca <= 90:
            print("O periodo entre as datas e de ate 90 dias.")
            return True
        else:
            print("O periodo entre as datas excede 90 dias.")
            return False
