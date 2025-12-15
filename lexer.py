import re
from rules import TOKEN_PATTERNS, TOKEN_KINDS, SYMBOLS, TYPE_KEYWORDS, CONTROL_KEYWORDS, SKIP_TOKENS
# TOKEN_KINDS is used to create tokens with the correct kind that the parser will later consume

class Token:
    """
    Represents a single lexical token from the source code.
    """
    def __init__(self, kind, value, pos):
        self.kind = kind # category of token
        self.value = value # what the token is exactly
        self.pos = pos # index in the original source string
        
    def __repr__(self):
        # string representation for debugging
        return f'Token({self.kind!r}, {self.value!r}, {self.pos})'


"""
Generator function that tokenizes Java source code into Python tokens.
Uses yield instead of return to produce tokens one at a time for memory efficiency.

Args: 
    src (str): The Java source code to tokenize.
    
Yields:
    Token: Individual tokens with kind, value, and position.
"""
def lex_java(src: str):
    # pre-compute combined lists once before the loop
    # avoids repreated work inside the loop
    patterns = {k: re.compile(v) for k, v in TOKEN_PATTERNS.items()}
    priority_keywords = TYPE_KEYWORDS + CONTROL_KEYWORDS
    skip_set = set(SKIP_TOKENS)
    priority_and_skip = set(priority_keywords + SKIP_TOKENS)
    
    i = 0
    n = len(src) 
    while i < n:
        matched = False
        
        # match type and control keywords first (highest priority)
        # ensures 'int' is tokenized as int_type, not identifier
        for name in priority_keywords:
            m = patterns[name].match(src, i) # try to match at current position
            if m:
                kind = TOKEN_KINDS[name]
                yield Token(kind, m.group(0), i)
                i = m.end() # move position to end of matched text
                matched = True
                break
        
        if matched: continue
        
        # skip, not consume whitespaces, comments and java specific constructs
        # that have no python equivalent
        for name in skip_set:
            m = patterns[name].match(src, i)
            if m:
                i = m.end()
                matched = True
                break
        
        if matched: continue
        
        # match all other token patterns
        for name in patterns:
            # skip patterns already handled
            if name in priority_and_skip:
                continue
            m = patterns[name].match(src, i)
            if m:
                kind = TOKEN_KINDS.get(name, name.lower())
                yield Token(kind, m.group(0), i)
                i = m.end()
                matched = True
                break
                
        if not matched:
            ch = src[i] # current character
            if ch in SYMBOLS:
                yield Token(SYMBOLS[ch], ch, i)
                i += 1
            else:
                line_num = src[:i].count('\n') + 1
                col_num = i - src.rfind('\n', 0, i)
                raise SyntaxError(f'Unexpected character {ch!r} at line {line_num}, column {col_num} (position {i})')
    
    yield Token("EOF", "", n) # end of file token 
