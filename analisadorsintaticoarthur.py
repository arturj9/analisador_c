class AnalisadorSintatico:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def analisar(self):
        self.programa()

    def proximo_token(self):
        if self.index < len(self.tokens):
            return self.tokens[self.index]
        else:
            return None

    def consome_token(self):
        self.index += 1

    def programa(self):
        while self.proximo_token():
            self.stmt_list()

    def stmt_list(self):
        self.stmt()
        while self.proximo_token()["token"] == "PONTO_VIRGULA":
            self.consome_token()
            self.stmt()

    def stmt(self):
        if self.proximo_token()["token"] == "TIPO_VARIAVEL":
            self.declaracao_variavel()
        elif self.proximo_token()["token"] == "IDENTIFICADOR":
            self.atribuicao()
        elif self.proximo_token()["token"] == "IF":
            self.estrutura_if()
        elif self.proximo_token()["token"] == "WHILE":
            self.estrutura_while()
        elif self.proximo_token()["token"] == "FOR":
            self.estrutura_for()

    def declaracao_variavel(self):
        self.tipo_variavel()
        self.consome_token()
        self.identificador()
        while self.proximo_token()["token"] == "COMMA":
            self.consome_token()
            self.identificador()
        self.consome_token()  # PONTO_VIRGULA

    def tipo_variavel(self):
        self.consome_token()  # TIPO_VARIAVEL

    def identificador(self):
        self.consome_token()  # IDENTIFICADOR

    def atribuicao(self):
        self.identificador()
        self.consome_token()  # ATRIBUICAO
        self.expressao()
        self.consome_token()
