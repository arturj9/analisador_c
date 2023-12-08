import re

# Definição de tokens
tokens = [
    ('INT', r'int'),
    ('CHAR', r'char'),
    ('FLOAT', r'float'),
    ('DOUBLE', r'double'),
    ('MAIN', r'main'),
    ('IF', r'if'),
    ('ELSE', r'else'),
    ('WHILE', r'while'),
    ('FOR', r'for'),
    ('IDENTIFICADOR', r'[a-zA-Z_]\w*'),
    ('ASSOCIACAO', r'='),
    ('ARITEMTICOS_OP', r'\+|\-|\*|\/'),
    ('RELACIONAIS_OP', r'==|!=|<|>|<=|>='),
    ('LOGICOS_OP', r'&&|\|\|'),
    ('NUMERO', r'\d+(\.\d+)?'),
    ('PARENTESE_E', r'\('),
    ('PARENTESE_D', r'\)'),
    ('PONTO_E_VIRGULA', r';'),
    ('CHAVE_E', r'{'),
    ('CHAVE_D', r'}'),
    ('VURGULA', r','),
]

# Exemplo de código C
code = '''
int main() {
    int bola, y;
    bola = 5;
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

# Função para identificar tokens no código
def tokenize(code):
    for token in tokens:
        name, pattern = token
        regex = re.compile(pattern)
        match = regex.search(code)
        if match:
            yield (name, match.group())
            code = regex.sub('', code, 1)

# Testando a função de tokenize
for token in tokenize(code):
    print(token)
