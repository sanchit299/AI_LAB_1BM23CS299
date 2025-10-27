from itertools import combinations

def pl_resolution(KB, query):
    # Negate the query and add to KB
    clauses = KB + [negate(query)]
    print("Initial Clauses:")
    for c in clauses:
        print(c)
    print("-" * 40)

    new = set()
    while True:
        # Generate all possible pairs of clauses
        pairs = list(combinations(clauses, 2))
        for (ci, cj) in pairs:
            resolvents = resolve(ci, cj)
            if [] in resolvents:
                print(f"Derived empty clause from {ci} and {cj}")
                return True
            new.update(tuple(sorted(r)) for r in resolvents)
        
        if new.issubset(set(tuple(sorted(c)) for c in clauses)):
            # No new clauses added — cannot derive contradiction
            return False
        for c in new:
            if list(c) not in clauses:
                clauses.append(list(c))

def resolve(ci, cj):
    """Resolve two clauses and return the resolvents."""
    resolvents = []
    for di in ci:
        for dj in cj:
            if di == negate(dj):
                new_clause = list(set(ci + cj))
                new_clause.remove(di)
                new_clause.remove(dj)
                resolvents.append(new_clause)
    return resolvents

def negate(literal):
    """Negate a literal."""
    if literal.startswith('~'):
        return literal[1:]
    else:
        return '~' + literal


KB = [
    ['~R', 'W'],
    ['~W', 'G'],
    ['R']
]

query = 'G'

# --- Run Resolution ---
entailed = pl_resolution(KB, query)
print("1BM23CS299 Sanchit Mehta")
print("\nResult:")
if entailed:
    print(f"✅ The knowledge base entails {query}.")
else:
    print(f"❌ The knowledge base does NOT entail {query}.")
