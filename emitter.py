"""
Code emitter module for Java-to-Python translator.
Converts AST into formatter Python source code.
"""
import re

from parser import (
    Print, Variable, IfStatement, BinaryCondition, 
    LogicalCondition, WhileStatement, VarUpdate, ForStatement, UserInput,
    Function, Return, SwitchStatement, Class, Constructor, FieldAccess, ObjectCreation
)

INDENT = '    '

def indent_lines(text, level=1):
    """
    Add indentation to each non_empty line of text.
    """
    
    lines = text.split('\n')
    indented = []
    for line in lines:
        if line.strip():
            # only indent non-empty lines
            indented.append(INDENT * level + line)
        else:
            # keep empty lines empty
            indented.append(line)
    return '\n'.join(indented)

def emit_module(mod):
    """
    Generate Python code from Module AST node.
    """
    
    lines = []
    for stmt in mod.body:
        lines.append(emit_stmt(stmt))
    return "".join(lines) 

def emit_condition(cond):
    """
    Generate Python code for conditional expressions.
    Handles both binary conditions and logical combinations.
    Recursively processes nested conditions.
    """
    
    if isinstance(cond, BinaryCondition):
        if cond.operator:
            return f'{cond.left} {cond.operator} {cond.right}'
        else:
            return f'{cond.left}'
    
    elif isinstance(cond, LogicalCondition):
        py_op = 'and' if cond.operator == '&&' else 'or'  
        # recursivity   
        left_str = emit_condition(cond.left)
        right_str = emit_condition(cond.right)
        return f'({left_str}) {py_op} ({right_str})'
    
    # fallback for unexpected condition types
    return str(cond)

def emit_value(val):
    """
    Convert Java literal values to Python equivalents.
    Handles boolean and float suffixes.
    """
    
    if not val:
        return val
    
    if val == 'true':
        return 'True'
    elif val == 'false':
        return 'False'
    elif len(val) > 1 and val[-1] in ('f', 'F'):
        return val[:-1]
    
    if val.startswith('new '):
        return val[4:]
    
    return val

def emit_if(stmt):
    """
    Generate Python code for IfStatement AST node.
    Handles optional else branch.
    """
    
    cond_str = emit_condition(stmt.condition)
    result = f'if {cond_str}:\n'
    
    body_lines = [emit_stmt(s) for s in stmt.body]
    body_str = ''.join(body_lines)
    result += indent_lines(body_str, level=1)
    
    if stmt.else_if:
        elif_code = emit_stmt(stmt.else_if)
        elif_code = elif_code.replace('if', 'elif', 1)
        result += elif_code
    elif stmt.else_body:
        result += 'else:\n'
        else_lines = [emit_stmt(s) for s in stmt.else_body]
        else_str = ''.join(else_lines)
        result += indent_lines(else_str, level=1)
    return result

def emit_while(stmt):
    """
    Generate Python code for while loop.
    """
    
    cond_str = emit_condition(stmt.condition)
    result = f'while {cond_str}:\n'
    
    body_lines = [emit_stmt(s) for s in stmt.body]
    body_str = ''.join(body_lines)
    result += indent_lines(body_str, level=1)
    
    return result

def is_simple_range_loop(stmt):
    """
    Determine if a ForStatement can be converted to Python's range() loop.
    
    A simple range loop has:
    - numeric initialization
    - binary condition comparing loop variable to a number
    - simple increment/decrement
    """
    
    return (
        stmt.init and isinstance(stmt.init, Variable) and stmt.init.value.isdigit() and
        stmt.condition and isinstance(stmt.condition, BinaryCondition) and
        stmt.condition.left == stmt.init.name and stmt.condition.right.isdigit() and
        stmt.update and isinstance(stmt.update, VarUpdate) and abs(stmt.update.delta) == 1
    )

