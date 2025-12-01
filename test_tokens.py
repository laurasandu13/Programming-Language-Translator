import sys
from lexer import lex_java

java_file = sys.argv[1]
with open(java_file) as f:
    src = f.read()

print("TOKENS:")
for i, t in enumerate(lex_java(src)):
    print(f"{i:2d}: {t.kind:12s} '{t.value}' at {t.pos}")
