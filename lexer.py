import re

class Token:
    def __init__(self, kind, value, pos):
        self.kind = kind # category of token
        self.value = value # what the token is exactly
        self.pos = pos # index in the original source string
                        # later i will modify this to line

# regex patterns for whitespaces, comments, braces etc.
whitespace = re.compile(r'[ \t\r\n]+')
line_comment = re.compile(r'//.*') 
block_comment = re.compile(r'/\*.*?\*/', re.DOTALL)
identifier = re.compile(r'[A-Za-z_][A-Za-z_0-9]*')
string = re.compile(r"\"(\\.|[^\'\\])*\"")

# dictionary of frequent symbols
symbols = {
    "(": "left_parenthesis", 
    ")": "right_parenthesis", 
    ";": "semicolon", 
    ".": "dot"
}

def lex_java(src: str):
    i = 0
    n = len(src) 
    while i < n:
        m = whitespace.match(src, i)
        if m: #runs only when a match is found
            i = m.end() # sets the scanning index at the end of the matched text
            continue
        
        m = line_comment.match(src, i)
        if m: 
            i = m.end() 
            continue 
        
        m = block_comment.match(src, i)
        if m: 
            i = m.end() 
            continue
        
        m = string.match(src, i)
        if m:
            yield Token("string", m.group(0), i) 
            i = m.end()
            continue
            
        m = identifier.match(src, i)
        if m:
            yield Token("identifier", m.group(0), i)
            i = m.end() 
            continue
            
        ch = src[i]
        if ch in symbols:
            yield Token(symbols[ch], ch, i)
            i += 1
            continue
        raise SyntaxError(f"Unexpected character at {i}: {ch!r}")
    
    yield Token("EOF", "", n) # end of file token 
