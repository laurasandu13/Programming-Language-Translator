"""
Defines token patterns (regex), token kinds (categories), 
and specific Java constructs.
"""

PRINT_RECEIVER = 'System'
PRINT_FIELD = 'out'
PRINT_METHODS = ('println', 'print')

# TOKEN_PATTERNS: defines regex patterns to match Java language constructs
# order matters: more specific patterns come before more general ones
# according to python's 're' module behavior, patterns are matched in the order they are defined
# used by the lexer
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
    #string content 
    'STRING': r'"([^"\\]|\\.)*"',     # stops at first closing quote
    'CHAR_LITERAL': r"'(\\.|[^\\'])'",
    #variable name
    'IDENT': r'[A-Za-z_][A-Za-z_0-9]*',
    # numbers
    'FLOAT_NUMBER': r'\d+(\.\d+)?[fF]', 
    'NUMBER': r'\d+(\.\d+)?',
    # arithmetic operators
    'INCREMENT': r'\+\+',
    'PLUS': r'\+',
    'DECREMENT': r'\-\-',
    'MINUS': r'\-',
    'MULTIPLY': r'\*',
    'DIVIDE': r'\/',
    'MODULO': r'%',
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
    # delimiters
    'LBRACE': r'\{',
    'RBRACE': r'\}',
    'LPAREN': r'\(',  
    'RPAREN': r'\)',  
    'LBRACKET': r'\[',  
    'RBRACKET': r'\]',  
    'SEMI': r';',
    'COMMA': r',',
    'DOT': r'\.',
}

# to use in lexer
SKIP_TOKENS = ['WHITESPACE', 'LINE_COMMENT', 'BLOCK_COMMENT', 'CLASS_DECL', 'MAIN_DECL']
TYPE_KEYWORDS = ['INT', 'STRING_TYPE', 'CHAR', 'FLOAT', 'DOUBLE', 'BOOLEAN']
CONTROL_KEYWORDS = ['IF', 'ELSE', 'WHILE', 'FOR']
LITERAL_KINDS = ('string', 'char_literal', 'number', 'float_number', 'true_literal', 'false_literal')
PRINTABLE_KINDS = ('string', 'identifier', 'number', 'char_literal', 'float_number')
VALUE_KINDS = LITERAL_KINDS + ('identifier',)

# TOKEN_KINDS maps token pattern names to their semantic categories
# this provides a consistent way to refer to different token types in the parser
# used by the parser
TOKEN_KINDS = {
    # variable types
    'INT': 'int_type',
    'STRING_TYPE': 'string_type',
    'CHAR': 'char_type',
    'CHAR_LITERAL': 'char_literal',
    'FLOAT': 'float_type',
    'DOUBLE': 'double_type',
    'BOOLEAN': 'boolean_type',
    # literals
    'T_TRUE': 'true_literal',
    'T_FALSE': 'false_literal',
    'STRING': 'string',
    'FLOAT_NUMBER': 'float_number',
    'NUMBER': 'number',
    # loops and conditionals
    'IF': 'if_keyword',
    'ELSE': 'else_keyword',
    'WHILE': 'while_keyword',
    'FOR': 'for_keyword',
    # other stuff
    'IDENT': 'identifier', 
    # arithmetic operators
    'INCREMENT': 'increment_op',
    'PLUS': 'plus_op',
    'DECREMENT': 'decrement_op',
    'MINUS': 'minus_op',
    'MULTIPLY': 'multiply_op',
    'DIVIDE': 'divide_op',
    'MODULO': 'modulo_op',
    # logical operators
    'AND': 'and_op',
    'OR': 'or_op',
    # comparison opperators
    'ASSIGN': 'assign',
    'EQ': 'eq',
    'NEQ': 'neq',
    'LT': 'lt',
    'GT': 'gt',
    'LEQ': 'leq',
    'GEQ': 'geq',
    # delimiters
    'LBRACKET': 'left_bracket',
    'RBRACKET': 'right_bracket',
    'LBRACE': 'left_brace',
    'RBRACE': 'right_brace',
    'DOT': 'dot',
    'LPAREN': 'left_parenthesis',
    'RPAREN': 'right_parenthesis',
    'SEMI': 'semicolon',
    'COMMA': 'comma',
    'SINGLE_QUOTE': 'single_quote',
}   

TYPE_TOKEN_KINDS = tuple(TOKEN_KINDS[k] for k in TYPE_KEYWORDS)

# SYMBOLS provides a direct character-to-token-kind mapping for single-character symbols
# this is used when TOKEN_PATTERNS doesn't match
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
    ",": "comma",
}