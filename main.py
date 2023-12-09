from analisador_sintatico import analisador_sintatico

 # Example usage
code = '''int main(){
    int x = 5;
    if(f && s){
        x = 4;
    }
}
'''

analisador_sintatico(code)