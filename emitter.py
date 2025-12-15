"""
Code emitter module for Java-to-Python translator.
Converts AST into formatter Python source code.
"""

from parser import (
    Print, Variable, IfStatement, BinaryCondition, 
    LogicalCondition, WhileStatement, VarUpdate, ForStatement
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

def emit_stmt(stmt):
    
    """
    Generate Python code for a single statement.
    Dispatches to appropriate emitter based on statement type.
    """
    if isinstance(stmt, Print):
        return f'print({stmt.args[0]})\n' 
    
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

    raise NotImplementedError(f"No emitter for {type(stmt).__name__}")
