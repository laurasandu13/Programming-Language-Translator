from parser import Print, Variable

def emit_module(mod):
    lines = []
    for stmt in mod.body:
        lines.append(emit_stmt(stmt))
    return "".join(lines) 

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
    raise NotImplementedError(f"No emitter for {type(stmt).__name__}")
