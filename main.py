from analisador_sintatico import analisador_sintatico

code = open("example.txt", 'r', encoding='utf-8').read()
analisador_sintatico(code)