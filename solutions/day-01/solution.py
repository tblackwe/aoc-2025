#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 01: Secret Entrance

A safe dial puzzle where we track how many times the dial points to 0.
"""

import sys
from pathlib import Path


def parse_input(input_text: str) -> list[tuple[str, int]]:
    """
    Parse instructions into (direction, amount) tuples.

    Each line is L or R followed by a number (e.g., "L68", "R48").
    """
    instructions = []
    for line in input_text.strip().split('\n'):
        line = line.strip()
        if line:
            instructions.append((line[0], int(line[1:])))
    return instructions


def solve_part1(instructions: list[tuple[str, int]]) -> int:
    """
    Count how many times the dial points to 0.

    Rules:
    - Dial starts at 50
    - L = rotate left (subtract), R = rotate right (add)
    - Dial wraps: 0-99 (modulo 100)
    - Count each time dial lands on 0 after a rotation
    """
    position = 50
    zero_count = 0

    for direction, amount in instructions:
        if direction == 'L':
            position = (position - amount) % 100
        else:
            position = (position + amount) % 100

        if position == 0:
            zero_count += 1

    return zero_count


def solve_part2(instructions: list[tuple[str, int]]) -> int:
    """
    Count how many times the dial points to 0 DURING rotations (not just landing).

    For each rotation, count how many times we pass through or land on 0.
    E.g., R1000 from position 50 would hit 0 ten times (at 100, 200, ... 1000 clicks).

    Key: we count arrivals at 0, not departures. If starting at 0, we don't count
    the initial position - only if we return to 0 during the rotation.
    """
    position = 50
    zero_count = 0

    for direction, amount in instructions:
        if direction == 'L':
            new_position = (position - amount) % 100

            # Moving left from P by A steps: we hit 0 at step P, P+100, P+200, etc.
            # But if P=0, first hit is at step 100, not 0 (we start there, don't count it)
            steps_to_first_zero = position if position > 0 else 100

            if amount >= steps_to_first_zero:
                zero_count += 1 + (amount - steps_to_first_zero) // 100

            position = new_position
        else:
            new_position = (position + amount) % 100

            # Moving right from P by A steps: we hit 0 at step (100-P), (200-P), etc.
            # If P=0, first hit is at step 100 (full rotation)
            steps_to_first_zero = (100 - position) % 100
            if steps_to_first_zero == 0:
                steps_to_first_zero = 100

            if amount >= steps_to_first_zero:
                zero_count += 1 + (amount - steps_to_first_zero) // 100

            position = new_position

    return zero_count


def main():
    """Run the solution."""
    input_file = Path(__file__).parent / 'input.txt'
    data = parse_input(input_file.read_text())

    print(f"Part 1: {solve_part1(data)}")

    if (part2 := solve_part2(data)) is not None:
        print(f"Part 2: {part2}")


def test():
    """Run tests based on spec test cases."""

    # === Part 1 Tests ===
    print("Part 1 Tests:")

    # Main example
    example = "L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82"
    assert solve_part1(parse_input(example)) == 3
    print("  ✓ Main example: 3")

    # Single move landing exactly on 0
    assert solve_part1(parse_input("R50")) == 1
    print("  ✓ R50: 1 (lands exactly on 0)")

    # Single move left landing exactly on 0
    assert solve_part1(parse_input("L50")) == 1
    print("  ✓ L50: 1 (lands exactly on 0)")

    # Single move, doesn't reach 0
    assert solve_part1(parse_input("R49")) == 0
    print("  ✓ R49: 0 (doesn't reach 0)")

    # Single move left, doesn't reach 0
    assert solve_part1(parse_input("L49")) == 0
    print("  ✓ L49: 0 (doesn't reach 0)")

    # Two moves, both land on 0 (R50: 50→0, then L100: 0→0)
    assert solve_part1(parse_input("R50\nL100")) == 2
    print("  ✓ R50,L100: 2 (both land on 0)")

    # === Step-by-step trace validation ===
    print("\nStep-by-step trace:")
    data = parse_input(example)
    expected = [82, 52, 0, 95, 55, 0, 99, 0, 14, 32]
    position = 50
    for i, (direction, amount) in enumerate(data):
        position = (position - amount) % 100 if direction == 'L' else (position + amount) % 100
        assert position == expected[i], f"Step {i+1}: expected {expected[i]}, got {position}"
    print("  ✓ All intermediate positions verified")

    # === Part 2 Tests ===
    print("\nPart 2 Tests:")

    # Main example: 3 landings + 3 pass-throughs
    assert solve_part2(parse_input(example)) == 6
    print("  ✓ Main example: 6 (3 landings + 3 pass-throughs)")

    # Large rotation from 50, passes 0 ten times
    assert solve_part2(parse_input("R1000")) == 10
    print("  ✓ R1000: 10 (large rotation)")

    # Lands exactly on 0, counts once
    assert solve_part2(parse_input("R50")) == 1
    print("  ✓ R50: 1 (lands exactly on 0)")

    # Passes 0 at step 50 and 150
    assert solve_part2(parse_input("R150")) == 2
    print("  ✓ R150: 2 (passes 0 twice)")

    # First lands on 0, second passes through 0 once
    assert solve_part2(parse_input("L50\nR100")) == 2
    print("  ✓ L50,R100: 2 (land + pass-through)")

    print("\n✅ All tests passed!")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test()
    else:
        main()

