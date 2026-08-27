"""
display.py – ASCII table rendering for PrefAgent output.
"""
from src.engine import object_label, compute_penalties, qcl_rank


#Table builder

def _build_table(headers: list[str], rows: list[list[str]]) -> str:
    
    n_cols = len(headers)

    # Compute column widths
    col_widths = []
    for c in range(n_cols):
        w = len(headers[c])
        for row in rows:
            w = max(w, len(row[c]))
        col_widths.append(w)

    def sep_line() -> str:
        return '+' + '+'.join('-' * (w + 2) for w in col_widths) + '+'

    def data_line(cells: list[str]) -> str:
        parts = [f' {cells[c]:<{col_widths[c]}} ' for c in range(n_cols)]
        return '|' + '|'.join(parts) + '|'

    lines = [sep_line(), data_line(headers), sep_line()]
    for row in rows:
        lines.append(data_line(row))
    lines.append(sep_line())
    return '\n'.join(lines)


# Penalty Logic table 

def print_penalty_table(all_objects: list, feasible_indices: list,
                        attributes: list, pl_rules: list) -> None:
    #Print the penalty table for all feasible objects.
    
    headers = ['encoding'] + [fs for fs, _, _ in pl_rules] + ['total penalty']
    rows = []
    for i in feasible_indices:
        individual, total = compute_penalties(all_objects[i], pl_rules)
        rows.append([object_label(i)] + [str(p) for p in individual] + [str(total)])
    print(_build_table(headers, rows))


# QCL table

def print_qcl_table(all_objects: list, feasible_indices: list,
                    attributes: list, qcl_rules: list) -> None:
    #Print the QCL rank table for all feasible objects.

   
    rule_labels = []
    for chain_strs, _, psi_str, _ in qcl_rules:
        label = ' BT '.join(chain_strs)
        if psi_str:
            label += f' IF {psi_str}'
        rule_labels.append(label)

    headers = ['encoding'] + rule_labels
    rows = []
    for i in feasible_indices:
        obj = all_objects[i]
        ranks = [str(qcl_rank(obj, cf, pf)) for _, cf, _, pf in qcl_rules]
        rows.append([object_label(i)] + ranks)
    print(_build_table(headers, rows))
