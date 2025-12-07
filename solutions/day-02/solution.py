#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 02: Gift Shop

Find invalid product codes (IDs made of a digit sequence repeated twice).
"""

import sys
from pathlib import Path


def parse_input(input_text: str) -> list[tuple[int, int]]:
    """
    Parse comma-separated ranges into (start, end) tuples.

    Input format: "11-22,95-115,998-1012,..."
    Handles newlines within the input.
    """
    # Remove newlines and split by comma
    text = input_text.replace('\n', '').strip()
    ranges = []
    for part in text.split(','):
        part = part.strip()
        if part and '-' in part:
            start, end = part.split('-')
            ranges.append((int(start), int(end)))
    return ranges


def is_invalid_code(n: int) -> bool:
    """
    Check if a number is an invalid product code.
    
    Invalid = the digits form a sequence repeated exactly twice.
    E.g., 11 (1 repeated), 1212 (12 repeated), 123123 (123 repeated)
    """
    s = str(n)
    length = len(s)
    
    # Must have even length to be a repeated sequence
    if length % 2 != 0:
        return False
    
    half = length // 2
    return s[:half] == s[half:]


def solve_part1(ranges: list[tuple[int, int]]) -> int:
    """
    Sum all invalid product codes across all ranges.
    
    Invalid = ID made of some digit sequence repeated twice.
    """
    total = 0
    
    for start, end in ranges:
        for n in range(start, end + 1):
            if is_invalid_code(n):
                total += n
    
    return total


def is_invalid_code_part2(n: int) -> bool:
    """
    Check if a number is invalid for Part 2.

    Invalid = the entire number is made of some pattern repeated 2+ times.

    Part 1: pattern repeated exactly twice (11, 1212, 123123)
    Part 2: pattern repeated 2 or more times (111=1x3, 565656=56x3, 824824824=824x3)

    Examples:
    - 11: "1" repeated 2x → invalid
    - 111: "1" repeated 3x → invalid
    - 1212: "12" repeated 2x → invalid
    - 565656: "56" repeated 3x → invalid
    - 824824824: "824" repeated 3x → invalid
    """
    s = str(n)
    length = len(s)

    # Check if string is made of a pattern repeated 2+ times
    for pattern_len in range(1, length // 2 + 1):
        if length % pattern_len == 0:
            pattern = s[:pattern_len]
            repetitions = length // pattern_len
            if repetitions >= 2 and pattern * repetitions == s:
                return True

    return False


def solve_part2(ranges: list[tuple[int, int]]) -> int | None:
    """
    Sum all invalid product codes (Part 2 definition).

    Invalid = any ID containing a 2+ digit sequence that appears twice.
    """
    total = 0

    for start, end in ranges:
        for n in range(start, end + 1):
            if is_invalid_code_part2(n):
                total += n

    return total


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

    # Main example from spec
    example = """11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124"""
    assert solve_part1(parse_input(example)) == 1227775554
    print("  ✓ Main example: 1227775554")

    # Edge cases from spec
    assert solve_part1(parse_input("11-11")) == 11
    print("  ✓ 11-11: Smallest invalid code")

    assert solve_part1(parse_input("10-12")) == 11
    print("  ✓ 10-12: Range containing one invalid")

    assert solve_part1(parse_input("12-15")) == 0
    print("  ✓ 12-15: Range with no invalid codes")

    assert solve_part1(parse_input("99-99")) == 99
    print("  ✓ 99-99: Single digit repeated twice")

    assert solve_part1(parse_input("1212-1212")) == 1212
    print("  ✓ 1212-1212: 2-digit pattern repeated")

    assert solve_part1(parse_input("111-111")) == 0
    print("  ✓ 111-111: Odd length - NOT invalid for Part 1")

    assert solve_part1(parse_input("121212-121212")) == 0
    print("  ✓ 121212-121212: 121≠212, not two equal halves")

    # === Part 2 Tests ===
    print("\nPart 2 Tests:")

    # Main example from spec
    assert solve_part2(parse_input(example)) == 4174379265
    print("  ✓ Main example: 4174379265")

    # Edge cases from spec
    assert solve_part2(parse_input("11-11")) == 11
    print("  ✓ 11-11: Same as Part 1")

    assert solve_part2(parse_input("111-111")) == 111
    print("  ✓ 111-111: NEW - 1 repeated 3x")

    assert solve_part2(parse_input("999-999")) == 999
    print("  ✓ 999-999: NEW - 9 repeated 3x")

    assert solve_part2(parse_input("121212-121212")) == 121212
    print("  ✓ 121212-121212: NEW - 12 repeated 3x")

    assert solve_part2(parse_input("1000-1000")) == 0
    print("  ✓ 1000-1000: Has '00' but not full repetition")

    assert solve_part2(parse_input("100100-100100")) == 100100
    print("  ✓ 100100-100100: Pattern with leading zeros works")

    print("\n✅ All tests passed!")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test()
    else:
        main()

