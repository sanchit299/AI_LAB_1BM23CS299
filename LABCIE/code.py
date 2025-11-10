class Fact:
    """Represents a simple fact."""
    def __init__(self, predicate, *args):
        self.predicate = predicate
        self.args = args

    def __eq__(self, other):
        return isinstance(other, Fact) and \
               self.predicate == other.predicate and \
               self.args == other.args

    def __hash__(self):
        return hash((self.predicate, self.args))

    def __repr__(self):
        return f'{self.predicate}({", ".join(self.args)})'

class Rule:
    """Represents an IF-THEN rule."""
    def __init__(self, antecedent, consequent):
        self.antecedent = antecedent  # A list of facts
        self.consequent = consequent  # A single fact

    def __repr__(self):
        return f'IF {self.antecedent} THEN {self.consequent}'

def prove_query(facts, rules, query):
   
    working_memory = set(facts)
    new_facts_in_cycle = True
    iteration = 0

    print("--- Starting Forward Reasoning System ---")
    print(f"Initial facts: {[str(f) for f in working_memory]}\n")

    
    while new_facts_in_cycle:
        iteration += 1
        new_facts_in_cycle = False
        
        
        
        for rule in rules:
            
            if all(fact in working_memory for fact in rule.antecedent):
                consequent = rule.consequent
                
               
                if consequent not in working_memory:
                    print(f"Applying rule: {rule}")
                    print(f"Derived new fact: {consequent}\n")
                    working_memory.add(consequent)
                    new_facts_in_cycle = True
                    
                  
                    if consequent == query:
                        print("Query proven: Ice-creams are available.")
                        return True
    
    print("No more new facts can be derived.")
    if query in working_memory:
        print("Query proven: Ice-creams are available.")
        return True
    else:
        print("Query not proven.")
        return False

fact1 = Fact('Darjeeling', 'holiday_spot')

fact2 = Fact('is_visited', 'Darjeeling')

rule1 = Rule(antecedent=[Fact('is', 'X', 'holiday_spot')],
             consequent=Fact('ice_creams_available_at', 'X'))

fact4 = Fact('highly_visited', 'Darjeeling')

fact5 = Fact('is_not', 'Munar')
facts = [
    Fact('is', 'Darjeeling', 'holiday_spot'),
    Fact('is_visited', 'Darjeeling')
]
rules = [
    Rule(antecedent=[Fact('is', 'Darjeeling', 'holiday_spot')],
         consequent=Fact('ice_creams_available_at', 'Darjeeling'))
]

query_to_prove = Fact('ice_creams_available_at', 'Darjeeling')


prove_query(facts, rules, query_to_prove)
