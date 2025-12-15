"""
Parser module for Java-to-Python translation.
Implements a recursive descent parser that converts tokens into an Abstract Syntax Tree (AST).
Performs syntax analysis and builds a tree representation of the program structure.
"""

from rules import PRINT_RECEIVER, PRINT_FIELD, PRINT_METHODS, TYPE_TOKEN_KINDS, PRINTABLE_KINDS, LITERAL_KINDS, VALUE_KINDS
from dataclasses import dataclass
from typing import List, Union, Optional
from lexer import Token
# AST node classes
# dataclasses represent nodes in the AST
# dataclasses generate automatically __init__ and other methods

@dataclass
class Module:
    # root node of AST
    # list of statements in the module
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
    """
    Represents an increment or decrement operation on a variable.
    examples: x++, y--
    """
    name: str # variable being updated
    delta: int # amount to increment/decrement by
    
@dataclass
class BinaryCondition: 
    """
    Represent a binary comparison condition.
    Example: x == 5 -> BinaryCondition(left='x', operator='==', right='5')
             isActive -> BinaryCondition(left='isActive', operator='', right='')
    """
    left: str
    # when the condition is a bool/var name, 
    # operator and right are empty strings
    operator: str
    right: str    
    
@dataclass
class LogicalCondition:
    """
    Represents a logical combination of conditions using && or ||.
    Example: (x > 5 && y < 10) -> LogicalCondition with two BinaryConditions
    
    Allows nested conditions.
    """
    left: Union['BinaryCondition', 'LogicalCondition'] 
    operator: str #and or or
    right: Union['BinaryCondition', 'LogicalCondition']
    
@dataclass
class IfStatement:
    """
    Represents if/else-if/else statement chains.
    else-if is represented as a recursive IfStatement.
    """
    
    condition: Union[BinaryCondition, LogicalCondition]
    body: List[object]
    else_if: Optional['IfStatement'] = None # chain next elif (recursive structure)
    else_body: Optional[List[object]] = None
    
@dataclass
class WhileStatement:
    condition: Union[BinaryCondition, LogicalCondition]
    body: List[object]    

@dataclass
class ForStatement:
    init: Optional[Union[Variable, VarUpdate]] # can be none
    condition: Optional[Union[BinaryCondition, LogicalCondition]] # can be none
    update: Optional[VarUpdate] # update expression (can be none)
    body: List[object]    

class Cursor:
    
    """
    Manages token stream navigation for the parser.
    Provides three key operations:
    - peek(k): look ahead at token without consuming
    - pop(): consume and return current token
    - expect(kind, value): consume token and verify it matches expectations
    
    Lookahead is necessary for determining which rule to apply.
    """
    
    def __init__(self, tokens):
        self.tokens = list(tokens) # convert generator to list for random access
        self.i = 0
    
    # look at future tokens without removing them from the token stream
    def peek(self, k = 0):
        idx = self.i + k
        if idx >= len(self.tokens):
            return self.tokens[-1] if self.tokens else Token('EOF', '', 0)
        return self.tokens[idx]
    
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
    """
    Converts token stream into AST Module.
    Called from main.py after lexical analysis.
    """
    
    c = Cursor(tokens)
    body = []
    
    while c.peek().kind != "EOF":
        stmt = parse_statement(c)
        if stmt: 
            body.append(stmt)
    return Module(body=body)

def parse_statement(c: Cursor):
    """
    Parses a single statement by examining the current 
    token and dispatching to appropriate parse function.
    """
    peek = c.peek()
    
    # check for print statement
    if (peek.kind == 'identifier' and peek.value == PRINT_RECEIVER and
        c.peek(1).kind == 'dot' and c.peek(2).value == PRINT_FIELD and
        c.peek(3).kind == 'dot' and c.peek(4).value in PRINT_METHODS):
        return parse_print(c)
    
    if peek.kind in TYPE_TOKEN_KINDS:
        return parse_variable(c)
    
    if peek.kind == 'if_keyword':
        return parse_if(c)
    
    if peek.kind == 'while_keyword':
        return parse_while(c)
    
    if peek.kind == 'for_keyword':
        return parse_for(c)
    
    # increment/decrement
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
    # consume java pattern: System.out.println(...)
    c.expect("identifier", PRINT_RECEIVER)
    c.expect("dot", '.')          
    c.expect("identifier", PRINT_FIELD)
    c.expect("dot", '.')
    
    # get print method name (println or print)
    name = c.expect("identifier").value
    if name not in PRINT_METHODS:
        raise SyntaxError(f'Expected {PRINT_METHODS}, got {name}')
    
    c.expect("left_parenthesis", '(') 
    
    # parse argument
    # currently only handles single argument, but could be extended for more
    arg_token = c.peek()
    if arg_token.kind in PRINTABLE_KINDS:
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
    if value_token.kind in VALUE_KINDS:
        value_token = c.pop()
    else: 
        raise SyntaxError(f'Expected string, number, identifier, true or false but got {value_token.kind} {value_token.value!r}')
    
    c.expect('semicolon', ';')
    
    # convert java type to python type hint
    type_hint = type_token.value.lower()
    
    return Variable(name=name_token.value, value=value_token.value, type_hint=type_hint)

def parse_condition(c: Cursor):
    
    """
    Parse conditional expression recursively.
    Handles binary conditions, boolean literals and logical operators.
    Calls itself for nested conditions.
    """
    # check for comparison operator
    if c.peek().kind == 'identifier':
        identifier = c.expect('identifier').value
        next_token = c.peek()
        # check for comparison operator
        if next_token.kind in ('eq', 'neq', 'lt', 'gt', 'leq', 'geq'):
            operator = c.expect(next_token.kind).value
            # parse right side of comparison
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
        # recursive call to parse nested condition
        term = parse_condition(c)
        c.expect('right_parenthesis')
    
    else:
        raise SyntaxError(
            f'Unexpected token in condition at position {c.peek().pos}: '
            f'{c.peek().kind} {c.peek().value!r}'
        )
    # check for logical operators and build LogicalCondition
    while c.peek().kind in ('and_op', 'or_op'): 
        log_op = c.expect(c.peek().kind).value
        right_term = parse_condition(c)
        term = LogicalCondition(left=term, operator=log_op, right=right_term)
    
    return term

# recursive parsing of if-else chains
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
        if c.peek().kind in TYPE_TOKEN_KINDS:
            type_token = c.pop()
            name_token = c.expect('identifier')
            c.expect('assign')
            value_token = c.pop()
            init = Variable(
                name=name_token.value, 
                value=value_token.value, 
                type_hint=type_token.value.lower()
            )
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