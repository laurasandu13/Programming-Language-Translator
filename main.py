from lexer import lex_java
from parser import parse_module
from emitter import emit_module

def translate_str(java_src: str) -> str:
    tokens = list(lex_java(java_src))
    mod = parse_module(tokens)
    return emit_module(mod)