def emit_for(stmt):
    """
    Generate Python code for for loop.
    Attempts to convert simple counting loops to Python's range() syntax.
    Falls back to while loop for complex cases.
    """
    
    if is_simple_range_loop(stmt):
        start = int(stmt.init.value)
        end = int(stmt.condition.right)
        var_name = stmt.init.name
        op = stmt.condition.operator
        step = stmt.update.delta
        
        range_args = None
        
        if op == '<' and step == 1:
            # for (i = 0; i < 10; i++) → range(0, 10)
            range_args = f'{start}, {end}'
        elif op == '<=' and step == 1:
            # for (i = 0; i <= 10; i++) → range(0, 11)
            range_args = f'{start}, {end + 1}'
        elif op == '>' and step == -1:
            # for (i = 10; i > 0; i--) → range(10, 0, -1)
            range_args = f'{start}, {end}, -1'
        elif op == '>=' and step == -1:
            # for (i = 10; i >= 0; i--) → range(10, -1, -1)
            range_args = f'{start}, {end - 1}, -1'
        elif op == '==' and step == 1:
            # Edge case: for (i = 5; i == 5; i++) runs once
            range_args = f'{start}, {start + 1}'
        elif op == '!=' and step == 1:
            # for (i = 0; i != 10; i++) → range(0, 10)
            range_args = f'{start}, {end}'
            
        if range_args:
            result = f'for {var_name} in range({range_args}):\n'
            
            body_lines = [emit_stmt(s) for s in stmt.body]
            body_str = ''.join(body_lines)
            result += indent_lines(body_str, level=1)
            
            return result
    
    lines = [] 
    # fallback convert to while loop
    if stmt.init is not None:
        lines.append(emit_stmt(stmt.init))
        
    cond_str = 'True' if stmt.condition is None else emit_condition(stmt.condition)
    
    body_lines = [emit_stmt(s) for s in stmt.body]
    if stmt.update is not None:
        body_lines.append(emit_stmt(stmt.update))
    body_str = ''.join(body_lines)
    
    result = f'while {cond_str}:\n'
    result += indent_lines(body_str, level=1)
    
    return ''.join(lines) + result

def emit_user_input(stmt):
    if stmt.input_type in ('nextLine', 'next'):
        return f'{stmt.name} = input()\n'
    elif stmt.input_type == 'nextInt':
        return f'{stmt.name} = int(input())\n'
    elif stmt.input_type in ('nextDouble', 'nextFloat'):
        return f'{stmt.name} = float(input())\n'
    else:   
        raise NotImplementedError(f"Unknown input type: {stmt.input_type}")
    
def emit_function(stmt):
    param_names = [name for (param_type, name) in stmt.parameters]
    params_str = ', '.join(param_names)
    result = f'def {stmt.name}({params_str}):\n'
    
    if stmt.body:
        body_lines = [emit_stmt(s) for s in stmt.body]
        body_str = ''.join(body_lines)
        result += indent_lines(body_str, level=1)
    else:
        result += indent_lines('pass\n', level=1)
    return result + '\n'

def emit_return(stmt):
    if stmt.value is None:
        return 'return\n'
    else:
        converted_value = emit_value(stmt.value)
        return f'return {converted_value}\n'
    
def emit_switch(stmt):
    # Special case: switch with only default (no cases)
    if not stmt.cases and stmt.default_body:
        # Just emit the default body directly
        result = ""
        for s in stmt.default_body:
            result += emit_stmt(s)
        return result
    
    # Special case: switch with no cases and no default (empty switch)
    if not stmt.cases and not stmt.default_body:
        return "pass\n"
    
    result = ""
    first_case = True
    
    i = 0
    while i < len(stmt.cases):
        case_value, case_body, has_break = stmt.cases[i]
        
        # Collect cases for fall-through
        fall_through_cases = [case_value]
        accumulated_body = list(case_body)
        
        # If no break, accumulate following cases
        if not has_break and i < len(stmt.cases) - 1:
            j = i + 1
            while j < len(stmt.cases):
                next_val, next_body, next_break = stmt.cases[j]
                fall_through_cases.append(next_val)
                accumulated_body.extend(next_body)
                if next_break:
                    i = j  # Skip to this case
                    break
                j += 1
            else:
                i = j - 1
        
        # Build condition with all fall-through values
        condition_parts = [f'{stmt.expression} == {emit_value(val)}' for val in fall_through_cases]
        condition = ' or '.join(condition_parts)
        
        if first_case:
            result += f'if {condition}:\n'
            first_case = False
        else:
            result += f'elif {condition}:\n'
            
        if accumulated_body:
            body_lines = [emit_stmt(s) for s in accumulated_body]
            body_str = ''.join(body_lines)
            result += indent_lines(body_str, level=1)
        else:
            result += indent_lines('pass\n', level=1)
        
        i += 1
    
    # handle default case
    if stmt.default_body:
        result += 'else:\n'
        default_lines = [emit_stmt(s) for s in stmt.default_body]
        default_str = ''.join(default_lines)
        result += indent_lines(default_str, level=1)
    
    return result

