"""
parser.py – Load and parse all PrefAgent input files.
"""
from src.formula import parse_formula


# Attributes 

def parse_attributes(filename: str) -> list[tuple[str, list[str]]]:
    """Parse an attributes file.

    """
    attributes = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            attr, rest = line.split(':', 1)
            v1, v2 = [v.strip() for v in rest.split(',', 1)]
            attributes.append((attr.strip(), [v1, v2]))
    return attributes


# Hard Constraints 

def parse_constraints(filename: str) -> list[tuple]:
    """Parse a hard-constraints file.

    Each non-empty line is one CNF clause (disjunction of literals).
    Returns a list of parsed formula AST tuples.
    """
    formulas = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                formulas.append(parse_formula(line))
    return formulas


# Penalty Logic

def parse_penalty_logic(filename: str) -> list[tuple[str, tuple, int]]:
    """Parse a penalty-logic preferences file.

    Each line:  <CNF formula>, <integer penalty>
    The last comma in the line separates the formula from the penalty.

    """
    rules = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            idx = line.rfind(',')
            formula_str = line[:idx].strip()
            penalty = int(line[idx + 1:].strip())
            rules.append((formula_str, parse_formula(formula_str), penalty))
    return rules


# Qualitative Choice Logic 

def parse_qcl(filename: str) -> list[tuple[list[str], list[tuple], str, tuple]]:
    """Parse a qualitative-choice-logic preferences file.

    Each line:  phi_1 BT phi_2 BT ... BT phi_n IF psi
    The condition psi (after IF) may be empty, meaning the rule always applies.

    Returns a list of:
        (chain_strings, chain_formulas, psi_string, psi_formula)
    where chain_strings / chain_formulas are lists of the φ components in order.
    """
    rules = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Split on the first (and only) ' IF ' keyword
            if ' IF ' in line:
                chain_part, psi_str = line.split(' IF ', 1)
                psi_str = psi_str.strip()
            else:
                chain_part = line
                psi_str = ''

            chain_strs = [p.strip() for p in chain_part.split(' BT ')]
            chain_formulas = [parse_formula(p) for p in chain_strs]
            psi_formula = parse_formula(psi_str)  # ('TRUE',) when psi_str is empty
            rules.append((chain_strs, chain_formulas, psi_str, psi_formula))
    return rules
