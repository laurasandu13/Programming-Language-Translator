from parser import Print, Variable, IfStatement, BinaryCondition, LogicalCondition, WhileStatement, VarUpdate, ForStatement

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
        body_str= '\n'.join(emit_stmt(s) for s in stmt.body)
        result = f'if {cond_str}:\n'
        for line in body_str.split('\n'):
            if line:
                result += f'    {line}\n'
        
        if stmt.else_if:
            elif_part = emit_stmt(stmt.else_if).replace('if', 'elif', 1)
            result += elif_part
        elif stmt.else_body:
            else_str = '\n'.join(emit_stmt(s) for s in stmt.else_body)
            result += 'else:\n'
            for line in else_str.split('\n'):
                if line:
                    result += f'    {line}\n'
        return result
        
    elif isinstance(stmt, WhileStatement):
        cond_str = emit_condition(stmt.condition)
        body_str= '\n'.join(emit_stmt(s) for s in stmt.body)
        result = f'while {cond_str}:\n'
        for line in body_str.split('\n'):
            if line:
                result += f'    {line}\n'
        return result
    
    elif isinstance(stmt, VarUpdate):
        if stmt.delta >= 0:
            return f'{stmt.name} += {stmt.delta}\n'
        else:
            return f'{stmt.name} -= {abs(stmt.delta)}\n'
        
    elif isinstance(stmt, ForStatement):
        if (stmt.init and isinstance(stmt.init, Variable) and stmt.init.value.isdigit() and
            stmt.condition and isinstance(stmt.condition, BinaryCondition) and 
            stmt.condition.left == stmt.init.name and stmt.condition.right.isdigit() and
            stmt.update and isinstance(stmt.update, VarUpdate) and abs(stmt.update.delta) == 1):
            
            start = int(stmt.init.value)
            end = int(stmt.condition.right)
            var_name = stmt.init.name
            op = stmt.condition.operator
            step = stmt.update.delta
            
            # map Java operators to Python range() bounds
            if op == '<' and step == 1:
                range_args = f'{start}, {end}'
            elif op == '<=' and step == 1:
                range_args = f'{start}, {end + 1}'
            elif op == '>' and step == -1:
                range_args = f'{start}, {end}, -1'
            elif op == '>=' and step == -1:
                range_args = f'{start}, {end - 1}, -1'
            elif op == '==' and step == 1:
                range_args = f'{start}, {start + 1}'
            elif op == '!=' and step == 1:
                range_args = f'{start}, {end}'
            else:
                range_args = None
            
            if range_args:
                body_str = '\n'.join(emit_stmt(s) for s in stmt.body)
                result = f'for {var_name} in range({range_args}):\n'
                for line in body_str.split('\n'):
                    if line:
                        result += f'    {line}\n'
                return result
        
        # fallback to emit as while loops for complex cases
        else:
            lines = []
            if stmt.init is not None:
                lines.append(emit_stmt(stmt.init))
            
            cond_str = 'True' if stmt.condition is None else emit_condition(stmt.condition)
            
            body_lines = [emit_stmt(s) for s in stmt.body]
            if stmt.update is not None:
                body_lines.append(emit_stmt(stmt.update))
            
            body_str = ''.join(body_lines)
            result = f'while {cond_str}:\n'
            for line in body_str.split('\n'):
                if line:
                    result += f'    {line}\n'
            return ''.join(lines) + result

    raise NotImplementedError(f"No emitter for {type(stmt).__name__}")
