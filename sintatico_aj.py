from lexico_aj import analisador_lexico

# Syntax Tree Node
class SyntaxTreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)

# Global variables
tokens = []
current_token = None
tree = SyntaxTreeNode('<program>')

# Helper functions
def match(token_type):
    global current_token
    if current_token and current_token['token'] == token_type:
        try:
            current_token = tokens.pop(0)
        except:
            ...
        return True
    return False

def error(message):
    raise Exception(f"Syntax Error: {message}")

# Parsing functions
def parse_program():
    global tree
    while tokens:
        if current_token['token'] == 'TIPO_VARIAVEL' and tokens[0]['token'] == 'FUNCAO_MAIN':
            parse_function_definition()
        elif current_token['token'] == 'TIPO_VARIAVEL':
            parse_declaration()
        else:
            error("Unexpected token in <program>")
    return tree

def parse_declaration():
    global tree
    tree.add_child(SyntaxTreeNode('<declaration>'))
    parse_type_specifier()
    parse_declarator_list()

def parse_type_specifier():
    global tree
    tree.add_child(SyntaxTreeNode('<type_specifier>'))
    if not match('TIPO_VARIAVEL'):
        error("Expected type specifier in <type_specifier>")

def parse_declarator_list():
    global tree
    tree.add_child(SyntaxTreeNode('<declarator_list>'))
    parse_declarator()

def parse_declarator():
    global tree
    tree.add_child(SyntaxTreeNode('<declarator>'))
    if not match('FUNCAO_MAIN'):
        parse_statement()

def parse_function_definition():
    global tree
    tree.add_child(SyntaxTreeNode('<function_definition>'))
    parse_type_specifier()
    parse_declarator()
    if not match('PARENTESE_ABRE'):
        error("Expected '(' in <function_definition>")
    # parse_parameter_list()
    if not match('PARENTESE_FECHA'):
        error("Expected ')' in <function_definition>")
    parse_compound_statement()

# def parse_parameter_list():
#     global tree
#     tree.add_child(SyntaxTreeNode('<parameter_list>'))
#     parse_parameter_declaration()
#     while match('VIRGULA'):
#         parse_parameter_declaration()

# def parse_parameter_declaration():
#     global tree
#     tree.add_child(SyntaxTreeNode('<parameter_declaration>'))
#     parse_type_specifier()
#     parse_declarator()

def parse_compound_statement():
    global tree
    tree.add_child(SyntaxTreeNode('<compound_statement>'))
    if match('CHAVE_ABRE'):
        while current_token['token'] == 'TIPO_VARIAVEL':
            parse_declaration()
        while current_token['token'] in ('TIPO_VARIAVEL','IDENTIFICADOR', 'NUMERO', 'IF', 'WHILE', 'FOR'):
            parse_statement()
        if not match('CHAVE_FECHA'):
            error("Expected '}' in <compound_statement>")
    else:
        error("Expected '{' in <compound_statement>")

def parse_statement():
    global tree
    tree.add_child(SyntaxTreeNode('<statement>'))
    if current_token['token'] == 'TIPO_VARIAVEL':
        parse_declaration()
    elif current_token['token'] == 'IDENTIFICADOR':
        parse_assignment_statement()
    elif current_token['token'] == 'IF':
        parse_conditional_statement()
    elif current_token['token'] == 'WHILE':
        parse_while_loop_statement()
    elif current_token['token'] == 'FOR':
        parse_for_loop_statement()

def parse_assignment_statement():
    global tree
    tree.add_child(SyntaxTreeNode('<assignment_statement>'))
    parse_identifier()
    if not match('ATRIBUICAO'):
        error("Expected '=' in <assignment_statement>")
    parse_expression()
    if not match('PONTO_VIRGULA'):
        error("Expected ';' in <declaration>")

def parse_conditional_statement():
    global tree
    tree.add_child(SyntaxTreeNode('<conditional_statement>'))
    if not match('IF'):
        error("Expected 'if' in <conditional_statement>")
    if not match('PARENTESE_ABRE'):
        error("Expected '(' in <conditional_statement>")
    parse_logical_expression()
    if not match('PARENTESE_FECHA'):
        error("Expected ')' in <conditional_statement>")
    parse_compound_statement()
    if match('ELSE'):
        parse_compound_statement()

