#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 07: Laboratories

Simulate a tachyon beam traveling through a manifold, splitting when it hits
splitters (^) and merging when multiple beams reach the same position.
Count the total number of splits.
"""

import sys
from pathlib import Path


def parse_input(input_text: str):
    """
    Parse the input text into a usable format.
    
    Returns a dictionary containing:
    - rows: number of rows in the grid
    - cols: number of columns in the grid
    - start_cols: set of starting column positions (where S is located)
    - splitters: set of (row, col) tuples for splitter positions
    - grid: list of strings representing the grid
    """
    lines = input_text.strip().split('\n')
    
    rows = len(lines)
    cols = len(lines[0]) if rows > 0 else 0
    
    start_cols = set()
    splitters = set()
    
    for row_idx, line in enumerate(lines):
        for col_idx, char in enumerate(line):
            if char == 'S':
                start_cols.add(col_idx)
            elif char == '^':
                splitters.add((row_idx, col_idx))
    
    return {
        'rows': rows,
        'cols': cols,
        'start_cols': start_cols,
        'splitters': splitters,
        'grid': lines
    }


def solve_part1(data) -> int:
    """
    Solve part 1 of the puzzle.
    
    Simulates the tachyon beam traveling through the manifold and counts
    the total number of times the beam splits when it encounters splitters.
    
    Algorithm:
    - Start with beams at all start column(s)
    - Process row by row
    - For each active beam that hits a splitter:
      - Increment split counter
      - Create two new beams at (col-1) and (col+1)
    - Beams at the same position automatically merge (using sets)
    - Beams outside grid bounds are filtered out
    """
    rows = data['rows']
    cols = data['cols']
    start_cols = data['start_cols']
    splitters = data['splitters']
    
    # Track active beam columns as a set (automatically handles merging)
    active_beams = start_cols.copy()
    split_count = 0
    
    # Process each row
    for row in range(rows):
        # Check which beams hit splitters in this row
        next_beams = set()
        
        for col in active_beams:
            if (row, col) in splitters:
                # Beam hits a splitter - increment counter and create two new beams
                split_count += 1
                
                # Add left and right beams (will be filtered for bounds)
                left_col = col - 1
                right_col = col + 1
                
                if 0 <= left_col < cols:
                    next_beams.add(left_col)
                if 0 <= right_col < cols:
                    next_beams.add(right_col)
            else:
                # Beam continues straight down to next row
                next_beams.add(col)
        
        # Update active beams for next row
        active_beams = next_beams
    
    return split_count


def solve_part2(data) -> int:
    """
    Solve part 2 of the puzzle.
    
    Count unique quantum timelines through the splitter network.
    Unlike Part 1, timelines NEVER merge even if they reach the same position.
    Each unique path through the network counts as a separate timeline.
    
    Algorithm:
    - Use recursive path counting with memoization
    - From each position, count all possible paths to the exit
    - Timelines split when hitting a splitter (left and right paths)
    - Timelines continue straight when in empty space
    - Out-of-bounds timelines still count
    """
    rows = data['rows']
    cols = data['cols']
    start_cols = data['start_cols']
    splitters = data['splitters']
    
    # Memoization cache for counting timelines from each position
    memo = {}
    
    def count_timelines(row, col):
        """
        Count the number of unique timelines starting from position (row, col).
        
        Returns the number of distinct paths from this position to exiting the grid.
        """
        # Base case: exited the grid bottom
        if row >= rows:
            return 1  # One complete timeline
        
        # Check memoization cache
        if (row, col) in memo:
            return memo[(row, col)]
        
        # Recursive case
        if (row, col) in splitters:
            # Hit a splitter: timeline splits into left and right paths
            left_count = count_timelines(row + 1, col - 1)
            right_count = count_timelines(row + 1, col + 1)
            result = left_count + right_count
        else:
            # Empty space: continue straight down
            result = count_timelines(row + 1, col)
        
        # Store in cache
        memo[(row, col)] = result
        return result
    
    # Sum timelines from all starting positions
    total_timelines = 0
    for start_col in start_cols:
        # Start at row 0 (or row 1 if we need to skip the start row)
        # Based on Part 1, it seems we start processing from row 0
        total_timelines += count_timelines(0, start_col)
    
    return total_timelines


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
