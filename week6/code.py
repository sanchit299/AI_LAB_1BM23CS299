def parse_expr(tokens):
    token = tokens.pop(0)
    if token == '(':
        op = tokens.pop(0)
        args = []
        while tokens[0] != ')':
            args.append(parse_expr(tokens))
        tokens.pop(0)  # Remove ')'
        return (op, *args)
    else:
        return token

def tokenize(s):
    return s.replace('(', ' ( ').replace(')', ' ) ').split()

def tt_entails(kb, alpha):
    symbols = list(get_symbols(kb) | get_symbols(alpha))
    print("Symbols:", symbols)
    
  
    header = symbols + ['KB', 'α']
    print("\t".join(header))
    
    # Start recursive check
    result = tt_check_all(kb, alpha, symbols, {})
    return result

def tt_check_all(kb, alpha, symbols, model):
    if not symbols:
        kb_val = pl_true(kb, model)
        alpha_val = pl_true(alpha, model)
        # Print current model and values
        row = [str(model.get(s, False)) for s in sorted(model.keys())] + [str(kb_val), str(alpha_val)]
        print("\t".join(row))
        
        if kb_val:
            return alpha_val
        else:
            return True
    else:
        rest = symbols[1:]
        symbol = symbols[0]
        model_true = model.copy()
        model_true[symbol] = True
        model_false = model.copy()
        model_false[symbol] = False
        return (tt_check_all(kb, alpha, rest, model_true) and
                tt_check_all(kb, alpha, rest, model_false))

def get_symbols(expr):
    if isinstance(expr, str):
        return {expr}
    elif isinstance(expr, tuple):
        symbols = set()
        for part in expr[1:] if expr[0] != 'not' else [expr[1]]:
            symbols |= get_symbols(part)
        return symbols
    else:
        return set()

def pl_true(expr, model):
    if isinstance(expr, str):
        return model.get(expr, False)
    op = expr[0]
    if op == 'and':
        return all(pl_true(arg, model) for arg in expr[1:])
    elif op == 'or':
        return any(pl_true(arg, model) for arg in expr[1:])
    elif op == 'not':
        return not pl_true(expr[1], model)
    elif op == 'implies':
        return (not pl_true(expr[1], model)) or pl_true(expr[2], model)
    else:
        raise ValueError(f"Unknown operator: {op}")


kb_input = input("Enter knowledge base (e.g. (and A (or B C))): ")
alpha_input = input("Enter query (e.g. A): ")

kb = parse_expr(tokenize(kb_input))
alpha = parse_expr(tokenize(alpha_input))

result = tt_entails(kb, alpha)
print(f"\nDoes KB entail α? : {result}")
