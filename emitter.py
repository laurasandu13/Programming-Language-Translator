def emit_module(mod):
    lines = []
    for stmt in mod.body:
        lines.append(emit_stmt(stmt))
    return "".join(lines) 

def emit_stmt(stmt):
    if stmt.__class__.__name__ == "Print": 
        return f"print({stmt.args[0]})\n"
    raise NotImplementedError(f"No emitter for {type(stmt).__name__}")
