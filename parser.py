"""
Parser module for Java-to-Python translation.
Implements a recursive descent parser that converts tokens into an Abstract Syntax Tree (AST).
Performs syntax analysis and builds a tree representation of the program structure.
"""

from rules import (PRINT_RECEIVER, PRINT_FIELD, PRINT_METHODS, TYPE_TOKEN_KINDS, FUNCTION_RETURN_TYPES)
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
    
@dataclass
class UserInput:
    name: str # variable name receiving input
    input_type: str # type of scanner method (nextLine, nextInt, etc.)
    var_type: str # java type being declared (intr, String, etc.) 
    
@dataclass
class Function:
    name: str
    parameters: List[tuple] # list of (type, name) tuples for parameters
    return_type: str
    body: List[object]
    
@dataclass
class Return:
    value: Optional[str] # can be none for void functions
    
@dataclass
class SwitchStatement:
    expression: str
    cases: List[tuple]  # list of (case_value, body) tuples
    default_body: Optional[List[object]] = None # default case body (optional)
    
@dataclass
class Class:
    name: str
    fields: List[Variable] # instance variables
    constructor: Optional['Constructor']
    methods: List[Function] # instance methods
    
@dataclass
class Constructor:
    # initialize obkects (becomes __init__ in python)
    parameters: List[tuple] # list of (type, name) tuples
    body: List[object] # constructor body statements
    
@dataclass
class FieldAccess:
    object_name: str # 'this' or object variable name
    field_name: str # the field being accessed
    
@dataclass
class ObjectCreation:
    class_name: str
    arguments: List[str] # constructor arguments

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
 
    # skip standalone closing braces (end of class body)
    if peek.kind == 'right_brace':
        c.pop()
        return None
    
    # check for class declaration
    if (peek.kind == 'identifier' and peek.value == 'class' and c.peek(1).kind == 'identifier'):
        return parse_class(c)
    
    if (peek.kind == 'void_type' and 
        c.peek(1).kind == 'identifier' and c.peek(1).value == 'main' and
        c.peek(2).kind == 'left_parenthesis'):
        c.pop()  # void
        c.pop()  # main
        c.pop()  # (
        while c.peek().kind != 'left_brace' and c.peek().kind != 'EOF':
            c.pop()
        c.pop()  # consume the {
        return None
    
    # check for print statement
    if (peek.kind == 'identifier' and peek.value == PRINT_RECEIVER and
        c.peek(1).kind == 'dot' and c.peek(2).value == PRINT_FIELD and
        c.peek(3).kind == 'dot' and c.peek(4).value in PRINT_METHODS):
        return parse_print(c)
    
    if peek.kind in FUNCTION_RETURN_TYPES:
        if (c.peek(1).kind == 'identifier' and c.peek(2).kind == 'left_parenthesis'):
            func = parse_function(c)
            return func
    
    if peek.kind in TYPE_TOKEN_KINDS:
        if (c.peek(1).kind == 'identifier' and 
            c.peek(2).kind == 'assign' and 
            c.peek(3).kind == 'identifier' and
            c.peek(4).kind in ('scanner_nextline', 'scanner_nextint', 'scanner_nextdouble', 
                            'scanner_nextfloat', 'scanner_next')):
            return parse_user_input(c)
        return parse_variable(c)
    
    # check for object creation (ClassName varName = new ClassName(...))
    if (peek.kind == 'identifier' and 
        c.peek(1).kind == 'identifier' and 
        c.peek(2).kind == 'assign' and
        c.peek(3).kind == 'new_keyword'):
        return parse_variable(c)
    
    # check for method calls (varName.methodName(...))
    if (peek.kind == 'identifier' and 
        c.peek(1).kind == 'dot' and
        c.peek(2).kind == 'identifier' and
        c.peek(3).kind == 'left_parenthesis'):
        # this is a method call - parse it
        return parse_method_call(c)

    if peek.kind == 'if_keyword':
        return parse_if(c)
    
    if peek.kind == 'while_keyword':
        return parse_while(c)
    
    if peek.kind == 'for_keyword':
        return parse_for(c)
    
    if peek.kind == 'return_keyword':
        return parse_return(c)
    
    if peek.kind == 'switch_keyword':
        return parse_switch(c)
    
    # increment/decrement
    if (peek.kind == 'identifier' and c.peek(1).kind in ('increment_op', 'decrement_op')
                                  and c.peek(2).kind == 'semicolon'):
        name = c.pop().value
        op_token = c.pop()
        c.pop() # skip semicolon
        delta = 1 if op_token.kind == 'increment_op' else -1
        return VarUpdate(name=name, delta=delta)
    
    if (peek.kind == 'identifier' and c.peek(1).kind == 'assign'):
        name = c.pop().value
        c.expect('assign')
        
        value_tokens = []
        while c.peek().kind != 'semicolon' and c.peek().kind != 'EOF':
            value_tokens.append(c.pop().value)
        
        c.expect('semicolon')
        value = ' '.join(value_tokens)
        
        return Variable(name=name, value=value, type_hint='')
    
    # handle this.field++ and this.field-- (in constructors/methods)
    if (peek.kind == 'this_keyword' and c.peek(1).kind == 'dot' and 
        c.peek(3).kind in ('increment_op', 'decrement_op')):
        c.pop()  # consume 'this'
        c.expect('dot')
        field_name = c.expect('identifier').value
        op_token = c.pop()  # ++ or --
        c.expect('semicolon')
        
        delta = 1 if op_token.kind == 'increment_op' else -1
        # return as VarUpdate with 'this.field' as name
        return VarUpdate(name=f'this.{field_name}', delta=delta)

    # handle this.field = value (in constructors/methods)
    if (peek.kind == 'this_keyword' and c.peek(1).kind == 'dot'):
        c.pop()  # consume 'this'
        c.expect('dot')
        field_name = c.expect('identifier').value
        c.expect('assign')
        
        # collect value expression
        value_tokens = []
        while c.peek().kind != 'semicolon' and c.peek().kind != 'EOF':
            value_tokens.append(c.pop().value)
        
        c.expect('semicolon')
        value = ' '.join(value_tokens)
        
        # return as Variable with 'this.field' as name
        return Variable(name=f'this.{field_name}', value=value, type_hint='')

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
    
    arg_tokens = []
    while c.peek().kind != "right_parenthesis" and c.peek().kind != "EOF":
        arg_tokens.append(c.pop().value)
        
    arg_value = ' '.join(arg_tokens) if arg_tokens else ''
    
    c.expect("right_parenthesis", ')')
    c.expect("semicolon", ';')
    
    return Print([arg_value])

