from typing import List, Tuple, Dict, Set, Union

Predicate = Tuple[str, Tuple[str, ...]]

class Rule:
    def __init__(self, head: Predicate, body: List[Predicate]):
        self.head = head
        self.body = body

    def __repr__(self):
        body_str = ', '.join(f"{p[0]}{p[1]}" for p in self.body)
        return f"{body_str} => {self.head[0]}{self.head[1]}"

# Knowledge base
class KnowledgeBase:
    def __init__(self):
        self.facts: Set[Predicate] = set()
        self.rules: List[Rule] = []

    def add_fact(self, fact: Predicate):
        self.facts.add(fact)

    def add_rule(self, rule: Rule):
        self.rules.append(rule)

    def forward_chain(self, query: Predicate) -> bool:
        inferred = set(self.facts)
        added = True

        while added:
            added = False
            for rule in self.rules:
                if all(self._match_fact(body_pred, inferred) for body_pred in rule.body):
                    if not self._match_fact(rule.head, inferred):
                        inferred.add(rule.head)
                        added = True
                        print(f"Inferred: {rule.head}")

                        if self._match_fact(query, inferred):
                            return True
        return self._match_fact(query, inferred)

    def _match_fact(self, pred: Predicate, fact_set: Set[Predicate]) -> bool:
        return pred in fact_set

# --- Example usage ---
if __name__ == "__main__":
    kb = KnowledgeBase()

    kb.add_fact(("Parent", ("John", "Mary")))
    kb.add_fact(("Parent", ("Mary", "Sue")))

    facts_list = list(kb.facts)
    for f1 in facts_list:
        for f2 in facts_list:
            if f1[0] == "Parent" and f2[0] == "Parent":
                if f1[1][1] == f2[1][0]:
                    head = ("Grandparent", (f1[1][0], f2[1][1]))
                    body = [f1, f2]
                    kb.add_rule(Rule(head, body))

    query = ("Grandparent", ("John", "Sue"))
    result = kb.forward_chain(query)

    print(f"Query {query} is", "True" if result else "False")
    print("sanchit 1bm23cs299") 
