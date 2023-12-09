import re

TOKENS = [

    {"token": "TIPO_VARIAVEL", "pattern": r"\b(int|float|double|char)\b"},
    {"token": "FUNCAO_MAIN", "pattern": r"main"},
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
    {"token": "VIRGULA", "pattern": r','},
    {"token": "COMENTARIO", "pattern": r"//.*|/\*[\s\S]*?\*/"}
]

def analisador_lexico(input_string):
    tokens_identificados = []
    index = 0
    numero_linha = 1  # Inicia a contagem de linhas a partir de 1

    while index < len(input_string):
        matched = False

        # Ignorar espaços em branco e comentários
        if input_string[index] in [" ", "\t", "\r", "\n"]:
            index += 1
            continue
        elif input_string[index:index + 2] == "//":
            index = input_string.find("\n", index)
            if index == -1:
                break
            numero_linha += 1
            index += 1
            continue
        elif input_string[index:index + 2] == "/*":
            index = input_string.find("*/", index)
            if index == -1:
                return f"Erro: Comentário não fechado na linha {numero_linha}, posição {index + 2}"
            index += 2
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
