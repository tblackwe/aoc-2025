#!/usr/bin/env python3
"""
Advent of Code 2025 - Day XX: [Problem Title]

[Brief description of the puzzle]
"""

import sys
from pathlib import Path


def parse_input(input_text: str):
    """
    Parse the input text into a usable format.

    [Describe input format]
    """
    lines = input_text.strip().split('\n')
    # TODO: implement parsing
    pass


def solve_part1(data) -> int:
    """
    Solve part 1 of the puzzle.

    [Describe what part 1 computes]
    """
    # TODO: implement part 1
    pass


def solve_part2(data) -> int | None:
    """
    Solve part 2 of the puzzle.

    [Describe what part 2 computes]
    """
    # TODO: implement part 2
    return None


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
