PRINT_RECEIVER = 'System'
PRINT_FIELD = 'out'
PRINT_METHODS = ('println', 'print')

TOKEN_PATTERNS = {
    # things to always skip
    'WHITESPACE': r'[ \t\r\n]+',
    'LINE_COMMENT': r'//.*',
    'BLOCK_COMMENT': r'/\*.*?\*/',
        # main file declaration in java
    'CLASS_DECL': r'\bpublic\s+class\s+[A-Za-z_][A-Za-z_0-9]*\s*{?',
    'MAIN_DECL': r'\bpublic\s+static\s+void\s+main\s*\(\s*String\s*\[\s*\]\s*args\s*\)\s*{?',
    'IDENT': r'[A-Za-z_][A-Za-z_0-9]*', #variable name
    'STRING': r"\"(\\.|[^\'\\])*\"", #string content
    'NUMBER': r'\d+(\.\d+)?',
    # operators and other characters
    'ASSIGN': r'=',
    'EQ': r'==',
    'LBRACE': r'{',
    'RBRACE': r'}',
    'DOT': r'\.',
}

TOKEN_KINDS = {
    'IDENT': 'identifier', 
    'STRING': 'string',
    'NUMBER': 'number',
    # operators and other characters
    'ASSIGN': 'assign',
    'EQ': 'eq',
    'LBRACKET': 'left_bracket',
    'RBRACKET': 'right_bracket',
    'LBRACE': 'left_brace',
    'RBRACE': 'right_brace',
    'DOT': 'dot',
    'LPAREN': 'left_parenthesis',
    'RPAREN': 'right_parenthesis',
    'SEMI': 'semicolon',
}   

SYMBOLS = {
    "(": "left_parenthesis", 
    ")": "right_parenthesis", 
    ";": "semicolon", 
    ".": "dot",
    "[": "left_bracket",
    "]": "right_bracket",
}