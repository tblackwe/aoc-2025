#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 04: Printing Department

Count how many paper rolls are accessible to a forklift.
A roll is accessible if it has fewer than 4 neighboring rolls.
"""

import sys
from pathlib import Path


def parse_input(input_text: str):
    """
    Parse the input text into a 2D grid.

    Returns a list of lists where each cell contains '.' or '@'
    """
    lines = input_text.strip().split('\n')
    return [list(line) for line in lines]


def count_neighbors(grid, row, col):
    """
    Count the number of rolls (@) adjacent to position (row, col).
    
    Checks all 8 directions: up, down, left, right, and 4 diagonals.
    """
    # Define 8 direction vectors
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # top-left, top, top-right
        (0, -1),           (0, 1),    # left, right
        (1, -1),  (1, 0),  (1, 1)     # bottom-left, bottom, bottom-right
    ]
    
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    count = 0
    
    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc
        
        # Check if position is within bounds
        if 0 <= new_row < rows and 0 <= new_col < cols:
            if grid[new_row][new_col] == '@':
                count += 1
    
    return count


def solve_part1(data) -> int:
    """
    Count the number of accessible rolls.
    
    A roll is accessible if it has fewer than 4 neighboring rolls.
    """
    if not data or not data[0]:
        return 0
    
    rows = len(data)
    cols = len(data[0])
    accessible_count = 0
    
    # Check each position in the grid
    for row in range(rows):
        for col in range(cols):
            # If this position has a roll
            if data[row][col] == '@':
                # Count its neighbors
                neighbor_count = count_neighbors(data, row, col)
                # If fewer than 4 neighbors, it's accessible
                if neighbor_count < 4:
                    accessible_count += 1
    
    return accessible_count


def solve_part2(data) -> int | None:
    """
    Solve part 2 of the puzzle.

    Iteratively remove accessible rolls (those with < 4 neighbors) until none remain.
    Count the total number of rolls removed.
    """
    # Create a mutable copy of the grid
    grid = [row[:] for row in data]
    total_removed = 0
    
    while True:
        # Find all accessible rolls in this iteration
        accessible_positions = []
        rows = len(grid)
        cols = len(grid[0]) if rows > 0 else 0
        
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == '@':
                    neighbor_count = count_neighbors(grid, row, col)
                    if neighbor_count < 4:
                        accessible_positions.append((row, col))
        
        # If no accessible rolls found, we're done
        if not accessible_positions:
            break
        
        # Remove all accessible rolls
        for row, col in accessible_positions:
            grid[row][col] = '.'
        
        total_removed += len(accessible_positions)
    
    return total_removed


def main():
    """Run the solution."""
    input_file = Path(__file__).parent / 'input.txt'
    data = parse_input(input_file.read_text())

    print(f"Part 1: {solve_part1(data)}")

    if (part2 := solve_part2(data)) is not None:
        print(f"Part 2: {part2}")


def test():
    """
    Run tests based on spec test cases.

    Tests should match the Test Cases section in the spec file.
    """
    # === Part 1 Tests ===
    print("Part 1 Tests:")

    # Main example from spec
    example = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@."""
    assert solve_part1(parse_input(example)) == 13
    print("  ✓ Main example (expected 13 accessible rolls)")

    # === Part 2 Tests ===
    print("\nPart 2 Tests:")
    
    # Main example from spec - should remove 43 total rolls
    assert solve_part2(parse_input(example)) == 43
    print("  ✓ Main example (expected 43 total rolls removed)")

    print("\n✅ All tests passed!")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test()
    else:
        main()