def parse_variable(c: Cursor):
    type_token = c.pop()
    name_token = c.expect('identifier')
    
    # check if there's an assignment
    if c.peek().kind == 'assign':
        c.expect('assign')
        
        value_tokens = []
        while c.peek().kind != 'semicolon' and c.peek().kind != 'EOF':
            token = c.pop()
            value_tokens.append(token.value)
        
        c.expect('semicolon', ';')
        
        # join tokens smartly - no spaces around dots and parentheses
        if not value_tokens:
            value = ''
        else:
            value = ''
            for i, tok in enumerate(value_tokens):
                if i == 0:
                    value = tok
                elif tok in ('.', '(', ')', ',') or value_tokens[i-1] in ('.', '('):
                    value += tok
                else:
                    value += ' ' + tok
    
    else:
        # no initialization
        c.expect('semicolon', ';')
        value = ''  # empty value for uninitialized fields
        
    type_hint = type_token.value.lower()
    
    return Variable(
        name=name_token.value, 
        value=value, 
        type_hint=type_hint
    )


def parse_condition(c: Cursor):
    
    """
    Parse conditional expression recursively.
    Handles binary conditions, boolean literals and logical operators.
    Calls itself for nested conditions.
    """
    
    if c.peek().kind == 'left_parenthesis':
        c.expect('left_parenthesis')
        # recursive call to parse nested condition
        term = parse_condition(c)
        c.expect('right_parenthesis')
        
    elif c.peek().kind in ('true_literal', 'false_literal'):
        bool_value = c.expect(c.peek().kind).value
        term = BinaryCondition(left=bool_value, operator='', right='')
        
    else:
        left_tokens = []
        while c.peek().kind not in ('eq', 'neq', 'lt', 'gt', 'leq', 'geq', 
                                      'right_parenthesis', 'and_op', 'or_op', 'EOF'):
            left_tokens.append(c.pop().value)
        
        left_expr = ' '.join(left_tokens)
        
        if c.peek().kind in ('eq', 'neq', 'lt', 'gt', 'leq', 'geq'):
            operator = c.expect(c.peek().kind).value
            
            right_tokens = []
            while c.peek().kind not in ('right_parenthesis', 'and_op', 'or_op', 
                                         'semicolon', 'left_brace', 'EOF'):
                right_tokens.append(c.pop().value)
            
            right_expr = ' '.join(right_tokens)
            term = BinaryCondition(left=left_expr, operator=operator, right=right_expr)
        else:
            term = BinaryCondition(left=left_expr, operator='', right='')
   
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
          
    return IfStatement(
        condition=condition, 
        body=if_body, 
        else_if = else_if, 
        else_body=else_body
    )

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
    
    return WhileStatement(
        condition=condition, 
        body=while_body
    )

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
    
    return ForStatement(
        init=init, 
        condition=condition, 
        update=update, 
        body=for_body
    )

