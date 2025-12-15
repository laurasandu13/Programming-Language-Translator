import argparse
import sys
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
    
    try: 
        with open(args.input, 'r', encoding='utf-8') as f:
            java_src = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied reading '{args.input}'.", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error reading '{args.input}': {e}", file=sys.stderr)
        sys.exit(1)
        
    try: 
        py_code = translate_str(java_src)
    except SyntaxError as e:
        print(f"Syntax error in Java code: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Translation error: {e}", file=sys.stderr)
        sys.exit(2)
    
    if args.dry_run or args.output is None:
        print(py_code)
    else:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(py_code)
            print(f"Successfully translated '{args.input}' to '{args.output}'")
        except PermissionError:
            print(f"Error: Permission denied writing to '{args.output}'.", file=sys.stderr)
            sys.exit(1)
        except IOError as e:
            print(f"Error warning to '{args.output}': {e}", file=sys.stderr)
            sys.exit(1)
            
        
    