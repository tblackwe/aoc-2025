#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 03: Lobby

Find the maximum voltage from each battery bank by selecting two batteries
where the first (10s digit) comes before the second (1s digit).
"""

import sys
from pathlib import Path


def parse_input(input_text: str) -> list[str]:
    """
    Parse the input text into a list of battery bank strings.

    Each line represents a bank of batteries where each character is a digit (voltage).
    """
    lines = input_text.strip().split('\n')
    return [line.strip() for line in lines if line.strip()]


def get_max_voltage(bank: str) -> int:
    """
    Find the maximum voltage for a single battery bank.

    Select two batteries at positions i < j to maximize 10*digit[i] + digit[j].
    The first battery becomes the 10s digit, the second becomes the 1s digit.
    """
    max_voltage = 0
    n = len(bank)

    # For each position i (10s digit), find max digit at any position j > i (1s digit)
    for i in range(n - 1):
        tens_digit = int(bank[i])
        # Find max digit after position i
        max_ones_digit = max(int(bank[j]) for j in range(i + 1, n))
        voltage = tens_digit * 10 + max_ones_digit
        max_voltage = max(max_voltage, voltage)

    return max_voltage


def solve_part1(banks: list[str]) -> int:
    """
    Solve part 1 of the puzzle.

    For each battery bank, find the largest voltage possible by selecting
    two batteries (10s digit at position i, 1s digit at position j > i).
    Sum all the voltages.
    """
    return sum(get_max_voltage(bank) for bank in banks)


def get_max_joltage_12_digits(bank: str) -> int:
    """
    Find the maximum 12-digit joltage for a single battery bank.

    Select 12 batteries at positions i1 < i2 < ... < i12 to maximize the
    resulting 12-digit number. Uses greedy algorithm: for each digit position,
    pick the largest available digit while ensuring enough positions remain.
    """
    n = len(bank)
    num_digits = 12

    if n < num_digits:
        # Not enough batteries - use all of them (edge case)
        return int(bank)

    result = []
    current_pos = 0

    for digit_idx in range(num_digits):
        digits_remaining = num_digits - digit_idx
        # Can pick from current_pos up to (n - digits_remaining) inclusive
        max_start_pos = n - digits_remaining

        # Find the maximum digit in the valid range
        best_digit = '0'
        best_pos = current_pos
        for pos in range(current_pos, max_start_pos + 1):
            if bank[pos] > best_digit:
                best_digit = bank[pos]
                best_pos = pos

        result.append(best_digit)
        current_pos = best_pos + 1

    return int(''.join(result))


def solve_part2(banks: list[str]) -> int:
    """
    Solve part 2 of the puzzle.

    For each battery bank, find the largest 12-digit joltage possible by
    selecting 12 batteries where positions must be in increasing order.
    Sum all the joltages.
    """
    return sum(get_max_joltage_12_digits(bank) for bank in banks)


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
    example = """987654321111111
811111111111119
234234234234278
818181911112111"""
    assert solve_part1(parse_input(example)) == 357
    print("  ✓ Main example: 357")

    # Individual bank tests (trace validation)
    assert get_max_voltage("987654321111111") == 98
    print("  ✓ Bank 1: 98 (9 at pos 0, 8 at pos 1)")

    assert get_max_voltage("811111111111119") == 89
    print("  ✓ Bank 2: 89 (8 at pos 0, 9 at pos 15)")

    assert get_max_voltage("234234234234278") == 78
    print("  ✓ Bank 3: 78 (7 at pos 13, 8 at pos 14)")

    assert get_max_voltage("818181911112111") == 92
    print("  ✓ Bank 4: 92 (9 at pos 6, 2 at pos 11)")

    # Edge case: single two-digit bank
    assert get_max_voltage("12") == 12
    print("  ✓ Simple bank '12': 12")

    assert get_max_voltage("21") == 21
    print("  ✓ Simple bank '21': 21")

    # Edge case: all same digits
    assert get_max_voltage("5555") == 55
    print("  ✓ All same digits '5555': 55")

    # Edge case: ascending order
    assert get_max_voltage("123456789") == 89
    print("  ✓ Ascending '123456789': 89 (8 at pos 7, 9 at pos 8)")

    # Edge case: descending order
    assert get_max_voltage("987654321") == 98
    print("  ✓ Descending '987654321': 98 (9 at pos 0, 8 at pos 1)")

    # Edge case: max at end, need to find best pair
    assert get_max_voltage("1119") == 19
    print("  ✓ '1119': 19 (1 at pos 0-2, 9 at pos 3)")

    # Edge case: zeros
    assert get_max_voltage("00") == 0
    print("  ✓ All zeros '00': 0")

    assert get_max_voltage("09") == 9
    print("  ✓ '09': 9 (0*10 + 9)")

    assert get_max_voltage("90") == 90
    print("  ✓ '90': 90 (9*10 + 0)")

    print("\n✅ All Part 1 tests passed!")

    # === Part 2 Tests ===
    print("\nPart 2 Tests:")

    # Main example from spec
    assert solve_part2(parse_input(example)) == 3121910778619
    print("  ✓ Main example: 3121910778619")

    # Individual bank tests (trace validation)
    assert get_max_joltage_12_digits("987654321111111") == 987654321111
    print("  ✓ Bank 1: 987654321111 (first 12 digits, skip 1s at end)")

    assert get_max_joltage_12_digits("811111111111119") == 811111111119
    print("  ✓ Bank 2: 811111111119 (include 9 at end)")

    assert get_max_joltage_12_digits("234234234234278") == 434234234278
    print("  ✓ Bank 3: 434234234278 (skip 2,3,2 at start)")

    assert get_max_joltage_12_digits("818181911112111") == 888911112111
    print("  ✓ Bank 4: 888911112111 (skip 1s near front)")

    # Edge case: exactly 12 digits
    assert get_max_joltage_12_digits("123456789012") == 123456789012
    print("  ✓ Exactly 12 digits: 123456789012 (no choice)")

    # Edge case: 13 digits, one to skip
    assert get_max_joltage_12_digits("1234567890123") == 234567890123
    print("  ✓ 13 digits '1234567890123': 234567890123 (skip the 1)")

    # Edge case: all same digits
    assert get_max_joltage_12_digits("555555555555555") == 555555555555
    print("  ✓ All same digits: 555555555555")

    # Edge case: descending with extras
    assert get_max_joltage_12_digits("9876543210000") == 987654321000
    print("  ✓ Descending with zeros: 987654321000")

    # Edge case: fewer than 12 digits (use all)
    assert get_max_joltage_12_digits("12345") == 12345
    print("  ✓ Less than 12 digits '12345': 12345 (use all)")

    print("\n✅ All Part 2 tests passed!")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test()
    else:
        main()

