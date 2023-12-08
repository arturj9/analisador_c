import re

TOKENS = [
    {"token": "DECLARACAO_MAIN", "pattern": r"\bmain\b"},
    {"token": "TIPO_VARIAVEL", "pattern": r"\b(int|float|double|char)\b"},
    {"token": "PARENTESE_ABRE", "pattern": r"\("},
    {"token": "PARENTESE_FECHA", "pattern": r"\)"},
    {"token": "CHAVE_ABRE", "pattern": r"\{"},
    {"token": "CHAVE_FECHA", "pattern": r"\}"},
    {"token": "PONTO_VIRGULA", "pattern": r";"},
    {"token": "ATRIBUICAO", "pattern": r"="},
    {"token": "SOMA", "pattern": r"\+"},
    {"token": "SUBTRACAO", "pattern": r"-"},
    {"token": "MULTIPLICACAO", "pattern": r"\*"},
    {"token": "DIVISAO", "pattern": r"/"},
    {"token": "IGUAL", "pattern": r"=="},
    {"token": "DIFERENTE", "pattern": r"!="},
    {"token": "MENOR_QUE", "pattern": r"<"},
    {"token": "MAIOR_QUE", "pattern": r">"},
    {"token": "MENOR_OU_IGUAL", "pattern": r"<="},
    {"token": "MAIOR_OU_IGUAL", "pattern": r">="},
    {"token": "E_LOGICO", "pattern": r"&&"},
    {"token": "OU_LOGICO", "pattern": r"\|\|"},
    {"token": "NAO_LOGICO", "pattern": r"!"},
    {"token": "IF", "pattern": r"\bif\b"},
    {"token": "ELSE", "pattern": r"\belse\b"},
    {"token": "WHILE", "pattern": r"\bwhile\b"},
    {"token": "FOR", "pattern": r"\bfor\b"},
    {"token": "IDENTIFICADOR", "pattern": r"[a-zA-Z_][a-zA-Z0-9_]*"},
    {"token": "NUMERO", "pattern": r"\b\d+(\.\d+)?\b"},
    {"token": "ESPACO", "pattern": r"\s+"},
    {"token": "COMMA", "pattern": r','},
    {"token": "COMENTARIO", "pattern": r"//.*|/\*[\s\S]*?\*/"}
]

def analisador_lexico(input_string):
    tokens_identificados = []
    index = 0
    numero_linha = 1  # Inicia a contagem de linhas a partir de 1

    while index < len(input_string):
        matched = False

        # Verifica se é uma quebra de linha e atualiza o contador de linhas
        if input_string[index] == "\n":
            numero_linha += 1
            index += 1
            continue

        for token_info in TOKENS:
            pattern = r'^' + token_info["pattern"]
            match = re.match(pattern, input_string[index:])

            if match:
                matched = True

                if token_info["token"] not in ["ESPACO", "COMENTARIO"]:
                    tokens_identificados.append({"token": token_info["token"], "value": match.group(0), "linha": numero_linha})

                index += len(match.group(0))
                break

        if not matched:
            return f"Erro: Caractere inválido na linha {numero_linha}, posição {index}: {input_string[index]}"

    return tokens_identificados
def analisar_declaracao_variavel(tokens):
    if not tokens:
        return False

    # Verifica se o primeiro token é um tipo de variável
    if tokens[0]["token"] != "TIPO_VARIAVEL":
        return False

    # Deve haver pelo menos um identificador após o tipo
    tokens = tokens[1:]
    if not tokens or tokens[0]["token"] != "IDENTIFICADOR":
        return False

    # Processa o resto dos tokens
    tokens = tokens[1:]
    while tokens:
        # Verifica se há um ponto e vírgula para terminar a declaração
        if tokens[0]["token"] == "PONTO_VIRGULA":
            return True

        # Se houver uma vírgula, deve haver outro identificador
        if tokens[0]["token"] == "VIRGULA":
            tokens = tokens[1:]
            if not tokens or tokens[0]["token"] != "IDENTIFICADOR":
                return False
        else:
            # Se não for uma vírgula, não é uma declaração de variável válida
            return False

        tokens = tokens[1:]

    # Se a lista de tokens terminou sem encontrar um ponto e vírgula, a declaração é inválida
    return False
code = '''
int main() {
    int x, y;
    x = 5;
    y = 10;

    if (x > y) {
        y = x + y;
    } else {
        y = x - y;
    }

    while (y > 0) {
        x = x * 2;
        y = y - 1;
    }

    for (int i = 0@; i < 5; i++) {
        x = x + i;
    }

    return 0;
}
'''
print(analisador_lexico(code))


