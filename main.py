from lexer import lex_java
from parser import parse_module
from emitter import emit_module

def translate_str(java_src: str) -> str:
    tokens = list(lex_java(java_src))
    mod = parse_module(tokens)
    return emit_module(mod)

# simple test for a print statement
if __name__ == '__main__':
    java_src = 'System.out.println("Hello");'
    py_out = translate_str(java_src)
    print(py_out)