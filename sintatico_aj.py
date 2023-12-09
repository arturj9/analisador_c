from lexico_aj import analisador_lexico

def analisador_sintatico(code):

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
        nonlocal current_token
        if current_token and current_token['token'] == token_type:
            try:
                current_token = tokens.pop(0)
            except IndexError:
                ...
            return True
        return False

    def error(message):
        raise Exception(f"Syntax Error: {message} in line {current_token['linha']-1}")

    # Parsing functions
    def parse_program(tree):
        while tokens:
            if current_token['token'] == 'TIPO_VARIAVEL' and tokens[0]['token'] == 'FUNCAO_MAIN':
                parse_function_definition(tree)
            elif current_token['token'] == 'TIPO_VARIAVEL':
                parse_declaration(tree)
            else:
                error("Unexpected token in <program>")
        return tree

    def parse_declaration(parent):
        subtree = SyntaxTreeNode('<declaration>')
        parent.add_child(subtree)
        parse_type_specifier(subtree)
        parse_declarator_list(subtree)

    def parse_type_specifier(parent):
        parent.add_child(SyntaxTreeNode('<type_specifier>'))
        if not match('TIPO_VARIAVEL'):
            error("Expected type specifier in <type_specifier>")

    def parse_declarator_list(parent):
        parent.add_child(SyntaxTreeNode('<declarator_list>'))
        parse_declarator(parent)

    def parse_declarator(parent):
        subtree = SyntaxTreeNode('<declarator>')
        parent.add_child(subtree)
        if not match('FUNCAO_MAIN'):
            parse_statement(subtree)

    def parse_function_definition(parent):
        subtree = SyntaxTreeNode('<function_definition>')
        parent.add_child(subtree)
        parse_type_specifier(subtree)
        parse_declarator(subtree)
        if not match('PARENTESE_ABRE'):
            error("Expected '(' in <function_definition>")
        # parse_parameter_list()
        if not match('PARENTESE_FECHA'):
            error("Expected ')' in <function_definition>")
        parse_compound_statement(subtree)

    def parse_compound_statement(parent):
        subtree = SyntaxTreeNode('<compound_statement>')
        parent.add_child(subtree)
        if match('CHAVE_ABRE'):
            while current_token['token'] == 'TIPO_VARIAVEL':
                parse_declaration(subtree)
            while current_token['token'] in ('TIPO_VARIAVEL', 'IDENTIFICADOR', 'NUMERO', 'IF', 'WHILE', 'FOR'):
                parse_statement(subtree)
            if not match('CHAVE_FECHA'):
                error("Expected '}' in <compound_statement>")
        else:
            error("Expected '{' in <compound_statement>")

    def parse_statement(parent):
        subtree = SyntaxTreeNode('<statement>')
        parent.add_child(subtree)
        if current_token['token'] == 'TIPO_VARIAVEL':
            parse_declaration(subtree)
        elif current_token['token'] == 'IDENTIFICADOR':
            parse_assignment_statement(subtree)
        elif current_token['token'] == 'IF':
            parse_conditional_statement(subtree)
        elif current_token['token'] == 'WHILE':
            parse_while_loop_statement(subtree)
        elif current_token['token'] == 'FOR':
            parse_for_loop_statement(subtree)

    def parse_assignment_statement(parent):
        subtree = SyntaxTreeNode('<assignment_statement>')
        parent.add_child(subtree)
        parse_identifier(subtree)
        if not match('ATRIBUICAO'):
            error("Expected '=' in <assignment_statement>")
        parse_expression(subtree)
        if not match('PONTO_VIRGULA'):
            error("Expected ';' in <declaration>")

    def parse_conditional_statement(parent):
        subtree = SyntaxTreeNode('<conditional_statement>')
        parent.add_child(subtree)
        if not match('IF'):
            error("Expected 'if' in <conditional_statement>")
        if not match('PARENTESE_ABRE'):
            error("Expected '(' in <conditional_statement>")
        parse_logical_expression(subtree)
        if not match('PARENTESE_FECHA'):
            error("Expected ')' in <conditional_statement>")
        parse_compound_statement(subtree)
        if match('ELSE'):
            parse_compound_statement(subtree)

    def parse_while_loop_statement(parent):
        subtree = SyntaxTreeNode('<while_loop_statement>')
        parent.add_child(subtree)
        if not match('WHILE'):
            error("Expected 'while' in <while_loop_statement>")
        if not match('PARENTESE_ABRE'):
            error("Expected '(' in <while_loop_statement>")
        parse_logical_expression(subtree)
        if not match('PARENTESE_FECHA'):
            error("Expected ')' in <while_loop_statement>")
        parse_compound_statement(subtree)

    def parse_for_loop_statement(parent):
        subtree = SyntaxTreeNode('<for_loop_statement>')
        parent.add_child(subtree)
        if not match('FOR'):
            error("Expected 'for' in <for_loop_statement>")
        if not match('PARENTESE_ABRE'):
            error("Expected '(' in <for_loop_statement>")
        # parse_assignment_statement()
        # if not match('PONTO_VIRGULA'):
        #     error("Expected ';' in <for_loop_statement>")
        parse_logical_expression(subtree)
        # if not match('PONTO_VIRGULA'):
        #     error("Expected ';' in <for_loop_statement>")
        # parse_assignment_statement()
        if not match('PARENTESE_FECHA'):
            error("Expected ')' in <for_loop_statement>")
        parse_compound_statement(subtree)

    def parse_expression(parent):
        subtree = SyntaxTreeNode('<expression>')
        parent.add_child(subtree)
        parse_term(subtree)
        while current_token['token'] in ('SOMA', 'SUBTRACAO'):
            match('SOMA')
            match('SUBTRACAO')
            parse_term(subtree)

    def parse_term(parent):
        subtree = SyntaxTreeNode('<term>')
        parent.add_child(subtree)
        parse_factor(subtree)
        while current_token['token'] in ('MULTIPLICACAO', 'DIVISAO'):
            match('MULTIPLICACAO')
            match('DIVISAO')
            parse_factor(subtree)

    def parse_factor(parent):
        subtree = SyntaxTreeNode('<factor>')
        parent.add_child(subtree)
        if current_token['token'] == 'IDENTIFICADOR':
            parse_identifier(subtree)
        elif current_token['token'] == 'NUMERO':
            parse_number(subtree)
        elif match('PARENTESE_ABRE'):
            parse_expression(subtree)
            if not match('PARENTESE_FECHA'):
                error("Expected ')' in <factor>")
        else:
            error("Unexpected token in <factor>")

    def parse_logical_expression(parent):
        subtree = SyntaxTreeNode('<logical_expression>')
        parent.add_child(subtree)
        while current_token['token'] != 'PARENTESE_FECHA':
            if current_token['token'] == 'IDENTIFICADOR':
                parse_identifier(subtree)
            else:
                parse_logical_operator(subtree)

    def parse_logical_operator(parent):
        subtree = SyntaxTreeNode('<logical_operator>')
        parent.add_child(subtree)
        if not match('E_LOGICO') and not match('OU_LOGICO') and not match('NAO_LOGICO'):
            error("Expected relational operator in <logical_operator>")

    def parse_identifier(parent):
        subtree = SyntaxTreeNode('<identifier>')
        parent.add_child(subtree)
        if not match('IDENTIFICADOR'):
            error("Expected identifier in <identifier>")

    def parse_number(parent):
        subtree = SyntaxTreeNode('<number>')
        parent.add_child(subtree)
        if not match('NUMERO'):
            error("Expected number in <number>")

    tokens = analisador_lexico(code)
    try:
        current_token = tokens.pop(0)
        syntax_tree = parse_program(tree)

        # Print the syntax tree (for debugging purposes)
        def print_tree(node, indent=0):
            print('  ' * indent + node.value)
            for child in node.children:
                print_tree(child, indent + 1)


        print_tree(syntax_tree)
    except:
        print(tokens)
        


    