def parse_user_input(c: Cursor):
    type_token = c.pop()
    name_token = c.expect('identifier')
    c.expect('assign')
    scanner_obj = c.expect('identifier')
    
    method_token = c.peek()
    if method_token.kind in ('scanner_nextline', 'scanner_nextint', 'scanner_nextdouble', 
                             'scanner_nextfloat', 'scanner_next'):
        method_token = c.pop()
    else:
        raise SyntaxError(f'Expected scanner input method at {method_token.pos}, got {method_token.kind} {method_token.value!r}')
    
    c.expect('semicolon', ';')
    
    # map token kind to method name
    method_map = {
        'scanner_nextline': 'nextLine',
        'scanner_nextint': 'nextInt',
        'scanner_nextdouble': 'nextDouble',
        'scanner_nextfloat': 'nextFloat',
        'scanner_next': 'next'
    }
    
    return UserInput(
        name=name_token.value,
        input_type=method_map[method_token.kind],
        var_type=type_token.value.lower()
    )
    
def parse_method_call(c: Cursor):
    """
    Parse a method call statement: objectName.methodName(args);
    Example: alice.greet(); or buddy.bark();
    """
    object_name = c.expect('identifier').value
    c.expect('dot') 
    method_name = c.expect('identifier').value 
    c.expect('left_parenthesis')
    
    # collect arguments (if any)
    args = []
    while c.peek().kind != 'right_parenthesis' and c.peek().kind != 'EOF':
        arg_tokens = []
        while c.peek().kind not in ('comma', 'right_parenthesis', 'EOF'):
            arg_tokens.append(c.pop().value)
        
        if arg_tokens:
            args.append(' '.join(arg_tokens))
        
        if c.peek().kind == 'comma':
            c.pop()
    
    c.expect('right_parenthesis')  # )
    c.expect('semicolon')  # ;
    
    # return as a Variable assignment to handle it simply
    # format: objectName.methodName(args)
    args_str = ', '.join(args) if args else ''
    value = f'{object_name}.{method_name}({args_str})'
    
    return Variable(name='', value=value, type_hint='')

def parse_function(c: Cursor):
    return_type_token = c.pop()
    return_type = return_type_token.value.lower()
    
    name_token = c.expect('identifier')
    function_name = name_token.value
    
    c.expect('left_parenthesis')
    params = []
    
    # check if there are any parameters
    if c.peek().kind != 'right_parenthesis':
        while True:
            if c.peek().kind in TYPE_TOKEN_KINDS:
                param_type = c.pop().value.lower()
            else:
                raise SyntaxError(f'Expected parameter type at {c.peek().pos}, got {c.peek().kind} {c.peek().value!r}')
            
            param_name = c.expect('identifier').value
            params.append((param_type, param_name))
            
            if c.peek().kind == 'comma':
                c.pop()
            else:
                break
        
    c.expect('right_parenthesis')
    c.expect('left_brace')
    
    function_body = []
    while c.peek().kind != 'right_brace' and c.peek().kind != 'EOF':
        stmt = parse_statement(c)
        if stmt:
            function_body.append(stmt)
    
    c.expect('right_brace')
    
    return Function(
        name=function_name,
        parameters=params,
        return_type=return_type,
        body=function_body
    )
    
def parse_return(c: Cursor):
    c.expect('return_keyword')
    
    if c.peek().kind == 'semicolon':
        c.expect('semicolon')
        return Return(value=None) # for void functions
    
    return_tokens = []
    while c.peek().kind != 'semicolon' and c.peek().kind != 'EOF':
        return_tokens.append(c.pop().value)
        
    c.expect('semicolon')
    
    return_value = ' '.join(return_tokens)
    return Return(value=return_value)

def parse_switch(c: Cursor):
    c.expect('switch_keyword')
    c.expect('left_parenthesis')
    
    expr_tokens = []
    while c.peek().kind != 'right_parenthesis' and c.peek().kind != 'EOF':
        expr_tokens.append(c.pop().value)
    expression = ' '.join(expr_tokens)
    
    c.expect('right_parenthesis')
    c.expect('left_brace')

    cases = []
    default_body = None
    
    while c.peek().kind != 'right_brace' and c.peek().kind != 'EOF':
        if c.peek().kind == 'case_keyword':
            c.pop()  # consume 'case'
            
            case_value = c.pop().value
            c.expect('colon')
            
            case_body = []
            has_break = False
            
            while c.peek().kind not in ('case_keyword', 'default_keyword', 'right_brace', 'EOF'):
                if c.peek().kind == 'break_keyword':
                    has_break = True
                    c.pop()  # consume 'break'
                    c.expect('semicolon')
                    has_break = True
                    break
                else:
                    stmt = parse_statement(c)
                    if stmt:
                        case_body.append(stmt)

            cases.append((case_value, case_body, has_break))
            
        elif c.peek().kind == 'default_keyword':
            c.pop()
            c.expect('colon')
            
            default_body = []
            while c.peek().kind not in ('right_brace', 'EOF'):
                if c.peek().kind == 'break_keyword':
                    c.pop()  # consume 'break'
                    if c.peek().kind == 'semicolon':
                        c.pop()
                    break
                else:
                    stmt = parse_statement(c)
                    if stmt:
                        default_body.append(stmt)
        
        else:
            c.pop()  # skip unknown tokens
            
    c.expect('right_brace')
    
    return SwitchStatement(
        expression=expression, 
        cases=cases, 
        default_body=default_body
    )

