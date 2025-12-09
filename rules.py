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
    # variable types
    'INT': r'\bint\b',
    'STRING_TYPE': r'\bString\b',
    'CHAR': r"\bchar\b",
    'FLOAT': r'\bfloat\b',
    'DOUBLE': r'\bdouble\b',
    'BOOLEAN': r'\bboolean\b',
    'T_TRUE': r'\btrue\b',
    'T_FALSE': r'\bfalse\b',
    #variable name
    'IDENT': r'[A-Za-z_][A-Za-z_0-9]*',
    #string content 
    'STRING': r"\"(\\.|[^\'\\])*\"",
    'CHAR_LITERAL': r"'(\\.|[^\\'])'",
    'FLOAT_NUMBER': r'\d+(\.\d+)?[fF]', 
    'NUMBER': r'\d+(\.\d+)?',
    # operators and other characters
    'ASSIGN': r'=',
    'EQ': r'==',
    'LBRACE': r'{',
    'RBRACE': r'}',
    'DOT': r'\.',
}

TOKEN_KINDS = {
    # variable types
    'INT': 'int_type',
    'STRING_TYPE': 'string_type',
    'CHAR': 'char_type',
    'CHAR_LITERAL': 'char_literal',
    'FLOAT': 'float_type',
    'DOUBLE': 'double_type',
    'BOOLEAN': 'boolean_type',
    'T_TRUE': 'true_literal',
    'T_FALSE': 'false_literal',
    # other stuff
    'IDENT': 'identifier', 
    'STRING': 'string',
    'FLOAT_NUMBER': 'float_number',
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
    'SINGLE_QUOTE': 'single_quote',
}   

SYMBOLS = {
    "(": "left_parenthesis", 
    ")": "right_parenthesis", 
    ";": "semicolon", 
    ".": "dot",
    "[": "left_bracket",
    "]": "right_bracket",
    "'": "single-quote",
}