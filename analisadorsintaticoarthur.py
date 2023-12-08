class CParser:
    def __init__(self, tokens):
        # Inicializa o analisador com uma lista de tokens
        self.tokens = tokens
        self.current_token = None  # O token atual sendo analisado
        self.current_index = 0  # Índice para rastrear a posição atual na lista de tokens

    def parse(self):
        # Função principal para iniciar a análise sintática
        return self.parse_expression()

    def parse_expression(self):
        # Analisa expressões, incluindo adição e subtração
        term = self.parse_term()

        while self.current_token in ('+', '-'):
            # Se o próximo token for um operador de adição ou subtração, continua analisando
            operator = self.current_token
            self.consume_token()  # Consome o operador
            next_term = self.parse_term()
            term = (operator, term, next_term)  # Constrói a árvore sintática

        return term

    def parse_term(self):
        # Analisa termos, incluindo multiplicação e divisão
        factor = self.parse_factor()

        while self.current_token in ('*', '/'):
            # Se o próximo token for um operador de multiplicação ou divisão, continua analisando
            operator = self.current_token
            self.consume_token()  # Consome o operador
            next_factor = self.parse_factor()
            factor = (operator, factor, next_factor)  # Constrói a árvore sintática

        return factor

    def parse_factor(self):
        # Analisa fatores, incluindo parênteses e números
        if self.current_token == '(':
            # Se o próximo token for '(', analisa a expressão dentro dos parênteses
            self.consume_token()  # Consome '('
            expression = self.parse_expression()
            if self.current_token == ')':
                # Se o próximo token for ')', consome ')' e retorna a expressão dentro dos parênteses
                self.consume_token()
                return expression
            else:
                raise SyntaxError("Expected closing parenthesis")
        elif self.current_token.isdigit():
            # Se o próximo token for um número, consome o número e retorna seu valor
            value = int(self.current_token)
            self.consume_token()
            return value
        else:
            raise SyntaxError(f"Unexpected token: {self.current_token}")

    def consume_token(self):
        # Consome o próximo token na lista de tokens
        if self.current_index < len(self.tokens):
            self.current_token = self.tokens[self.current_index]
            self.current_index += 1
        else:
            self.current_token = None


# Exemplo de uso
if __name__ == "__main__":
    input_tokens = ['2', '+', '3', '*', '(', '4', '-', '1', ')']
    parser = CParser(input_tokens)
    result = parser.parse()
    print(f"Tokens analisados: {input_tokens}")
    print(f"Resultado da análise: {result}")
