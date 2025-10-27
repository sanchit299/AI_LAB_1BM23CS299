import re
import copy

class Predicate:
    def __init__(self, predicate_string):
        self.predicate_string = predicate_string
        self.name, self.arguments, self.negative = self.parse_predicate(predicate_string)

    def parse_predicate(self, predicate_string):
        neg = predicate_string.startswith('~')
        if neg:
            predicate_string = predicate_string[1:]
        m = re.match(r"([A-Za-z_][A-Za-z0-9_]*)\((.*?)\)", predicate_string)
        if not m:
            raise ValueError(f"Invalid predicate: {predicate_string}")
        name, args = m.groups()
        args = [a.strip() for a in args.split(",")]
        return name, args, neg

    def negate(self):
        self.negative = not self.negative
        if self.predicate_string.startswith('~'):
            self.predicate_string = self.predicate_string[1:]
        else:
            self.predicate_string = '~' + self.predicate_string

    def unify_with_predicate(self, other):
        if self.name != other.name or len(self.arguments) != len(other.arguments):
            return False
        subs = {}
        for a, b in zip(self.arguments, other.arguments):
            if a == b:
                continue
            if a[0].islower():
                subs[a] = b
            elif b[0].islower():
                subs[b] = a
            else:
                return False
        return subs

    def substitute(self, subs):
        self.arguments = [subs.get(a, a) for a in self.arguments]
        self.predicate_string = (
            ('~' if self.negative else '') +
            self.name + '(' + ','.join(self.arguments) + ')'
        )

    def __repr__(self):
        return self.predicate_string


class Statement:
    def __init__(self, statement_string):
        self.statement_string = statement_string
        self.predicate_set = self.parse_statement(statement_string)

    def parse_statement(self, statement_string):
        parts = statement_string.split('|')
        predicates = []
        for p in parts:
            predicates.append(Predicate(p.strip()))
        return set(predicates)

    def add_statement_to_KB(self, KB, KB_HASH):
        KB.add(self)
        for predicate in self.predicate_set:
            key = predicate.name
            if key not in KB_HASH:
                KB_HASH[key] = set()
            KB_HASH[key].add(self)

    def get_resolving_clauses(self, KB_HASH):
        resolving_clauses = set()
        for predicate in self.predicate_set:
            key = predicate.name
            if key in KB_HASH:
                resolving_clauses |= KB_HASH[key]
        return resolving_clauses

    def resolve(self, other):
        new_statements = set()
        for p1 in self.predicate_set:
            for p2 in other.predicate_set:
                if p1.name == p2.name and p1.negative != p2.negative:
                    subs = p1.unify_with_predicate(p2)
                    if subs is False:
                        continue
                    new_pred_set = set()
                    for pred in self.predicate_set.union(other.predicate_set):
                        if pred not in (p1, p2):
                            pred_copy = copy.deepcopy(pred)
                            pred_copy.substitute(subs)
                            new_pred_set.add(pred_copy)
                    if not new_pred_set:
                        return False
                    new_stmt = Statement('|'.join(sorted([str(p) for p in new_pred_set])))
                    new_statements.add(new_stmt)
        return new_statements

    def __repr__(self):
        return self.statement_string


def fol_to_cnf_clauses(sentence):
    sentence = sentence.replace(' ', '')
    if '=>' in sentence:
        lhs, rhs = sentence.split('=>')
        parts = lhs.split('&')
        negated_lhs = ['~' + p for p in parts]
        disjunction = '|'.join(negated_lhs + [rhs])
        return [disjunction]
    if '&' in sentence:
        return sentence.split('&')
    return [sentence]


KILL_LIMIT = 8000

def prepare_knowledgebase(fol_sentences):
    KB = set()
    KB_HASH = {}
    for sentence in fol_sentences:
        clauses = fol_to_cnf_clauses(sentence)
        for clause in clauses:
            stmt = Statement(clause)
            stmt.add_statement_to_KB(KB, KB_HASH)
    return KB, KB_HASH

def FOL_Resolution(KB, KB_HASH, query):
    KB2 = set()
    query.add_statement_to_KB(KB2, KB_HASH)
    query.add_statement_to_KB(KB, KB_HASH)
    while True:
        new_statements = set()
        if len(KB) > KILL_LIMIT:
            return False
        for s1 in KB:
            for s2 in s1.get_resolving_clauses(KB_HASH):
                if s1 == s2:
                    continue
                resolvents = s1.resolve(s2)
                if resolvents is False:
                    return True
                new_statements |= resolvents
        if new_statements.issubset(KB):
            return False
        new_statements -= KB
        KB |= new_statements

def main():
    fol_sentences = [
        "Parent(John, Mary)",
        "Parent(Mary, Sam)",
        "Parent(x, y) => Ancestor(x, y)",
        "Parent(x, y) & Ancestor(y, z) => Ancestor(x, z)"
    ]
    queries = ["Ancestor(John, Sam)"]
    KB, KB_HASH = prepare_knowledgebase(fol_sentences)
    print("\nKnowledge Base CNF Clauses:")
    for stmt in KB:
        print("  ", stmt)
    for query_str in queries:
        query_predicate = Predicate(query_str)
        query_predicate.negate()
        query_stmt = Statement(str(query_predicate))
        satisfiable = FOL_Resolution(copy.deepcopy(KB), copy.deepcopy(KB_HASH), query_stmt)
        print(f"\nQuery: {query_str} =>", "TRUE" if satisfiable else "FALSE")
    print("\nSanchit Mehta 1BM23CS299")

if __name__ == "__main__":
    main()
