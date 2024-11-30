# desconto_cobranca.py


from dataclasses import dataclass


@dataclass
class DescontoDataFixa(object):
    data: str  # formato YYYY-MM-DD, segundo ISO 8601.
    valorPerc: str  # (Valor do desconto absoluto) \d{1,10}\.\d{2}


@dataclass
class ValorPerc(object):
    valorPerc: str  # (Valor do desconto absoluto) \d{1,10}\.\d{2}
    # Tabela descrição	Domínio
    # Valor Fixo até a[s] data[s] informada[s]	1
    # Percentual até a[s] data[s] informada[s]	2
    # Valor por antecipação dia corrido	3
    # Valor por antecipação dia útil	4
    # Percentual por antecipação dia corrido	5
    # Percentual por antecipação dia útil	6
    modalidade: str = 1  # Modalidade de desconto, conforme tabela de domínios.


@dataclass
class DescontoCobranca(object):
    descontoDataFixa: [DescontoDataFixa]
    # Tabela descrição	Domínio
    # Valor Fixo até a[s] data[s] informada[s]	1
    # Percentual até a[s] data[s] informada[s]	2
    # Valor por antecipação dia corrido	3
    # Valor por antecipação dia útil	4
    # Percentual por antecipação dia corrido	5
    # Percentual por antecipação dia útil	6
    modalidade: str = 1  # Modalidade de desconto, conforme tabela de domínios.
