import re

TOKENS = [
    {"token": "DECLARACAO_MAIN", "pattern": r"\bmain\b"},
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

    while index < len(input_string):
        matched = False

        for token_info in TOKENS:
            pattern = r'^' + token_info["pattern"]
            match = re.match(pattern, input_string[index:])

            if match:
                matched = True

                if token_info["token"] not in ["ESPACO", "COMENTARIO"]:
                    tokens_identificados.append({"token": token_info["token"], "value": match.group(0)})

                index += len(match.group(0))
                break

        if not matched:
            return f"Caractere inválido na posição {index}: {input_string[index]}"

    return tokens_identificados
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

    for (int i = 0; i < 5; i++) {
        x = x + i;
    }

    return 0;
}
'''
print(analisador_lexico(code))


