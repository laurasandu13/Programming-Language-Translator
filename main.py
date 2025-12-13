import argparse
from lexer import lex_java
from parser import parse_module
from emitter import emit_module

def translate_str(java_src: str) -> str:
    tokens = list(lex_java(java_src))
    mod = parse_module(tokens)
    return emit_module(mod)    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Translate Java code to Python'
    )
    # requires the user to pass an input file path
    parser.add_argument(
        'input',
        help='Path to the input Java source file.'
    )
    
    parser.add_argument(
        'output',
        nargs='?', #output may be absent
        help='Path to the output Python file. If omitted, prints to stdout.'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Print translated code instead of writing to a file.'
    )
    
    args = parser.parse_args()
    
    with open(args.input, 'r', encoding='utf-8') as f:
        java_src = f.read()
        
    py_code = translate_str(java_src)
    
    if args.dry_run or args.output is None:
        print(py_code)
    else:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(py_code)