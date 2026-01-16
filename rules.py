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
    'CLASS_DECL': r'\bpublic\s+class\s+[A-Za-z_][A-Za-z_0-9]*\s*\{',
    'NEW': r'\bnew\b',
    'THIS': r'\bthis\b',
    # 'MAIN_DECL': r'\bpublic\s+static\s+void\s+main\s*\([^)]*\)\s*\{?',
    # USER INPUT
    # scanner import and object creation
    'SCANNER_IMPORT': r'\bimport\s+java\.util\.Scanner\s*;',
    'SCANNER_CREATE': r'\bScanner\s+[A-Za-z_][A-Za-z_0-9]*\s*=\s*new\s+Scanner\s*\(\s*System\.in\s*\)\s*;',
    'SCANNER_CLOSE': r'[A-Za-z_][A-Za-z_0-9]*\.close\s*\(\s*\)\s*;',
    # scanner input methods
    'SCANNER_NEXTLINE': r'\.nextLine\s*\(\s*\)',
    'SCANNER_NEXTINT': r'\.nextInt\s*\(\s*\)',
    'SCANNER_NEXTDOUBLE': r'\.nextDouble\s*\(\s*\)',
    'SCANNER_NEXTFLOAT': r'\.nextFloat\s*\(\s*\)',
    'SCANNER_NEXT': r'\.next\s*\(\s*\)',
    # method/function keywords
    'VOID': r'\bvoid\b',
    'RETURN': r'\breturn\b',
    'PUBLIC': r'\bpublic\b',
    'PRIVATE': r'\bprivate\b',
    'PROTECTED': r'\bprotected\b',
    'STATIC': r'\bstatic\b',
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
    # switch case
    'SWITCH': r'\bswitch\b',
    'CASE': r'\bcase\b',
    'DEFAULT': r'\bdefault\b',
    'BREAK': r'\bbreak\b',
    'COLON': r':',
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
SKIP_TOKENS = ['WHITESPACE', 'LINE_COMMENT', 'BLOCK_COMMENT', 
               'SCANNER_IMPORT', 'SCANNER_CREATE', 'SCANNER_CLOSE', 'PUBLIC', 'PRIVATE', 
               'PROTECTED', 'STATIC']
TYPE_KEYWORDS = ['INT', 'STRING_TYPE', 'CHAR', 'FLOAT', 'DOUBLE', 'BOOLEAN']
CONTROL_KEYWORDS = ['IF', 'ELSE', 'WHILE', 'FOR', 'SWITCH', 'CASE', 'DEFAULT', 'BREAK']
LITERAL_KINDS = ('string', 'char_literal', 'number', 'float_number', 'true_literal', 'false_literal')
PRINTABLE_KINDS = ('string', 'identifier', 'number', 'char_literal', 'float_number')
VALUE_KINDS = LITERAL_KINDS + ('identifier',)

# TOKEN_KINDS maps token pattern names to their semantic categories
# this provides a consistent way to refer to different token types in the parser
TOKEN_KINDS = {
    # user input methods
    'SCANNER_NEXTLINE': 'scanner_nextline',
    'SCANNER_NEXTINT': 'scanner_nextint',
    'SCANNER_NEXTDOUBLE': 'scanner_nextdouble',
    'SCANNER_NEXTFLOAT': 'scanner_nextfloat',
    'SCANNER_NEXT': 'scanner_next',
    # class keywords
    'NEW': 'new_keyword',
    'THIS': 'this_keyword',
    # method/function keywords
    'VOID': 'void_type',
    'RETURN': 'return_keyword',
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
    # switch case
    'SWITCH': 'switch_keyword',
    'CASE': 'case_keyword',
    'DEFAULT': 'default_keyword',
    'BREAK': 'break_keyword',
    'COLON': 'colon',
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
FUNCTION_RETURN_TYPES = TYPE_TOKEN_KINDS + ('void_type',)

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
    ":": "colon",
}