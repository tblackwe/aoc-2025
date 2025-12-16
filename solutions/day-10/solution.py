#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 10: Factory
Solve button-pressing optimization problems using linear algebra.

Part 1: Toggle lights using buttons (XOR logic over GF(2))
Part 2: Increment counters using buttons (Integer Linear Programming)
"""

from typing import List, Tuple
from itertools import product
import re


class Machine:
    """Representation of a machine with lights and buttons."""
    def __init__(self, target, buttons):
        self.target = target  # Target state for each light (0 or 1)
        self.buttons = buttons  # Each button is a list of light indices it toggles


def parse_machine(line: str) -> Machine:
    """
    Parse a single machine specification line.
    
    Args:
        line: Input line with format: [diagram] (button1) ... (buttonN) {joltage}
    
    Returns:
        Machine object with target state and button configurations
    """
    # Extract indicator diagram between [ and ]
    diagram_match = re.search(r'\[(.*?)\]', line)
    diagram = diagram_match.group(1)
    
    # Convert diagram to binary target: '#' -> 1, '.' -> 0
    target = [1 if c == '#' else 0 for c in diagram]
    
    # Extract all button patterns between ( and )
    button_matches = re.findall(r'\(([0-9,]+)\)', line)
    buttons = []
    for button_str in button_matches:
        indices = [int(x) for x in button_str.split(',')]
        buttons.append(indices)
    
    return Machine(target, buttons)


def parse_input(text: str) -> List[Machine]:
    """
    Parse all machines from input text.
    
    Args:
        text: Multi-line input string
    
    Returns:
        List of Machine objects
    """
    machines = []
    for line in text.strip().split('\n'):
        if line:
            machines.append(parse_machine(line))
    return machines


# ===========================
# Part 1: Toggle Lights (GF(2))
# ===========================

def build_matrix(machine: Machine) -> List[List[int]]:
    """
    Build augmented matrix [A | b] for Gaussian elimination over GF(2).
    Matrix[i][j] = 1 if button j toggles light i.
    Matrix[i][num_buttons] = target state of light i.
    
    Args:
        machine: Machine object
    
    Returns:
        Augmented matrix for solving system of equations
    """
    num_lights = len(machine.target)
    num_buttons = len(machine.buttons)
    
    matrix = []
    for light_idx in range(num_lights):
        row = [0] * (num_buttons + 1)
        
        # Check each button to see if it toggles this light
        for button_idx, button in enumerate(machine.buttons):
            if light_idx in button:
                row[button_idx] = 1
        
        # Augment with target state
        row[num_buttons] = machine.target[light_idx]
        matrix.append(row)
    
    return matrix


def gaussian_elimination_gf2(matrix: List[List[int]]) -> Tuple[List[List[int]], List[int]]:
    """
    Perform Gaussian elimination over GF(2) (binary field with XOR arithmetic).
    
    Args:
        matrix: Augmented matrix [A | b]
    
    Returns:
        Tuple of (reduced_matrix, pivot_cols)
    """
    num_rows = len(matrix)
    if num_rows == 0:
        return matrix, []
    
    num_cols = len(matrix[0]) - 1  # Exclude augmented column
    
    pivot_row = 0
    pivot_cols = []
    
    # Forward elimination with partial pivoting
    for col in range(num_cols):
        # Find pivot in this column
        found_pivot = False
        for row in range(pivot_row, num_rows):
            if matrix[row][col] == 1:
                # Swap rows if needed
                if row != pivot_row:
                    matrix[pivot_row], matrix[row] = matrix[row], matrix[pivot_row]
                found_pivot = True
                break
        
        if not found_pivot:
            continue  # Free variable
        
        pivot_cols.append(col)
        
        # Eliminate all other 1s in this column (reduced row echelon form)
        for row in range(num_rows):
            if row != pivot_row and matrix[row][col] == 1:
                # XOR this row with pivot row
                for c in range(num_cols + 1):
                    matrix[row][c] ^= matrix[pivot_row][c]
        
        pivot_row += 1
    
    return matrix, pivot_cols


def find_minimum_solution(matrix: List[List[int]], pivot_cols: List[int]) -> int:
    """
    Find minimum number of button presses from reduced matrix.
    
    Args:
        matrix: Reduced augmented matrix
        pivot_cols: List of column indices that have pivots
    
    Returns:
        Minimum number of button presses, or float('inf') if unsolvable
    """
    if len(matrix) == 0:
        return 0
    
    num_buttons = len(matrix[0]) - 1
    
    # Check for inconsistency: 0 = 1
    for row in matrix:
        if all(row[i] == 0 for i in range(num_buttons)) and row[num_buttons] == 1:
            return float('inf')
    
    # Identify free variables
    free_vars = [i for i in range(num_buttons) if i not in pivot_cols]
    
    # If no free variables, unique solution exists
    if not free_vars:
        solution = [0] * num_buttons
        for row_idx, col in enumerate(pivot_cols):
            solution[col] = matrix[row_idx][num_buttons]
        return sum(solution)
    
    # Multiple solutions exist - enumerate all combinations of free variables
    min_presses = float('inf')
    
    for mask in range(1 << len(free_vars)):
        solution = [0] * num_buttons
        
        # Set free variables according to current mask
        for i, var in enumerate(free_vars):
            solution[var] = (mask >> i) & 1
        
        # Solve for pivot variables using back substitution
        for row_idx, col in enumerate(pivot_cols):
            val = matrix[row_idx][num_buttons]
            for j in range(num_buttons):
                if j != col:
                    val ^= matrix[row_idx][j] * solution[j]
            solution[col] = val
        
        # Count total button presses
        min_presses = min(min_presses, sum(solution))
    
    return min_presses


def solve_machine(machine: Machine) -> int:
    """
    Solve a single machine for minimum button presses (Part 1).
    
    Args:
        machine: Machine object
    
    Returns:
        Minimum number of button presses needed
    """
    matrix = build_matrix(machine)
    matrix, pivot_cols = gaussian_elimination_gf2(matrix)
    return find_minimum_solution(matrix, pivot_cols)


def solve_part1(text: str) -> int:
    """
    Solve Part 1: Sum minimum presses across all machines.
    
    Args:
        text: Input text containing machine specifications
    
    Returns:
        Total minimum button presses for all machines
    """
    machines = parse_input(text)
    total_presses = 0
    
    for machine in machines:
        min_presses = solve_machine(machine)
        if min_presses != float('inf'):
            total_presses += min_presses
    
    return total_presses


# =======================================
# Part 2: Increment Counters (Integer LP)
# =======================================

def parse_machine_part2(line: str) -> Tuple[List[int], List[List[int]]]:
    """
    Parse a single machine specification line for Part 2.
    Extract joltage requirements instead of indicator diagram.
    
    Args:
        line: Input line with format: [diagram] (button1) ... (buttonN) {joltage}
    
    Returns:
        Tuple of (targets, buttons) where:
        - targets: List of joltage target values
        - buttons: List of button patterns
    """
    # Extract joltage requirements between { and }
    joltage_match = re.search(r'\{([0-9,]+)\}', line)
    joltage_str = joltage_match.group(1)
    targets = [int(x) for x in joltage_str.split(',')]
    
    # Extract button patterns
    button_matches = re.findall(r'\(([0-9,]+)\)', line)
    buttons = []
    for button_str in button_matches:
        indices = [int(x) for x in button_str.split(',')]
        buttons.append(indices)
    
    return targets, buttons


def build_matrix_part2(targets: List[int], buttons: List[List[int]]) -> List[List[int]]:
    """
    Build augmented matrix [A | b] for Part 2 integer linear programming.
    
    Args:
        targets: Target values for each counter
        buttons: List of button patterns
    
    Returns:
        Augmented matrix for solving Ax = b where x >= 0, x integer
    """
    num_counters = len(targets)
    num_buttons = len(buttons)
    
    matrix = []
    for counter_idx in range(num_counters):
        row = [0] * (num_buttons + 1)
        
        # Check which buttons increment this counter
        for button_idx, button in enumerate(buttons):
            if counter_idx in button:
                row[button_idx] = 1
        
        # Augment with target value
        row[num_buttons] = targets[counter_idx]
        matrix.append(row)
    
    return matrix


def solve_integer_linear_system(targets: List[int], buttons: List[List[int]]) -> int:
    """
    Solve the integer linear programming problem via Gaussian elimination
    and bounded search over free variables.
    
    Minimize sum(x) subject to Ax = b, x >= 0, x integer.
    
    Args:
        targets: Target counter values
        buttons: Button patterns
    
    Returns:
        Minimum total button presses, or float('inf') if unsolvable
    """
    num_counters = len(targets)
    num_buttons = len(buttons)
    
    # Special case: all targets are zero
    if all(t == 0 for t in targets):
        return 0
    
    # Build augmented matrix [A | b]
    matrix = []
    for counter_idx in range(num_counters):
        row = [0] * (num_buttons + 1)
        for button_idx, button in enumerate(buttons):
            if counter_idx in button:
                row[button_idx] = 1
        row[num_buttons] = targets[counter_idx]
        matrix.append(row)
    
    # Gaussian elimination (integer arithmetic)
    pivot_row = 0
    pivot_cols = []
    
    for col in range(num_buttons):
        # Find pivot in this column
        found_pivot = False
        for row in range(pivot_row, num_counters):
            if matrix[row][col] != 0:
                if row != pivot_row:
                    matrix[pivot_row], matrix[row] = matrix[row], matrix[pivot_row]
                found_pivot = True
                break
        
        if not found_pivot:
            continue  # Free variable
        
        pivot_cols.append(col)
        pivot_val = matrix[pivot_row][col]
        
        # Eliminate below this pivot
        for row in range(pivot_row + 1, num_counters):
            if matrix[row][col] != 0:
                factor = matrix[row][col]
                for c in range(num_buttons + 1):
                    matrix[row][c] = matrix[row][c] * pivot_val - matrix[pivot_row][c] * factor
        
        pivot_row += 1
    
    # Check for inconsistency
    for row_idx in range(pivot_row, num_counters):
        if all(matrix[row_idx][c] == 0 for c in range(num_buttons)) and matrix[row_idx][num_buttons] != 0:
            return float('inf')
    
    # Identify free variables
    free_vars = [i for i in range(num_buttons) if i not in pivot_cols]
    
    # If no free variables, try unique solution
    if not free_vars:
        solution = [0] * num_buttons
        
        for row_idx in range(len(pivot_cols) - 1, -1, -1):
            pivot_col = pivot_cols[row_idx]
            val = matrix[row_idx][num_buttons]
            
            for col in range(pivot_col + 1, num_buttons):
                val -= matrix[row_idx][col] * solution[col]
            
            if val % matrix[row_idx][pivot_col] != 0:
                return float('inf')
            
            solution[pivot_col] = val // matrix[row_idx][pivot_col]
            
            if solution[pivot_col] < 0:
                return float('inf')
        
        # Verify solution
        for counter_idx in range(num_counters):
            total = 0
            for button_idx, button in enumerate(buttons):
                if counter_idx in button:
                    total += solution[button_idx]
            if total != targets[counter_idx]:
                return float('inf')
        
        return sum(solution)
    
    # Underdetermined system - search over free variables
    min_presses = float('inf')
    sum_tgt = sum(targets)
    
    # Determine search bound based on number of free variables
    if len(free_vars) == 1:
        max_bound = sum_tgt
    elif len(free_vars) == 2:
        max_bound = min(sum_tgt, sum_tgt // 2 + 50)
    elif len(free_vars) == 3:
        max_bound = min(sum_tgt, max(100, sum_tgt // 3))
    else:
        max_bound = min(sum_tgt, max(50, sum_tgt // len(free_vars)))
    
    search_space_size = (max_bound + 1) ** len(free_vars)
    
    # Limit search space to avoid excessive computation
    if search_space_size > 1_000_000_000:
        return float('inf')
    
    # Enumerate all combinations of free variables
    for free_values in product(range(max_bound + 1), repeat=len(free_vars)):
        # Early termination optimization
        if min_presses != float('inf') and sum(free_values) >= min_presses:
            continue
        
        solution = [0] * num_buttons
        
        # Set free variables
        for i, var_idx in enumerate(free_vars):
            solution[var_idx] = free_values[i]
        
        # Back substitution for pivot variables
        valid = True
        for row_idx in range(len(pivot_cols) - 1, -1, -1):
            pivot_col = pivot_cols[row_idx]
            val = matrix[row_idx][num_buttons]
            
            for col in range(pivot_col + 1, num_buttons):
                val -= matrix[row_idx][col] * solution[col]
            
            if val % matrix[row_idx][pivot_col] != 0:
                valid = False
                break
            
            solution[pivot_col] = val // matrix[row_idx][pivot_col]
            
            if solution[pivot_col] < 0:
                valid = False
                break
        
        if not valid:
            continue
        
        # Verify solution
        result = [0] * num_counters
        for button_idx, count in enumerate(solution):
            for counter_idx in buttons[button_idx]:
                result[counter_idx] += count
        
        if result == targets:
            presses = sum(solution)
            min_presses = min(min_presses, presses)
    
    return min_presses


def solve_machine_part2(targets: List[int], buttons: List[List[int]]) -> int:
    """
    Solve a single machine for Part 2 (joltage counter configuration).
    
    Args:
        targets: Target joltage values for each counter
        buttons: Button patterns (which counters each button increments)
    
    Returns:
        Minimum number of button presses needed
    """
    return solve_integer_linear_system(targets, buttons)


def solve_part2(text: str) -> int:
    """
    Solve Part 2: Sum minimum presses for joltage counter configuration.
    
    Part 2 uses joltage requirements {..} instead of indicator diagrams [..].
    Buttons increment counters (addition) instead of toggling (XOR).
    
    Args:
        text: Input text containing machine specifications
    
    Returns:
        Total minimum button presses for all machines
    """
    total_presses = 0
    
    for line in text.strip().split('\n'):
        if not line:
            continue
        
        targets, buttons = parse_machine_part2(line)
        presses = solve_machine_part2(targets, buttons)
        
        if presses != float('inf'):
            total_presses += presses
    
    return total_presses


def main():
    """Main execution function."""
    with open('input.txt', 'r') as f:
        data = f.read()
    
    part1_result = solve_part1(data)
    print(f"Part 1: {part1_result}")
    
    part2_result = solve_part2(data)
    print(f"Part 2: {part2_result}")


if __name__ == '__main__':
    main()
