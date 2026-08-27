
import random
import sys
import os

# Ensure the project root is on the Python path so 'src.*' imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.parser import parse_attributes, parse_constraints, parse_penalty_logic, parse_qcl
from src.engine import (
    generate_all_objects, object_label, object_to_display,
    get_feasible_indices,
    compute_penalties, penalty_compare, get_optimal_penalty,
    qcl_compare, get_optimal_qcl,
)
from src.display import print_penalty_table, print_qcl_table


# UI helpers 

def get_valid_choice(valid_set: set[str]) -> str:
    """Prompt until the user enters a choice that is in valid_set."""
    choice = input("Your Choice: ").strip()
    while choice not in valid_set:
        choice = input("Wrong Choice! Enter your choice: ").strip()
    return choice


# Shared tasks

def task_encoding(all_objects: list, attributes: list) -> None:
    for i, obj in enumerate(all_objects):
        print(f"o{i} \u2013 {object_to_display(obj, attributes)}")


def task_feasibility(feasible_indices: list) -> None:
    n = len(feasible_indices)
    if n == 0:
        print("No, there are no feasible objects.")
    else:
        print(f"Yes, there are {n} feasible objects.")


def task_exemplification(all_objects: list, feasible_indices: list,
                          compare_fn) -> None:
    """Randomly pick two feasible objects and show their preference relation."""
    if len(feasible_indices) < 2:
        print("Not enough feasible objects for exemplification (need at least 2).")
        return

    idx1, idx2 = random.sample(feasible_indices, 2)
    lbl1, lbl2 = object_label(idx1), object_label(idx2)
    result = compare_fn(all_objects[idx1], all_objects[idx2])

    print(f"Two randomly selected feasible objects are {lbl1} and {lbl2},")
    if result == 'prefer1':
        print(f"and {lbl1} is strictly preferred over {lbl2}.")
    elif result == 'prefer2':
        print(f"and {lbl2} is strictly preferred over {lbl1}.")
    elif result == 'equivalent':
        print(f"and {lbl1} and {lbl2} are equivalent.")
    else:
        print(f"and {lbl1} and {lbl2} are incomparable.")


def task_omni_optimization(optimal_indices: list) -> None:
    if not optimal_indices:
        print("No optimal objects found.")
    else:
        labels = ', '.join(object_label(i) for i in optimal_indices)
        print(f"All optimal objects: {labels}")


# Task sub-menu 

def run_task_menu(all_objects: list, feasible_indices: list,
                  attributes: list, mode: str, rules: list) -> None:
    """Interactive task menu for a chosen preference logic.

    mode: 'penalty' | 'qcl'
    rules: parsed penalty-logic rules OR parsed QCL rules
    """

    # Pre-build mode-specific helpers to keep the loop clean
    if mode == 'penalty':
        show_table   = lambda: print_penalty_table(all_objects, feasible_indices, attributes, rules)
        compare_fn   = lambda o1, o2: penalty_compare(o1, o2, rules)
        optimal_fn   = lambda: get_optimal_penalty(all_objects, feasible_indices, rules)
    else:  # 'qcl'
        show_table   = lambda: print_qcl_table(all_objects, feasible_indices, attributes, rules)
        compare_fn   = lambda o1, o2: qcl_compare(o1, o2, rules)
        optimal_fn   = lambda: get_optimal_qcl(all_objects, feasible_indices, rules)

    while True:
        print("\nChoose the reasoning task to perform:")
        print("1. Encoding")
        print("2. Feasibility Checking")
        print("3. Show the Table")
        print("4. Exemplification")
        print("5. Omni-optimization")
        print("6. Back to previous menu")

        choice = get_valid_choice({'1', '2', '3', '4', '5', '6'})

        if choice == '1':
            task_encoding(all_objects, attributes)

        elif choice == '2':
            task_feasibility(feasible_indices)

        elif choice == '3':
            show_table()

        elif choice == '4':
            task_exemplification(all_objects, feasible_indices, compare_fn)

        elif choice == '5':
            task_omni_optimization(optimal_fn())

        elif choice == '6':
            break


# Main loop 

def main() -> None:
    print("Welcome to PrefAgent!")

    # Load attributes and constraints  
    attr_file = input("Enter Attributes File Name: ").strip()
    attributes = parse_attributes(attr_file)

    constraint_file = input("Enter Hard Constraints File Name: ").strip()
    constraints = parse_constraints(constraint_file)

    # Build the complete object space and filter for feasible objects once
    all_objects = generate_all_objects(attributes)
    feasible_indices = get_feasible_indices(all_objects, constraints)

    # Logic selection loop
    while True:
        print("\nChoose the preference logic to use:")
        print("1. Penalty Logic")
        print("2. Qualitative Choice Logic")
        print("3. Exit")

        choice = get_valid_choice({'1', '2', '3'})

        if choice == '1':
            print("You picked Penalty Logic")
            pref_file = input("Enter Preferences File Name: ").strip()
            pl_rules = parse_penalty_logic(pref_file)
            run_task_menu(all_objects, feasible_indices, attributes, 'penalty', pl_rules)

        elif choice == '2':
            print("You picked Qualitative Choice Logic")
            pref_file = input("Enter Preferences File Name: ").strip()
            qcl_rules = parse_qcl(pref_file)
            run_task_menu(all_objects, feasible_indices, attributes, 'qcl', qcl_rules)

        elif choice == '3':
            print("Bye!")
            break


if __name__ == '__main__':
    main()
