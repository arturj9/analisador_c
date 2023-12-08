import re

TOKENS = [

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
    {"token": "VIRGULA", "pattern": r','},
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
code = '''
int main(){
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
#print(analisador_lexico(code))


#ANALISADOR SINTÁTICO
def analisar_declaracao_variavel(tokens):
    if not tokens:
        return "Erro: Nenhum token fornecido para análise."

    # Verifica se o primeiro token é um tipo de variável
    if tokens[0]["token"] != "TIPO_VARIAVEL":
        return f"Erro na linha {tokens[0]['linha']}: Esperado um tipo de variável, encontrado '{tokens[0]['value']}'."

    # Deve haver pelo menos um identificador após o tipo
    tokens = tokens[1:]
    if not tokens or tokens[0]["token"] != "IDENTIFICADOR":
        return "Erro: Esperado um identificador após o tipo de variável."

    # Processa o resto dos tokens
    tokens = tokens[1:]
    while tokens:
        # Verifica se há um ponto e vírgula para terminar a declaração
        if tokens[0]["token"] == "PONTO_VIRGULA":
            return "Declaração de variável válida."

        # Se houver uma vírgula, deve haver outro identificador
        if tokens[0]["token"] == "VIRGULA":
            tokens = tokens[1:]
            if not tokens or tokens[0]["token"] != "IDENTIFICADOR":
                return "Erro: Esperado um identificador após a vírgula."
        else:
            # Se não for uma vírgula, não é uma declaração de variável válida
            return f"Erro na linha {tokens[0]['linha']}: Caractere ou token inesperado '{tokens[0]['value']}'."

        tokens = tokens[1:]

    # Se a lista de tokens terminou sem encontrar um ponto e vírgula, a declaração é inválida
    return "Erro: Declaração de variável não terminada corretamente (faltando ponto e vírgula)."
def analisar_declaracao_main(tokens):
    if not tokens:
        return "Erro: Nenhum token fornecido para análise."

    # Procura pelo padrão da declaração da função main
    if len(tokens) < 5:
        return "Erro: Tokens insuficientes para uma declaração de 'main'."

    if tokens[0]["token"] != "TIPO_VARIAVEL" or tokens[0]["value"] != "int":
        return f"Erro na linha {tokens[0]['linha']}: Tipo de retorno da 'main' deve ser 'int', encontrado '{tokens[0]['value']}'."

    if tokens[1]["token"] != "IDENTIFICADOR" or tokens[1]["value"] != "main":
        return f"Erro na linha {tokens[1]['linha']}: Esperado identificador 'main', encontrado '{tokens[1]['value']}'."

    if tokens[2]["token"] != "PARENTESE_ABRE":
        return f"Erro na linha {tokens[2]['linha']}: Esperado '(', encontrado '{tokens[2]['value']}'."

    # Aceita 'void' ou nada dentro dos parênteses
    if tokens[3]["token"] == "PARENTESE_FECHA":
        index = 4
    elif tokens[3]["token"] == "IDENTIFICADOR" and tokens[3]["value"] == "void" and tokens[4]["token"] == "PARENTESE_FECHA":
        index = 5
    else:
        return "Erro: Parâmetros da função 'main' inválidos."

    if tokens[index]["token"] != "CHAVE_ABRE":
        return f"Erro na linha {tokens[index]['linha']}: Esperado '{{' após a declaração da 'main', encontrado '{tokens[index]['value']}'."

    # Verifica o fechamento da chave
    # Para uma verificação mais rigorosa, é necessário analisar todo o conteúdo dentro das chaves
    # Aqui está uma verificação básica para o fechamento da chave
    for token in tokens[index:]:
        if token["token"] == "CHAVE_FECHA":
            return "Declaração da função 'main' válida."

    return "Erro: Bloco de código da função 'main' não termina corretamente (faltando '}')."


def analisar_atribuicao_variavel(tokens):
    if not tokens:
        return "Erro: Nenhum token fornecido para análise."

    # Deve começar com um identificador
    if tokens[0]["token"] != "IDENTIFICADOR":
        return f"Erro na linha {tokens[0]['linha']}: Esperado um identificador, encontrado '{tokens[0]['value']}'."

    # Seguido por um operador de atribuição
    if len(tokens) < 2 or tokens[1]["token"] != "ATRIBUICAO":
        return "Erro: Esperado um operador de atribuição após o identificador."

    # Após o operador de atribuição, deve haver uma expressão válida
    # Aqui estamos simplificando para qualquer sequência até encontrar um ponto e vírgula
    index = 2
    while index < len(tokens) and tokens[index]["token"] != "PONTO_VIRGULA":
        index += 1

    if index == len(tokens):
        return "Erro: Atribuição não terminada corretamente (faltando ponto e vírgula)."

    # A expressão da atribuição não deve estar vazia
    if index == 2:
        return "Erro: Nenhuma expressão de atribuição encontrada."

    return "Operação de atribuição válida."

def analisar_operacao_aritmetica(tokens):
    if not tokens:
        return "Erro: Nenhum token fornecido para análise."

    # Verifica se a expressão termina com um ponto e vírgula
    if tokens[-1]["token"] != "PONTO_VIRGULA":
        return "Erro: A expressão aritmética não termina com ponto e vírgula."

    # Remove o ponto e vírgula para análise da expressão
    tokens = tokens[:-1]

    # Verifica a validade básica da expressão
    esperado = {"NUMERO", "IDENTIFICADOR", "PARENTESE_ABRE"}
    for token in tokens:
        if token["token"] in esperado:
            if token["token"] == "PARENTESE_ABRE":
                esperado = {"NUMERO", "IDENTIFICADOR", "PARENTESE_ABRE"}
            elif token["token"] in {"NUMERO", "IDENTIFICADOR"}:
                esperado = {"OPERADOR_ARITMETICO", "PARENTESE_FECHA", "PONTO_VIRGULA"}
            continue

        if token["token"] == "OPERADOR_ARITMETICO":
            esperado = {"NUMERO", "IDENTIFICADOR", "PARENTESE_ABRE"}
            continue

        if token["token"] == "PARENTESE_FECHA":
            esperado = {"OPERADOR_ARITMETICO", "PARENTESE_FECHA", "PONTO_VIRGULA"}
            continue

        return f"Erro na linha {token['linha']}: Token inesperado '{token['value']}'."

    # Verifica se todos os parênteses foram fechados
    abertos = sum(1 for t in tokens if t["token"] == "PARENTESE_ABRE")
    fechados = sum(1 for t in tokens if t["token"] == "PARENTESE_FECHA")
    if abertos != fechados:
        return "Erro: Número desigual de parênteses abertos e fechados."

    return "Operação aritmética válida."

# Exemplo de uso
codigo_c = "(x + y) * (a / b);"
tokens = analisador_lexico(codigo_c)
print(tokens)
resultado = analisar_atribuicao_variavel(tokens)
print(resultado)
