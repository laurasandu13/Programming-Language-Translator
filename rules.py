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
    # loops and conditionals
    'IF': r'\bif\b',
    'ELSE': r'\belse\b',
    'WHILE': r'\bwhile\b',
    'FOR': r'\bfor\b',
    #variable name
    'IDENT': r'[A-Za-z_][A-Za-z_0-9]*',
    #string content 
    'STRING': r'"([^"\\]|\\.)*"',     # stops at first closing quote
    'CHAR_LITERAL': r"'(\\.|[^\\'])'",
    'FLOAT_NUMBER': r'\d+(\.\d+)?[fF]', 
    'NUMBER': r'\d+(\.\d+)?',
    'INCREMENT': r'\+\+',
    'PLUS': r'\+',
    'DECREMENT': r'\-\-',
    'MINUS': r'\-',
    # logical operators
    'AND': r'&&',
    'OR': r'\|\|',
    # operators
    'EQ': r'==',
    'NEQ': r'!=',
    'LEQ': r'<=',
    'GEQ': r'>=',
    'LT': r'<',
    'GT': r'>',
    'ASSIGN': r'=',
    # other characters
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
    'INCREMENT': 'increment_op',
    'PLUS': 'plus_op',
    'DECREMENT': 'decrement_op',
    'MINUS': 'minus_op',
    # loops and conditionals
    'IF': 'if_keyword',
    'ELSE': 'else_keyword',
    'WHILE': 'while_keyword',
    'FOR': 'for_keyword',
    # other stuff
    'IDENT': 'identifier', 
    'STRING': 'string',
    'FLOAT_NUMBER': 'float_number',
    'NUMBER': 'number',
    # logical operators
    'AND': 'and_op',
    'OR': 'or_op',
    # operators and other characters
    'ASSIGN': 'assign',
    'EQ': 'eq',
    'NEQ': 'neq',
    'LT': 'lt',
    'GT': 'gt',
    'LEQ': 'leq',
    'GEQ': 'geq',
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
    "{": "left_brace",
    "}": "right_brace",
}