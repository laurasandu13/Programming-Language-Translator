import re
from rules import TOKEN_PATTERNS, TOKEN_KINDS, SYMBOLS

class Token:
    def __init__(self, kind, value, pos):
        self.kind = kind # category of token
        self.value = value # what the token is exactly
        self.pos = pos # index in the original source string
                        # later i will modify this to line

def lex_java(src: str):
    patterns = {k: re.compile(v) for k, v in TOKEN_PATTERNS.items()}
    symbols = {s: t for s, t in SYMBOLS.items()}
    
    i = 0
    n = len(src) 
    while i < n:
        matched = False
        
        for name, regex in patterns.items():
            m = regex.match(src, i)
            if m:
                if name in ('WHITESPACE', 'LINE_COMMENT', 'BLOCK_COMMENT', 
                            'CLASS_DECL', 'MAIN_DECL'):
                    i = m.end()
                    matched = True
                    break
                else:
                    kind = TOKEN_KINDS.get(name, name.lower())
                    yield Token(kind, m.group(0), i)
                    i = m.end()
                    matched =  True
                    break
                
        if not matched:
            ch = src[i]
            if ch in symbols:
                yield Token(symbols[ch], ch, i)
                i += 1
            else:
                raise SyntaxError(f'Unexpected character at {i}: {ch!r}')
    
    yield Token("EOF", "", n) # end of file token 