def parse_while_loop_statement():
    global tree
    tree.add_child(SyntaxTreeNode('<while_loop_statement>'))
    if not match('WHILE'):
        error("Expected 'while' in <while_loop_statement>")
    if not match('PARENTESE_ABRE'):
        error("Expected '(' in <while_loop_statement>")
    parse_logical_expression()
    if not match('PARENTESE_FECHA'):
        error("Expected ')' in <while_loop_statement>")
    parse_compound_statement()

def parse_for_loop_statement():
    global tree
    tree.add_child(SyntaxTreeNode('<for_loop_statement>'))
    if not match('FOR'):
        error("Expected 'for' in <for_loop_statement>")
    if not match('PARENTESE_ABRE'):
        error("Expected '(' in <for_loop_statement>")
    # parse_assignment_statement()
    # if not match('PONTO_VIRGULA'):
    #     error("Expected ';' in <for_loop_statement>")
    parse_logical_expression()
    # if not match('PONTO_VIRGULA'):
    #     error("Expected ';' in <for_loop_statement>")
    # parse_assignment_statement()
    if not match('PARENTESE_FECHA'):
        error("Expected ')' in <for_loop_statement>")
    parse_compound_statement()

def parse_expression():
    global tree
    tree.add_child(SyntaxTreeNode('<expression>'))
    parse_term()
    while current_token['token'] in ('SOMA', 'SUBTRACAO'):
        match('SOMA')
        match('SUBTRACAO')
        parse_term()

def parse_term():
    global tree
    tree.add_child(SyntaxTreeNode('<term>'))
    parse_factor()
    while current_token['token'] in ('MULTIPLICACAO', 'DIVISAO'):
        match('MULTIPLICACAO')
        match('DIVISAO')
        parse_factor()

def parse_factor():
    global tree
    tree.add_child(SyntaxTreeNode('<factor>'))
    if current_token['token'] == 'IDENTIFICADOR':
        parse_identifier()
    elif current_token['token'] == 'NUMERO':
        parse_number()
    elif match('PARENTESE_ABRE'):
        parse_expression()
        if not match('PARENTESE_FECHA'):
            error("Expected ')' in <factor>")
    else:
        error("Unexpected token in <factor>")

def parse_logical_expression():
    global tree
    tree.add_child(SyntaxTreeNode('<logical_expression>'))
    while current_token['token']!='PARENTESE_FECHA':
        if current_token['token'] == 'IDENTIFICADOR':
            parse_identifier()
        else:
            parse_logical_operator()

def parse_logical_operator():
    global tree
    tree.add_child(SyntaxTreeNode('<logical_operator>'))
    if not match('E_LOGICO') and not match('OU_LOGICO') and not match('NAO_LOGICO'):
        error("Expected relational operator in <logical_operator>")

# def parse_relational_operator():
#     global tree
#     tree.add_child(SyntaxTreeNode('<relational_operator>'))
#     if not match('IGUAL') and not match('DIFERENTE') and not match('MENOR_QUE') \
#             and not match('MAIOR_QUE') and not match('MENOR_OU_IGUAL') and not match('MAIOR_OU_IGUAL'):
#         error("Expected relational operator in <relational_operator>")

def parse_identifier():
    global tree
    tree.add_child(SyntaxTreeNode('<identifier>'))
    if not match('IDENTIFICADOR'):
        error("Expected identifier in <identifier>")

def parse_number():
    global tree
    tree.add_child(SyntaxTreeNode('<number>'))
    if not match('NUMERO'):
        error("Expected number in <number>")

# Example usage
code = '''
int main(){
    for(!g){
        if(a&&f){
            g=9;
        }
    }
    while(!a){
        int a = 5;
    }
    if(!a||b){
        f = 4;
        int d = (45+B)/f*5;
    }else{
        f=5;
    }
    int b = 5;
}
'''


tokens = analisador_lexico(code)
current_token = tokens.pop(0)

syntax_tree = parse_program()

# Print the syntax tree (for debugging purposes)
def print_tree(node, indent=0):
    print('  ' * indent + node.value)
    for child in node.children:
        print_tree(child, indent + 1)

print_tree(syntax_tree)
