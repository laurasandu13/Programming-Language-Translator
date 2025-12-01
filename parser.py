from rules import PRINT_RECEIVER, PRINT_FIELD, PRINT_METHODS
from dataclasses import dataclass
from typing import List

@dataclass
class Module:
    body: List[object]

@dataclass
class Print:
    args: List[str]

class Cursor:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.i = 0
    
    # look at future tokens without removing them from the token stream
    def peek(self, k = 0):
        return self.tokens[self.i + k]
    
    # consume the current token
    def pop(self):
        t = self.tokens[self.i]
        self.i += 1 
        return t
    
    # demand specific token
    def expect(self, kind, value = None):
        t = self.pop()
        if t.kind != kind or (value is not None and t.value != value):
            raise SyntaxError(f"Expected {kind} {value or ''} at {t.pos}, got {t.kind} {t.value!r}")
        return t

def parse_module(tokens):
    c = Cursor(tokens)
    body = []
    while c.peek().kind != "EOF":
        stmt = parse_statement(c)
        if stmt: 
            body.append(stmt)
    return Module(body=body)

def parse_statement(c: Cursor):
    peek = c.peek()
    if (peek.kind == 'identifier' and peek.value == PRINT_RECEIVER and
        c.peek(1).kind == 'dot' and c.peek(2).value == PRINT_FIELD and
        c.peek(3).kind == 'dot' and c.peek(4).value in PRINT_METHODS):
        return parse_print(c)
    
    while c.peek().kind not in ('semicolon', 'EOF'):
        c.pop()
    if c.peek().kind == 'semicolon':
        c.pop()
    return None 

def parse_print(c: Cursor):
    c.expect("identifier", PRINT_RECEIVER)
    c.expect("dot", '.')          
    c.expect("identifier", PRINT_FIELD)
    c.expect("dot", '.')
    name = c.expect("identifier").value
    if name not in PRINT_METHODS:
        raise SyntaxError(f'Expected {PRINT_METHODS}, got {name}')
    c.expect("left_parenthesis", '(') 
    arg_tok = c.expect("string")
    c.expect("right_parenthesis", ')')
    c.expect("semicolon", ';')
    return Print([arg_tok.value])

