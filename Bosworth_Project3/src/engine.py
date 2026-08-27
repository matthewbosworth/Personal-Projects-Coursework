"""
engine.py – Core reasoning engine for PrefAgent.

"""
from src.formula import evaluate


#Object generation & helpers 

def generate_all_objects(attributes: list) -> list[dict[str, bool]]:
    #Generate all 2^n objects as truth-assignment dicts.

    
    n = len(attributes)
    objects = []
    for i in range(2 ** n):
        obj: dict[str, bool] = {}
        for j, (_, values) in enumerate(attributes):
            bit = (i >> (n - 1 - j)) & 1
            obj[values[0]] = (bit == 1)   # first value  → 1
            obj[values[1]] = (bit == 0)   # second value → 0
        objects.append(obj)
    return objects


def object_label(idx: int) -> str:
    """Return display label for an object, e.g. 'o7'."""
    return f"o{idx}"


def object_to_display(obj: dict, attributes: list) -> str:
    """Return comma-separated string of the active value for each attribute."""
    parts = []
    for _, values in attributes:
        parts.append(values[0] if obj[values[0]] else values[1])
    return ', '.join(parts)


# Feasibility 

def get_feasible_indices(all_objects: list, constraints: list) -> list[int]:
    """Return the indices of objects that satisfy *all* hard constraints."""
    return [
        i for i, obj in enumerate(all_objects)
        if all(evaluate(c, obj) for c in constraints)
    ]


# Penalty Logic 

def compute_penalties(obj: dict, pl_rules: list) -> tuple[list[int], int]:
    """Compute per-rule and total penalties for an object.

    A rule (formula, penalty) incurs its penalty when the formula is *false*
    for the given object (i.e., the object violates the soft constraint).

    """
    individual = []
    total = 0
    for _, formula, penalty in pl_rules:
        p = 0 if evaluate(formula, obj) else penalty
        individual.append(p)
        total += p
    return individual, total


def penalty_compare(obj1: dict, obj2: dict, pl_rules: list) -> str:
    """Compare two objects under Penalty Logic.

    Lower total penalty = strictly preferred.

    """
    _, t1 = compute_penalties(obj1, pl_rules)
    _, t2 = compute_penalties(obj2, pl_rules)
    if t1 < t2:
        return 'prefer1'
    if t2 < t1:
        return 'prefer2'
    return 'equivalent'


def get_optimal_penalty(all_objects: list, feasible_indices: list, pl_rules: list) -> list[int]:
    """Return indices of feasible objects with the minimum total penalty."""
    scored = [(i, compute_penalties(all_objects[i], pl_rules)[1]) for i in feasible_indices]
    min_p = min(s for _, s in scored)
    return [i for i, s in scored if s == min_p]


# Qualitative Choice Logic

def qcl_rank(obj: dict, chain_formulas: list, psi_formula: tuple) -> int:
    """Compute the rank of *obj* under a single QCL rule (chain_formulas, psi_formula).

    Ranking semantics:
        rank 0        – obj does NOT satisfy ψ (outside the comparison context).
                        Being outside the context is treated as the *best* possible
                        rank for this rule (smaller rank = better).
        rank 1 .. n   – obj satisfies ψ and the first φ_i it satisfies has index i.
        rank n+1      – obj satisfies ψ but none of the φ's in the chain.
    """
    if not evaluate(psi_formula, obj):
        return 0  # outside context → "best" for this rule
    for k, phi in enumerate(chain_formulas):
        if evaluate(phi, obj):
            return k + 1
    return len(chain_formulas) + 1


def qcl_compare(obj1: dict, obj2: dict, qcl_rules: list) -> str:
    """Compare two objects under all QCL rules.

    Aggregation:
      • Collect whether each rule strictly prefers obj1 (rank1 < rank2)
        or strictly prefers obj2 (rank2 < rank1).
      • 'prefer1'      – some rule prefers obj1, none prefer obj2
      • 'prefer2'      – some rule prefers obj2, none prefer obj1
      • 'equivalent'   – no rule strictly prefers either
      • 'incomparable' – some rule prefers obj1 AND some rule prefers obj2

    """
    prefer1 = False
    prefer2 = False
    for _, chain_formulas, _, psi_formula in qcl_rules:
        r1 = qcl_rank(obj1, chain_formulas, psi_formula)
        r2 = qcl_rank(obj2, chain_formulas, psi_formula)
        if r1 < r2:
            prefer1 = True
        elif r2 < r1:
            prefer2 = True

    if prefer1 and not prefer2:
        return 'prefer1'
    if prefer2 and not prefer1:
        return 'prefer2'
    if not prefer1 and not prefer2:
        return 'equivalent'
    return 'incomparable'


def get_optimal_qcl(all_objects: list, feasible_indices: list, qcl_rules: list) -> list[int]:
    """Return indices of non-dominated feasible objects (Pareto-optimal set).

    An object o is *dominated* if some other feasible object is strictly
    preferred over o under qcl_compare.
    """
    optimal = []
    for i in feasible_indices:
        dominated = any(
            qcl_compare(all_objects[j], all_objects[i], qcl_rules) == 'prefer1'
            for j in feasible_indices if j != i
        )
        if not dominated:
            optimal.append(i)
    return optimal