def emit_class(stmt):
    result = f'class {stmt.name}:\n'

    # if class is completely empty
    if not stmt.constructor and not stmt.methods and not stmt.fields:
        result += indent_lines('pass', level=1)
        return result + '\n'
    
    # emit constructor
    if stmt.constructor:
        result += emit_constructor(stmt.constructor)
    elif stmt.fields:
        # if no constructor, but has fields, create default __init__
        result += indent_lines('def __init__(self):\n', level=1)
        for field in stmt.fields:
            if field.value:
                result += indent_lines(f'self.{field.name} = {emit_value(field.value)}\n', level=2)
            else:
                result += indent_lines(f'self.{field.name} = None\n', level=2)
    
    # emit instance methods
    for method in stmt.methods:
        result += emit_method(method)
        
    return result + '\n'

def emit_constructor(stmt):
    param_names = ['self'] + [name for (param_type, name) in stmt.parameters]
    params_str = ', '.join(param_names)
    result = indent_lines(f'def __init__({params_str}):\n', level=1)
    
    if stmt.body:
        body_lines = []
        for s in stmt.body:
            line = emit_stmt(s)
            # convert 'this.field' to 'self.field' in constructor body
            line = re.sub(r'this\s*\.\s*', 'self.', line)
            body_lines.append(line)
        body_str = ''.join(body_lines)
        result += indent_lines(body_str, level=2)
    else:
        result += indent_lines('pass\n', level=2)
        
    return result + '\n'

def emit_method(stmt):
    # build parameter list with 'self'
    param_names = ['self'] + [name for (param_type, name) in stmt.parameters]
    params_str = ', '.join(param_names)
    result = indent_lines(f'def {stmt.name}({params_str}):\n', level=1)
    
    if stmt.body:
        body_lines = []
        for s in stmt.body:
            line = emit_stmt(s)
            line = re.sub(r'this\s*\.\s*', 'self.', line)
            body_lines.append(line)
        body_str = ''.join(body_lines)
        result += indent_lines(body_str, level=2)
    else:
        result += indent_lines('pass\n', level=2)
    
    return result + '\n'
    
    
def emit_stmt(stmt):
    
    """
    Generate Python code for a single statement.
    Dispatches to appropriate emitter based on statement type.
    """
    if isinstance(stmt, Print):
        arg = stmt.args[0]
        
        if '+' in arg:
            arg_with_commas = arg.replace(' + ', ', ')
            return f'print({arg_with_commas})\n'
        return f'print({arg})\n'
    
    elif isinstance(stmt, Variable):
        val = emit_value(stmt.value)
        return f'{stmt.name} = {val}\n'
    
    elif isinstance(stmt, IfStatement):
        return emit_if(stmt)
        
    elif isinstance(stmt, WhileStatement):
        return emit_while(stmt)
    
    elif isinstance(stmt, VarUpdate):
        if stmt.delta >= 0:
            return f'{stmt.name} += {stmt.delta}\n'
        else:
            return f'{stmt.name} -= {abs(stmt.delta)}\n'
        
    elif isinstance(stmt, ForStatement):
        return emit_for(stmt)
    
    elif isinstance(stmt, UserInput):
        return emit_user_input(stmt)
    
    elif isinstance(stmt, Function):
        return emit_function(stmt)
    
    elif isinstance(stmt, Return):
        return emit_return(stmt)
    
    elif isinstance(stmt, SwitchStatement):
        return emit_switch(stmt)
    
    elif isinstance(stmt, Class):
        return emit_class(stmt)

    raise NotImplementedError(f"No emitter for {type(stmt).__name__}")
