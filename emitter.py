from parser import Print, Variable, IfStatement, BinaryCondition, LogicalCondition

def emit_module(mod):
    lines = []
    for stmt in mod.body:
        lines.append(emit_stmt(stmt))
    return "".join(lines) 

def emit_condition(cond):
    if isinstance(cond, BinaryCondition):
        if cond.operator:
            return f'{cond.left} {cond.operator} {cond.right}'
        else:
            return f'{cond.left}'
    
    elif isinstance(cond, LogicalCondition):
        py_op = 'and' if cond.operator == '&&' else 'or'        
        return f'({emit_condition(cond.left)} {py_op} {emit_condition(cond.right)})'
    
    return str(cond)

def emit_stmt(stmt):
    if isinstance(stmt, Print):
        return f'print({stmt.args[0]})\n' 
    
    elif isinstance(stmt, Variable):
        val = stmt.value
        if val == 'true':
            val = 'True'
        elif val == 'false':
            val = 'False'
        elif val[-1] in ('f', 'F'):
            val = val[:-1]
        return f'{stmt.name} = {val}\n'
    
    elif isinstance(stmt, IfStatement):
        cond_str = emit_condition(stmt.condition)
        body_str= '\n'.join(emit_stmt(s) for s in stmt.body).replace('\n', '\n    ')
        
        if stmt.else_if:
            elif_part = emit_stmt(stmt.else_if).replace('if', 'elif', 1).lstrip()
            return f'if {cond_str}:\n    {body_str}\n{elif_part}'
        elif stmt.else_body:
            else_str = '\n'.join(emit_stmt(s) for s in stmt.else_body).replace('\n', '\n    ')
            return f'if {cond_str}:\n    {body_str}\nelse:\n    {else_str}'
        else:
            return f'if {cond_str}:\n    {body_str}\n'
        
    raise NotImplementedError(f"No emitter for {type(stmt).__name__}")
