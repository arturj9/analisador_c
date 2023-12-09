import re

TOKENS = [
    {"token": "DECLARACAO_MAIN", "pattern": r"\s+main\s*"},
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
    int x;
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


#ANALISADOR SINTÁTICO
def analisar_declaracao_variavel(tokens):
    index = 0
    while index < len(tokens):
        token = tokens[index]

        if token["token"] == "TIPO_VARIAVEL":
            index += 1
            if index < len(tokens):
                # Verifica se o próximo token é uma declaração de função (como 'main')
                if tokens[index]["token"] == "DECLARACAO_MAIN":
                    while index < len(tokens) and tokens[index]["token"] != "PONTO_VIRGULA":
                        index += 1
                    if index < len(tokens):
                        index += 1  # Passa o ponto e vírgula

                # Verifica se o próximo token é um identificador (para declaração de variável)
                if tokens[index]["token"] == "IDENTIFICADOR":
                    index += 1
                    # Verifica se há atribuição
                    if index < len(tokens) and tokens[index]["token"] == "ATRIBUICAO":
                        index += 1  # Pula o operador de atribuição
                        # Processa a expressão de atribuição (simplificado)
                        if index < len(tokens) and (tokens[index]["token"] in ["NUMERO", "IDENTIFICADOR"]):
                            index += 1  # Pula o valor da atribuição
                        else:
                            return f"Erro: Esperado um valor para atribuição na linha {tokens[index]['linha']}", index
                    
                    # Verificar se há mais variáveis na mesma declaração
                    if index < len(tokens) and tokens[index]["token"] == "VIRGULA":
                        index += 1  # Pula a vírgula para processar a próxima variável
                        continue

                    if index < len(tokens) and tokens[index]["token"] == "PONTO_VIRGULA":
                        index += 1  # Pula o ponto e vírgula
                        break  # Encerra a análise desta declaração de variável
                    else:
                        return f"Erro: Esperado ';' ou ',' na linha {tokens[index]['linha']}", index
                else:
                    return f"Erro: Esperado identificador ou declaração de função após tipo de variável na linha {tokens[index]['linha']}", index
        else:
            # Continua se não for uma declaração de tipo de variável
            index += 1

    return "Análise de declaração de variável concluída sem erros"

def analisar_atribuicao_variavel(tokens):
    index = 0
    while index < len(tokens):
        token = tokens[index]

        if token["token"] == "IDENTIFICADOR":
            index += 1

            if index < len(tokens) and tokens[index]["token"] == "ATRIBUICAO":
                index += 1
                # Aqui você analisaria a expressão. Por simplicidade, vamos apenas avançar até o ponto e vírgula
                while index < len(tokens) and tokens[index]["token"] != "PONTO_VIRGULA":
                    index += 1

                if index < len(tokens) and tokens[index]["token"] == "PONTO_VIRGULA":
                    index += 1
                else:
                    return f"Erro: Esperado ';' ao final da atribuição na linha {tokens[index]['linha']}"
            else:
                return f"Erro: Esperado operador de atribuição após identificador na linha {tokens[index]['linha']}"

        else:
            index += 1

def analisar_declaracao_main(tokens):
    index = 0
    while index < len(tokens):
        token = tokens[index]

        # Verificar se é o início da função main
        if token["token"] == "DECLARACAO_MAIN" :
            token = tokens[index]
            if token["token"] == "DECLARACAO_MAIN":
                index += 1
                token = tokens[index]

                # Verificar parênteses abertos
                if token["token"] == "PARENTESE_ABRE":
                    index += 1
                    token = tokens[index]

                    # Verificar parênteses fechados
                    if token["token"] == "PARENTESE_FECHA":
                        index += 1
                        token = tokens[index]

                        # Verificar chaves abrindo o corpo da função
                        if token["token"] == "CHAVE_ABRE":
                            # Aqui, você analisaria o corpo da função. Por simplicidade, vamos apenas avançar até a chave de fechamento
                            while index < len(tokens) and tokens[index]["token"] != "CHAVE_FECHA":
                                index += 1

                            if index < len(tokens):
                                index += 1
                                return "Declaração da função main analisada sem erros"
                            else:
                                return "Erro: Chave de fechamento não encontrada para a função main"
                        else:
                            return "Erro: Esperado '{' após a declaração da função main"
                    else:
                        return "Erro: Esperado ')' após 'main('"
                else:
                    return "Erro: Esperado '(' após 'main'"
        else:
            index += 1

    return "Nenhuma declaração da função main encontrada"
def analisar_operacoes_aritmeticas(tokens):
    index = 0
    pilha_parenteses = []

    while index < len(tokens):
        token = tokens[index]

        if token["token"] in ["NUMERO", "IDENTIFICADOR"]:
            # Espera-se um operador aritmético ou um parêntese fechado após um número ou identificador
            index += 1
            if index < len(tokens) and tokens[index]["token"] not in ["SOMA", "SUBTRACAO", "MULTIPLICACAO", "DIVISAO", "PARENTESE_FECHA"]:
                return f"Erro: Operador ou ')' esperado após número/identificador na linha {token['linha']}"

        elif token["token"] in ["SOMA", "SUBTRACAO", "MULTIPLICACAO", "DIVISAO"]:
            # Espera-se um número, identificador ou parêntese aberto após um operador
            index += 1
            if index < len(tokens) and tokens[index]["token"] not in ["NUMERO", "IDENTIFICADOR", "PARENTESE_ABRE"]:
                return f"Erro: Número, identificador ou '(' esperado após operador na linha {token['linha']}"

        elif token["token"] == "PARENTESE_ABRE":
            pilha_parenteses.append(index)
            index += 1

        elif token["token"] == "PARENTESE_FECHA":
            if not pilha_parenteses:
                return f"Erro: Parêntese fechado ')' sem correspondente '(' na linha {token['linha']}"
            pilha_parenteses.pop()
            index += 1

        else:
            index += 1

    if pilha_parenteses:
        return f"Erro: Parêntese aberto '(' sem correspondente ')'"

    return "Análise de operações aritméticas concluída sem erros"
def analisar_condicao(tokens, index):
    # Implemente a lógica para analisar a condição. Por simplicidade, vamos apenas avançar até o parêntese de fechamento.
    while index < len(tokens) and tokens[index]["token"] != "PARENTESE_FECHA":
        index += 1
    return index + 1  # Retorna o índice após o parêntese de fechamento

def analisar_for_condicao(tokens, index):
    # Implemente a lógica para analisar a condição do 'for'. Por simplicidade, vamos apenas avançar até o parêntese de fechamento.
    while index < len(tokens) and tokens[index]["token"] != "PARENTESE_FECHA":
        index += 1
    return index + 1  # Retorna o índice após o parêntese de fechamento

def analisar_bloco(tokens, index):
    # Implemente a lógica para analisar o bloco. Por simplicidade, vamos apenas avançar até a chave de fechamento.
    while index < len(tokens) and tokens[index]["token"] != "CHAVE_FECHA":
        index += 1
    return index + 1  # Retorna o índice após a chave de fechamento

def analisar_lacos_condicionais(tokens):
    index = 0

    while index < len(tokens):
        token = tokens[index]

        if token["token"] in ["IF", "WHILE"]:
            # Verificar a estrutura: if/while (condição) {bloco}
            index += 1  # Avança além de 'if' ou 'while'
            if index < len(tokens) and tokens[index]["token"] == "PARENTESE_ABRE":
                index = analisar_condicao(tokens, index + 1)  # Análise da condição
                if index < len(tokens) and tokens[index]["token"] == "CHAVE_ABRE":
                    index = analisar_bloco(tokens, index + 1)  # Análise do bloco
                else:
                    return f"Erro: Esperado '' após condição na linha {token['linha']}"
            else:
                return f"Erro: Esperado '(' após 'if' ou 'while' na linha {token['linha']}"

        elif token["token"] == "FOR":
            # Verificar a estrutura: for (inicialização; condição; incremento) {bloco}
            index += 1  # Avança além de 'for'
            if index < len(tokens) and tokens[index]["token"] == "PARENTESE_ABRE":
                index = analisar_for_condicao(tokens, index + 1)  # Análise específica da condição do 'for'
                if index < len(tokens) and tokens[index]["token"] == "CHAVE_ABRE":
                    index = analisar_bloco(tokens, index + 1)  # Análise do bloco
                else:
                    return f"Erro: Esperado '' após condição na linha {token['linha']}"
            else:
                return f"Erro: Esperado '(' após 'for' na linha {token['linha']}"

        elif token["token"] == "ELSE":
            # Verificar a estrutura: else {bloco} ou else if (condição) {bloco}
            index += 1  # Avança além de 'else'
            if index < len(tokens) and tokens[index]["token"] == "CHAVE_ABRE":
                index = analisar_bloco(tokens, index + 1)  # Análise do bloco do 'else'
            elif index < len(tokens) and tokens[index]["token"] == "IF":
                continue  # Continua a análise para o 'else if'
            else:
                return f"Erro: Esperado '' ou 'if' após 'else' na linha {token['linha']}"

        else:
            index += 1

    return "Análise de laços condicionais concluída sem erros"

def analisar_expressoes_logicas(tokens):
    index = 0
    pilha_parenteses = []

    while index < len(tokens):
        token = tokens[index]

        if token["token"] in ["IDENTIFICADOR", "NUMERO"]:
            # Espera-se um operador lógico/comparação ou um parêntese fechado após um número/identificador
            index += 1
            if index < len(tokens) and tokens[index]["token"] not in ["E_LOGICO", "OU_LOGICO", "NAO_LOGICO", "IGUAL", "DIFERENTE", "MENOR_QUE", "MAIOR_QUE", "MENOR_OU_IGUAL", "MAIOR_OU_IGUAL", "PARENTESE_FECHA"]:
                return f"Erro: Operador lógico/comparação ou ')' esperado após número/identificador na linha {token['linha']}"

        elif token["token"] in ["E_LOGICO", "OU_LOGICO", "NAO_LOGICO", "IGUAL", "DIFERENTE", "MENOR_QUE", "MAIOR_QUE", "MENOR_OU_IGUAL", "MAIOR_OU_IGUAL"]:
            # Espera-se um número, identificador ou parêntese aberto após um operador
            index += 1
            if index < len(tokens) and tokens[index]["token"] not in ["NUMERO", "IDENTIFICADOR", "PARENTESE_ABRE"]:
                return f"Erro: Número, identificador ou '(' esperado após operador na linha {token['linha']}"

        elif token["token"] == "PARENTESE_ABRE":
            pilha_parenteses.append(index)
            index += 1

        elif token["token"] == "PARENTESE_FECHA":
            if not pilha_parenteses:
                return f"Erro: Parêntese fechado ')' sem correspondente '(' na linha {token['linha']}"
            pilha_parenteses.pop()
            index += 1

        else:
            index += 1

    if pilha_parenteses:
        return f"Erro: Parêntese aberto '(' sem correspondente ')'"

    return "Análise de expressões lógicas concluída sem erros"
def analisador_sintatico(codigo):
    # Primeiro, use o analisador léxico para obter os tokens
    tokens = analisador_lexico(codigo)
    if isinstance(tokens, str):
        return tokens  # Se houver erro na análise léxica, retorne a mensagem de erro

    # Inicializa o índice para percorrer a lista de tokens
    index = 0

    while index < len(tokens):
        token = tokens[index]

        if token["token"] == "TIPO_VARIAVEL":
            resultado = analisar_declaracao_variavel(tokens[index:])
            if resultado != "Análise de declaração de variável concluída sem erros":
                return resultado

        elif token["token"] == "IDENTIFICADOR":
            resultado = analisar_atribuicao_variavel(tokens[index:])
            if resultado != "Análise de atribuição de variável concluída sem erros":
                return resultado

        elif token["token"] in ["IF", "WHILE", "FOR", "ELSE"]:
            resultado = analisar_lacos_condicionais(tokens[index:])
            if resultado != "Análise de laços condicionais concluída sem erros":
                return resultado
            
        elif token["token"] == "PARENTESE_ABRE":
            resultado = analisar_operacoes_aritmeticas(tokens[index:])
            if resultado != "Análise de expressoes logicas concluída sem erros":
                return resultado
            
        elif token["token"] == "DECLARACAO_MAIN":
            resultado = analisar_declaracao_main(tokens[index:])
            if resultado != "Declaração da função main analisada sem erros":
                return resultado
        index += 1

    return "Análise sintática concluída sem erros"

# Aqui você incluiria o código do analisador léxico e das outras funções de análise
print(analisador_sintatico(code))