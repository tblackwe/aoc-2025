#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 04: Printing Department

Count how many paper rolls are accessible to a forklift.
A roll is accessible if it has fewer than 4 neighboring rolls.

Performance optimizations:
- Uses set-based data structure instead of 2D grid for O(1) lookups
- Only iterates over existing rolls, not empty spaces
- Caches neighbor counts in Part 2 to avoid redundant calculations
- Only re-checks rolls that could have changed (neighbors of removed rolls)
"""

import sys
from pathlib import Path
from typing import Set, Tuple

# Type alias for clarity
Position = Tuple[int, int]
GridData = Tuple[Set[Position], int, int]

# Pre-define 8 direction vectors for neighbor checking
DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),  # top-left, top, top-right
    (0, -1),           (0, 1),    # left, right
    (1, -1),  (1, 0),  (1, 1)     # bottom-left, bottom, bottom-right
]


def parse_input(input_text: str) -> GridData:
    """
    Parse the input text into a set of roll positions.
    
    Optimized parsing that creates a set for O(1) lookup operations.
    
    Args:
        input_text: Raw input string with '@' for rolls and '.' for empty spaces
    
    Returns:
        tuple: (set of (row, col) positions with rolls, max_row, max_col)
    """
    lines = input_text.strip().split('\n')
    rolls: Set[Position] = set()
    
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == '@':
                rolls.add((row, col))
    
    max_row = len(lines) - 1
    max_col = len(lines[0]) - 1 if lines else 0
    
    return rolls, max_row, max_col


def count_neighbors_set(rolls: Set[Position], row: int, col: int, 
                        max_row: int, max_col: int) -> int:
    """
    Count the number of rolls adjacent to position (row, col).
    
    Uses set-based lookup for O(1) neighbor checking instead of grid indexing.
    
    Args:
        rolls: set of (row, col) positions containing rolls
        row: row position to check
        col: column position to check
        max_row: maximum valid row index
        max_col: maximum valid column index
    
    Returns:
        int: number of neighboring rolls (0-8)
    """
    count = 0
    
    for dr, dc in DIRECTIONS:
        new_row = row + dr
        new_col = col + dc
        
        # Check if position is within bounds and has a roll
        if 0 <= new_row <= max_row and 0 <= new_col <= max_col:
            if (new_row, new_col) in rolls:
                count += 1
    
    return count


def solve_part1(data: GridData) -> int:
    """
    Count the number of accessible rolls.
    
    A roll is accessible if it has fewer than 4 neighboring rolls.
    
    Time Complexity: O(N) where N is the number of rolls
    Space Complexity: O(1) additional space
    
    Args:
        data: tuple of (rolls set, max_row, max_col) from parse_input
    
    Returns:
        int: count of accessible rolls
    """
    rolls, max_row, max_col = data
    
    if not rolls:
        return 0
    
    accessible_count = 0
    
    # Check only positions that have rolls (not entire grid)
    for row, col in rolls:
        neighbor_count = count_neighbors_set(rolls, row, col, max_row, max_col)
        if neighbor_count < 4:
            accessible_count += 1
    
    return accessible_count


def solve_part2(data: GridData) -> int | None:
    """
    Iteratively remove accessible rolls until none remain.
    
    Optimized approach:
    - Uses set of roll positions instead of full grid scanning
    - Pre-computes neighbor counts for all rolls
    - Only updates neighbor counts for affected rolls (neighbors of removed rolls)
    - Maintains a set of potentially accessible rolls to check each iteration
    
    This avoids re-checking rolls that couldn't have changed, dramatically
    reducing the number of neighbor count calculations needed.
    
    Time Complexity: O(N + E) where N is rolls, E is edges between neighbors
    Space Complexity: O(N) for storing rolls and neighbor counts
    
    Args:
        data: tuple of (rolls set, max_row, max_col) from parse_input
    
    Returns:
        int: total number of rolls removed
    """
    rolls, max_row, max_col = data
    
    # Work with a mutable copy of the rolls set
    rolls = set(rolls)
    total_removed = 0
    
    # Pre-compute neighbor counts for all rolls - O(N) operation
    neighbor_counts = {}
    for row, col in rolls:
        neighbor_counts[(row, col)] = count_neighbors_set(rolls, row, col, max_row, max_col)
    
    # Initially, all rolls with < 4 neighbors are candidates for removal
    candidates = {pos for pos, count in neighbor_counts.items() if count < 4}
    
    while candidates:
        # All current candidates are accessible and will be removed
        accessible_positions = list(candidates)
        
        # Remove all accessible rolls
        for pos in accessible_positions:
            rolls.discard(pos)
            del neighbor_counts[pos]
        
        total_removed += len(accessible_positions)
        
        # Find neighbors of removed rolls that need their counts updated
        # This is the key optimization: only check neighbors of removed rolls
        affected_neighbors = set()
        for row, col in accessible_positions:
            for dr, dc in DIRECTIONS:
                new_row, new_col = row + dr, col + dc
                neighbor_pos = (new_row, new_col)
                
                # Only process if it's still a roll (not removed)
                if neighbor_pos in rolls:
                    affected_neighbors.add(neighbor_pos)
        
        # Update neighbor counts only for affected rolls and rebuild candidates
        candidates = set()
        for pos in affected_neighbors:
            row, col = pos
            new_count = count_neighbors_set(rolls, row, col, max_row, max_col)
            neighbor_counts[pos] = new_count
            
            if new_count < 4:
                candidates.add(pos)
    
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
