from rules import PRINT_RECEIVER, PRINT_FIELD, PRINT_METHODS
from dataclasses import dataclass
from typing import List

@dataclass
class Module:
    body: List[object]

@dataclass
class Print:
    args: List[str]
    
@dataclass
class Variable:
    name: str
    value: str
    type_hint: str
    
@dataclass
class VarUpdate:
    name: str # variable being updated
    delta: int # amount to increment/decrement by
    
@dataclass
class BinaryCondition: #variable for condition in if statement
    left: str
    # when the condition is a bool/var name, 
    # oeprator and right are empty strings
    operator: str
    right: str    
    
@dataclass
class LogicalCondition:
    left: object #binary condition or logical condition
    operator: str #and or or
    right: object #binary condition or logical condition
    
@dataclass
class IfStatement:
    condition: object
    body: List[object]
    else_if: 'IfStatement' = None # chain next elif
    else_body: List[object] = None
    
@dataclass
class WhileStatement:
    condition: object
    body: List[object]    

@dataclass
class ForStatement:
    init: object # VAriable or VarUpdate
    condition: object # BinaryCondition or LogicalCondition
    update: object # VarUpdate
    body: List[object]    


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

# called in main
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
    
    if peek.kind in ('int_type', 'string_type', 'char_type', 'float_type', 'double_type', 'boolean_type'):
        return parse_variable(c)
    
    if peek.kind == 'if_keyword':
        return parse_if(c)
    
    if peek.kind == 'while_keyword':
        return parse_while(c)
    
    if peek.kind == 'for_keyword':
        return parse_for(c)
    
    if (peek.kind == 'identifier' and c.peek(1).kind in ('increment_op', 'decrement_op')
                                  and c.peek(2).kind == 'semicolon'):
        name = c.pop().value
        op_token = c.pop()
        c.pop() # skip semicolon
        delta = 1 if op_token.kind == 'increment_op' else -1
        return VarUpdate(name=name, delta=delta)
    
    # skip unknown statements
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
    arg_token = c.peek()
    if arg_token.kind == 'string' or arg_token.kind == 'identifier':
        arg_token = c.pop()
    else:
        raise SyntaxError(f'Expected string or identifier at {arg_token.pos}, got {arg_token.kind} {arg_token.value!r}')
    c.expect("right_parenthesis", ')')
    c.expect("semicolon", ';')
    return Print([arg_token.value])

def parse_variable(c: Cursor):
    type_token = c.pop()
    name_token = c.expect('identifier')
    c.expect('assign')
    value_token = c.peek()
    if value_token.kind in ('string', 'char_literal', 'number', 'float_number', 
                            'identifier', 'true_literal', 'false_literal'):
        value_token = c.pop()
    else: 
        raise SyntaxError(f'Expected string, number, identifier, true or false but got {value_token.kind} {value_token.value!r}')
    c.expect('semicolon', ';')
    type_hint = type_token.value.lower()
    return Variable(name=name_token.value, value=value_token.value, type_hint=type_hint)

def parse_condition(c: Cursor):
    if c.peek().kind == 'identifier':
        identifier = c.expect('identifier').value
        next_token = c.peek()
        if next_token.kind in ('eq', 'neq', 'lt', 'gt', 'leq', 'geq'):
            operator = c.expect(next_token.kind).value
            right_kinds = ('number', 'identifier', 'true_literal', 'false_literal')
            if c.peek().kind in right_kinds:
                right = c.expect(c.peek().kind).value
            else:
                raise SyntaxError(f'Expected {right_kinds} after {operator}, got {c.peek().kind}')
            term = BinaryCondition(left=identifier, operator=operator, right=right)
        else:
            term = BinaryCondition(left=identifier, operator='', right='')
    
    elif c.peek().kind in ('true_literal', 'false_literal'):
        bool_value = c.expect(c.peek().kind).value
        term = BinaryCondition(left=bool_value, operator='', right='')
    
    elif c.peek().kind == 'left_parenthesis':
        c.expect('left_parenthesis')
        term = parse_condition(c)
        c.expect('right_parenthesis')
    
    else:
        raise SyntaxError(f'Unexpected token in condition at {c.peek().pos}: {c.peek().kind} {c.peek().value!r}')
    
    while c.peek().kind in ('and_op', 'or_op'): 
        log_op = c.expect(c.peek().kind).value
        right_term = parse_condition(c)
        term = LogicalCondition(left=term, operator=log_op, right=right_term)
    
    return term
    
def parse_if(c: Cursor):
    c.expect('if_keyword')
    c.expect('left_parenthesis')

    condition = parse_condition(c)
    c.expect('right_parenthesis')
    c.expect('left_brace')
    
    # parse body
    if_body = []
    while c.peek().kind != 'right_brace' and c.peek().kind != 'EOF':
        stmt = parse_statement(c)
        if stmt:
            if_body.append(stmt)    
    c.expect('right_brace')
    
    # else if chains
    else_if = None
    else_body = None
    
    if c.peek().kind == 'else_keyword':
        c.expect('else_keyword')
        
        if c.peek().kind == 'if_keyword':
            else_if = parse_if(c) # recursive call to parse next if as elif            
        else:    
            # final else
            c.expect('left_brace')
            else_body = []
            while c.peek().kind != 'right_brace' and c.peek().kind != 'EOF':
                stmt = parse_statement(c)
                if stmt:
                    else_body.append(stmt)
            c.expect('right_brace')
          
    return IfStatement(condition=condition, body=if_body, else_if = else_if, else_body=else_body)

def parse_while(c: Cursor):
    c.expect('while_keyword')
    c.expect('left_parenthesis')
    condition = parse_condition(c)
    c.expect('right_parenthesis')
    c.expect('left_brace')
    
    while_body = []
    while c.peek().kind != 'right_brace' and c.peek().kind != 'EOF':
        stmt = parse_statement(c)
        if stmt:
            while_body.append(stmt)
    c.expect('right_brace')
    
    return WhileStatement(condition=condition, body=while_body)

def parse_for(c: Cursor):
    c.expect('for_keyword')
    c.expect('left_parenthesis')
    
    init = None
    if c.peek().kind != 'semicolon':
        if c.peek().kind in ('int_type',):
            type_token = c.pop()
            name_token = c.expect('identifier')
            c.expect('assign')
            value_token = c.pop()
            init = Variable(name=name_token.value, value=value_token.value, type_hint=type_token.value.lower())
        elif c.peek(1).kind == 'assign':
            name_token = c.expect('identifier')
            c.expect('assign')
            value_token = c.pop()
            init = Variable(name=name_token.value, value=value_token.value, type_hint='int')
    
    c.expect('semicolon')
        
    condition = None
    if c.peek().kind != 'semicolon':
        condition = parse_condition(c)
    c.expect('semicolon')
    
    update = None
    if c.peek().kind != 'right_parenthesis':
        if c.peek().kind == 'identifier' and c.peek(1).kind in ('increment_op', 'decrement_op'):
            name = c.pop().value
            op_token = c.pop()
            delta = 1 if op_token.kind == 'increment_op' else -1
            update = VarUpdate(name=name, delta=delta)
            
    c.expect('right_parenthesis')
    
    c.expect('left_brace')
    
    for_body = []
    while c.peek().kind != 'right_brace' and c.peek().kind != 'EOF':
        stmt = parse_statement(c)
        if stmt:
            for_body.append(stmt)
    c.expect('right_brace')
    
    return ForStatement(init=init, condition=condition, update=update, body=for_body)