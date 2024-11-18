# exceptions.py


class ErroApi(Exception):
    def __init__(self, title, detail, timestamp, violacoes=None, *args, **kwargs):
        self.title = title
        self.detail = detail
        self.timestamp = timestamp
        self.violacoes = violacoes if violacoes is not None else [{}]

    def to_dict(self):
        return {
            "title": self.title,
            "detail": self.detail,
            "timestamp": self.timestamp,
            "violacoes": self.violacoes,
        }


class Erro:
    """Classe para representar um erro específico."""

    def __init__(self, codigo, descricao):
        self.codigo = codigo
        self.descricao = descricao

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "descricao": self.descricao,
        }


class BancoInterException(Exception):
    """Exceção personalizada para SDK."""

    def __init__(self, mensagem, erro):
        super().__init__(mensagem)  # Chama o construtor da classe pai
        self.erro = erro  # Armazena a instância de Erro


# Exemplo de uso
# try:
#     # Simulando um erro
#     erro = Erro(404, "Recurso não encontrado")
#     raise BancoInterException("Ocorreu um erro no SDK", erro)
# except BancoInterException as e:
#     print(f"Mensagem: {e}")
#     print(f"Código do Erro: {e.erro.codigo}, Descrição: {e.erro.descricao}")