def parse_class(c: Cursor):
    """
    Parse a Java class declaration.
    Special case: if class only contains main method, extract and return main body.
    """
    c.expect('identifier', 'class')
    class_name = c.expect('identifier').value
    c.expect('left_brace')

    # check if this is a main-only class
    # look ahead: is first non-field member "public static void main"?
    saved_pos = c.i  # save position to backtrack
    
    # skip any fields at the start
    temp_pos = c.i
    while c.peek().kind in TYPE_TOKEN_KINDS:
        if c.peek(1).kind == 'identifier' and c.peek(2).kind in ('semicolon', 'assign'):
            while c.peek().kind != 'semicolon' and c.peek().kind != 'EOF':
                c.pop()
            c.pop()  # semicolon
        else:
            break
    
    # now check if we see void main (public static are skipped by lexer)
    is_main_only = (c.peek().kind == 'void_type' and
                    c.peek(1).kind == 'identifier' and c.peek(1).value == 'main' and
                    c.peek(2).kind == 'left_parenthesis')

    
    # restore position
    c.i = saved_pos
    
    if is_main_only:
        # skip to the main method declaration (look for void main)
        while not (c.peek().kind == 'void_type' and
                   c.peek(1).kind == 'identifier' and c.peek(1).value == 'main'):
            if c.peek().kind == 'EOF':
                break
            c.pop()

        
        # skip "public static void main(...)"
        while c.peek().kind != 'left_brace' and c.peek().kind != 'EOF':
            c.pop()
        
        c.expect('left_brace')  # consume main's {
        
        # parse main body statements
        statements = []
        while c.peek().kind != 'right_brace' and c.peek().kind != 'EOF':
            stmt = parse_statement(c)
            if stmt:
                statements.append(stmt)
        
        c.expect('right_brace')  # consume main's }
        c.expect('right_brace')  # consume class's }
        
        # return a special marker that tells emit_module to flatten these
        return ('main_body', statements)
    
    # normal class parsing (has fields, constructors, multiple methods, etc.)
    fields = []
    constructor = None
    methods = []
    
    while c.peek().kind != 'right_brace' and c.peek().kind != 'EOF':
        peek = c.peek()
        
        # check for field declaration
        if peek.kind in TYPE_TOKEN_KINDS:
            if c.peek(1).kind == 'identifier' and c.peek(2).kind in ('semicolon', 'assign'):
                field = parse_variable(c)
                fields.append(field)
                continue
        
        # check for constructor
        if peek.kind == 'identifier' and peek.value == class_name and c.peek(1).kind == 'left_parenthesis':
            constructor = parse_constructor(c, class_name)
            continue
        
        # check for method
        if peek.kind in FUNCTION_RETURN_TYPES:
            if (c.peek(1).kind == 'identifier' and c.peek(2).kind == 'left_parenthesis'):
                method = parse_function(c)
                methods.append(method)
                continue
            
        c.pop()  # skip unknown tokens
        
    c.expect('right_brace')
    
    return Class(
        name=class_name, 
        fields=fields, 
        constructor=constructor, 
        methods=methods
    )

def parse_constructor(c: Cursor, class_name: str):
    c.expect('identifier', class_name)
    c.expect('left_parenthesis')
    params = []
    
    # check if there are any parameters
    if c.peek().kind != 'right_parenthesis':
        while True:
            if c.peek().kind in TYPE_TOKEN_KINDS:
                param_type = c.pop().value.lower()
            else:
                raise SyntaxError(f'Expected parameter type at {c.peek().pos}, got {c.peek().kind} {c.peek().value!r}')
            
            param_name = c.expect('identifier').value
            params.append((param_type, param_name))
            
            if c.peek().kind == 'comma':
                c.pop()
            else:
                break
        
    c.expect('right_parenthesis')
    c.expect('left_brace')
    
    constructor_body = []
    while c.peek().kind != 'right_brace' and c.peek().kind != 'EOF':
        stmt = parse_statement(c)
        if stmt:
            constructor_body.append(stmt)
    
    c.expect('right_brace')
    
    return Constructor(
        parameters=params,
        body=constructor_body
    )