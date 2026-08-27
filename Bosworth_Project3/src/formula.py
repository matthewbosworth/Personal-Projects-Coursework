"""
formula.py – Tokenize, parse, and evaluate propositional formulas.

Supported connectives : NOT, AND, OR
Operator precedence (tightest first): NOT > AND > OR
Literals: lower-case value names such as 'fish', 'ice-cream', 'not-soup'
"""
import re


# Tokenizer 

def tokenize(s: str) -> list[str]:
    """Split a formula string into a list of tokens."""
    if not s or not s.strip():
        return []
    # Keywords are matched first
    return re.findall(r'AND|OR|NOT|\(|\)|[a-zA-Z0-9][a-zA-Z0-9_\-]*', s)


# Recursive-descent parser 

class _Parser:
    """Builds an AST from a token list. Grammar (lowest to highest precedence):
        expr   ::= and_expr (OR and_expr)*
        and_expr ::= not_expr (AND not_expr)*
        not_expr ::= NOT atom | atom
        atom     ::= '(' expr ')' | LITERAL
    """

    def __init__(self, tokens: list[str]):
        self.tokens = tokens
        self.pos = 0

    def _peek(self) -> str | None:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _consume(self) -> str:
        t = self.tokens[self.pos]
        self.pos += 1
        return t

    def parse(self):
        if not self.tokens:
            return ('TRUE',)
        node = self._parse_or()
        return node

    def _parse_or(self):
        left = self._parse_and()
        while self._peek() == 'OR':
            self._consume()
            right = self._parse_and()
            left = ('OR', left, right)
        return left

    def _parse_and(self):
        left = self._parse_not()
        while self._peek() == 'AND':
            self._consume()
            right = self._parse_not()
            left = ('AND', left, right)
        return left

    def _parse_not(self):
        if self._peek() == 'NOT':
            self._consume()
            return ('NOT', self._parse_atom())
        return self._parse_atom()

    def _parse_atom(self):
        tok = self._peek()
        if tok == '(':
            self._consume()
            expr = self._parse_or()
            closing = self._peek()
            if closing != ')':
                raise ValueError(f"Expected ')', got {closing!r}")
            self._consume()
            return expr
        if tok is None or tok in ('AND', 'OR', 'NOT', ')'):
            raise ValueError(f"Unexpected token: {tok!r}")
        self._consume()
        return ('LIT', tok)


# Public API ──

def parse_formula(s: str):
    """Parse a formula string and return an AST tuple.

    AST node types:
        ('TRUE',)            – always-true constant (empty formula)
        ('LIT', name)        – propositional literal
        ('NOT', child)       – negation
        ('AND', left, right) – conjunction
        ('OR',  left, right) – disjunction
    """
    if not s or not s.strip():
        return ('TRUE',)
    tokens = tokenize(s)
    return _Parser(tokens).parse()


def evaluate(node: tuple, assignment: dict[str, bool]) -> bool:
    """Evaluate an AST node against a truth-assignment dict {value_name: bool}.

    Values absent from the assignment are treated as False.
    """
    kind = node[0]
    if kind == 'TRUE':
        return True
    if kind == 'LIT':
        return bool(assignment.get(node[1], False))
    if kind == 'NOT':
        return not evaluate(node[1], assignment)
    if kind == 'AND':
        return evaluate(node[1], assignment) and evaluate(node[2], assignment)
    if kind == 'OR':
        return evaluate(node[1], assignment) or evaluate(node[2], assignment)
    raise ValueError(f"Unknown AST node type: {kind!r}")
