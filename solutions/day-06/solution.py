#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 06: Trash Compactor

Parse vertical column math problems and calculate grand total.
"""

import sys
from pathlib import Path
from typing import List, Tuple, Optional


def parse_input(input_text: str) -> List[str]:
    """
    Parse the input text into lines, preserving spacing.
    
    Returns a list of lines with internal spacing preserved.
    Strips only the trailing newline from the entire input, not from individual lines.
    """
    lines = input_text.strip('\n').split('\n')
    return lines


def find_operators(operator_row: str) -> List[Tuple[int, str]]:
    """
    Find all operators and their positions in the operator row.
    
    Returns a list of (position, operator) tuples.
    """
    operators = []
    for i, char in enumerate(operator_row):
        if char in ['+', '*']:
            operators.append((i, char))
    return operators


def extract_number_at_position(row: str, pos: int) -> Optional[int]:
    """
    Extract a number in the column indicated by the operator position.
    
    The operator position marks the leftmost position of the widest number
    in that column. Numbers can be right-aligned, so we need to scan right
    from the operator position to find where numbers actually are in each row.
    
    Strategy:
    1. Starting from operator position, look right to find a digit
    2. Extract the complete number once a digit is found
    3. Don't look too far right (max ~5 positions) to avoid jumping to next column
    """
    # Handle position out of bounds
    if pos >= len(row):
        return None
    
    # Scan from operator position rightward to find a number in this column
    # We scan right because numbers are right-aligned
    max_scan = min(len(row), pos + 6)  # Don't scan too far (next column might start)
    
    for scan_pos in range(pos, max_scan):
        if scan_pos < len(row) and row[scan_pos].isdigit():
            # Found a digit! Extract the full number
            start = scan_pos
            while start > 0 and row[start - 1].isdigit():
                start -= 1
            
            end = scan_pos
            while end + 1 < len(row) and row[end + 1].isdigit():
                end += 1
            
            # Make sure this number starts at or after the operator position
            # (it's in this column, not the previous one)
            if start >= pos:
                number_str = row[start:end + 1]
                return int(number_str)
            # If the number starts before pos but extends into it, take it too
            elif start < pos <= end:
                number_str = row[start:end + 1]
                return int(number_str)
    
    return None


def extract_column_numbers(number_rows: List[str], op_pos: int) -> List[int]:
    """
    Extract all numbers in a column identified by operator position.
    
    Returns a list of integers found in that column.
    """
    numbers = []
    for row in number_rows:
        num = extract_number_at_position(row, op_pos)
        if num is not None:
            numbers.append(num)
    return numbers


def calculate_result(numbers: List[int], operator: str) -> int:
    """
    Apply operator to all numbers in column.
    
    For '*': multiply all numbers together
    For '+': add all numbers together
    """
    if operator == '*':
        result = 1
        for num in numbers:
            result *= num
        return result
    else:  # operator == '+'
        return sum(numbers)


def solve_part1(input_text: str) -> int:
    """
    Solve part 1 of the puzzle.
    
    Parse vertical column math problems and return grand total.
    """
    lines = parse_input(input_text)
    
    if not lines or len(lines) < 1:
        return 0
    
    # Separate number rows from operator row
    number_rows = lines[:-1]
    operator_row = lines[-1]
    
    # Find all operators and positions
    operators = find_operators(operator_row)
    
    # Process each column
    grand_total = 0
    for pos, op in operators:
        numbers = extract_column_numbers(number_rows, pos)
        if numbers:  # Only calculate if we found numbers
            result = calculate_result(numbers, op)
            grand_total += result
    
    return grand_total


def extract_vertical_problem(lines: List[str], col_pos: int) -> Optional[Tuple[int, str]]:
    """
    Extract a number and operator by reading vertically at a column position.
    
    Read through ALL rows at the given column position (including operator row),
    collecting digits to form a number, and identifying the operator.
    
    Args:
        lines: All input lines (including operator row)
        col_pos: Column position to read
    
    Returns:
        Tuple of (number, operator) or None if no valid problem at this position
    
    Example:
        Col 0:
          Row 0: '1'
          Row 1: '3'
          Row 2: '5'
          Row 3: '+'
        Result: (135, '+')
    """
    digits = []
    operator = None
    
    for row in lines:
        if col_pos < len(row):
            char = row[col_pos]
            if char.isdigit():
                digits.append(char)
            elif char in ['+', '*']:
                operator = char
            # Skip spaces
    
    if not digits or operator is None:
        return None
    
    number = int(''.join(digits))
    return (number, operator)


def parse_problems_part2(lines: List[str]) -> List[Tuple[List[int], str]]:
    """
    Parse problems reading vertically (top-to-bottom) and processing right-to-left.
    
    For Part 2:
    1. Each character column is read top-to-bottom to form a number
    2. Reading RIGHT-TO-LEFT, collect numbers until we hit an operator
    3. That operator applies to all collected numbers
    4. Continue processing right-to-left
    
    Args:
        lines: Parsed input lines (including operator row)
    
    Returns:
        List of (numbers, operator) tuples in the order they're encountered (right-to-left)
    
    Example:
        Input:
            123 328  51 64 
             45 64  387 23 
              6 98  215 314
            *   +   *   +  
        
        Reading right-to-left:
        - Col 14: number 4
        - Col 13: number 431
        - Col 12: number 623, operator + → problem: [4, 431, 623] with +
        - Col 10: number 175
        - Col 9: number 581
        - Col 8: number 32, operator * → problem: [175, 581, 32] with *
        - etc.
    """
    if not lines or len(lines) < 1:
        return []
    
    # Find maximum line length to determine rightmost column
    max_len = max(len(line) for line in lines)
    
    # Read columns from right to left, collecting numbers until we hit an operator
    problems = []
    current_numbers = []
    
    for col in range(max_len - 1, -1, -1):
        problem = extract_vertical_problem(lines, col)
        if problem is not None:
            number, operator = problem
            # This column has both a number and an operator
            # Add the number to current collection, then create problem
            current_numbers.append(number)
            problems.append((current_numbers.copy(), operator))
            current_numbers = []
        else:
            # Check if this column has just a number (no operator)
            digits = []
            for row in lines:
                if col < len(row) and row[col].isdigit():
                    digits.append(row[col])
            if digits:
                number = int(''.join(digits))
                current_numbers.append(number)
    
    return problems


def solve_part2(input_text: str) -> Optional[int]:
    """
    Solve part 2 of the puzzle.
    
    Part 2 changes:
    - Each character column is read VERTICALLY (top-to-bottom)
    - Reading RIGHT-TO-LEFT, collect numbers until hitting an operator
    - The operator applies to all collected numbers
    - Continue processing right-to-left
    
    Example:
        123 328  51 64 
         45 64  387 23 
          6 98  215 314
        *   +   *   +  
    
    Reading right-to-left:
    - Position 14: number 4
    - Position 13: number 431
    - Position 12: number 623 with operator + → problem: [4, 431, 623] with +
    - etc.
    """
    lines = parse_input(input_text)
    
    if not lines or len(lines) < 1:
        return 0
    
    # Parse problems with vertical reading and right-to-left processing
    problems = parse_problems_part2(lines)
    
    # Calculate result for each problem and sum
    grand_total = 0
    for numbers, operator in problems:
        result = calculate_result(numbers, operator)
        grand_total += result
    
    return grand_total


def main():
    """Run the solution."""
    input_file = Path(__file__).parent / 'input.txt'
    
    if not input_file.exists():
        print("Error: input.txt not found")
        return
    
    input_text = input_file.read_text()

    print(f"Part 1: {solve_part1(input_text)}")

    part2_result = solve_part2(input_text)
    if part2_result is not None:
        print(f"Part 2: {part2_result}")


def test():
    """
    Run tests based on spec test cases.

    Tests should match the Test Cases section in the spec file.
    """
    # === Part 1 Tests ===
    print("Part 1 Tests:")

    # Main example from spec
    example = """[paste example input here]"""
    assert solve_part1(parse_input(example)) == 0  # TODO: expected value
    print("  ✓ Main example")

    # TODO: Add more test cases from spec
    # assert solve_part1(parse_input("[input]")) == [expected]
    # print("  ✓ [test description]")

    # === Part 2 Tests ===
    print("\nPart 2 Tests:")

    # Main example
    assert solve_part2(parse_input(example)) == 0  # TODO: expected value
    print("  ✓ Main example")

    # TODO: Add more test cases from spec

    print("\n✅ All tests passed!")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test()
    else:
        main()
