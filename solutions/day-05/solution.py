#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 5: Cafeteria
Determine which available ingredient IDs are "fresh" based on inclusive ID ranges.

Algorithm: Range Checking (Approach 2)
- For each available ID, check if it falls within any fresh range
- Ranges are inclusive (both start and end are included)
- Time Complexity: O(N × R) where N = available IDs, R = number of ranges
- Space Complexity: O(R) for storing ranges
"""

from typing import List, Tuple


def parse_input(text: str) -> Tuple[List[Tuple[int, int]], List[int]]:
    """
    Parse the input text into fresh ID ranges and available ingredient IDs.
    
    Input format:
    - First section: Fresh ID ranges (e.g., "3-5")
    - Blank line separator
    - Second section: Available ingredient IDs (one per line)
    
    Args:
        text: Input text with two sections separated by blank line
        
    Returns:
        Tuple of (ranges, available_ids) where:
        - ranges: List of (start, end) tuples representing inclusive ranges
        - available_ids: List of ingredient IDs to check
    """
    # Split input into two sections at the blank line
    sections = text.strip().split('\n\n')
    
    # Parse fresh ID ranges from first section
    ranges = []
    # Check if first section contains ranges (has '-' character)
    if sections[0].strip() and '-' in sections[0]:
        range_lines = sections[0].strip().split('\n')
        for line in range_lines:
            line = line.strip()
            if line and '-' in line:  # Skip any empty lines and verify it's a range
                start, end = map(int, line.split('-'))
                ranges.append((start, end))
        
        # Parse available ingredient IDs from second section
        available_ids = []
        if len(sections) > 1 and sections[1].strip():
            id_lines = sections[1].strip().split('\n')
            for line in id_lines:
                if line.strip():  # Skip any empty lines
                    available_ids.append(int(line.strip()))
    else:
        # If first section doesn't contain ranges, treat all input as available IDs
        # This handles the edge case where there are no ranges
        available_ids = []
        for section in sections:
            if section.strip():
                id_lines = section.strip().split('\n')
                for line in id_lines:
                    line = line.strip()
                    if line and '-' not in line:  # Only add if it's not a range
                        available_ids.append(int(line))
    
    return ranges, available_ids


def is_fresh(ingredient_id: int, ranges: List[Tuple[int, int]]) -> bool:
    """
    Check if an ingredient ID is fresh (falls within any range).
    
    An ID is fresh if it falls within at least one range.
    Ranges are inclusive: both start and end values are included.
    
    Args:
        ingredient_id: The ingredient ID to check
        ranges: List of (start, end) tuples representing fresh ID ranges
        
    Returns:
        True if the ID is fresh (in at least one range), False otherwise
    """
    for start, end in ranges:
        # Check if ID falls within this range (inclusive on both ends)
        if start <= ingredient_id <= end:
            return True
    return False


def count_fresh_ingredients(ranges: List[Tuple[int, int]], available: List[int]) -> int:
    """
    Count how many available ingredient IDs are fresh.
    
    Args:
        ranges: List of (start, end) tuples representing fresh ID ranges
        available: List of available ingredient IDs to check
        
    Returns:
        Count of fresh ingredients (IDs that fall within at least one range)
    """
    count = 0
    for ingredient_id in available:
        if is_fresh(ingredient_id, ranges):
            count += 1
    return count


def merge_ranges(ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Merge overlapping or adjacent ranges into non-overlapping intervals.
    
    This is the optimal approach for Part 2 to avoid double-counting IDs.
    
    Algorithm:
    1. Sort ranges by start position
    2. Iterate through sorted ranges
    3. For each range:
       - If it overlaps or is adjacent to the previous merged range, extend the merged range
       - Otherwise, add it as a separate range
    
    Adjacent ranges (e.g., 1-5 and 6-10) are merged because they represent
    consecutive IDs with no gap between them.
    
    Args:
        ranges: List of (start, end) tuples representing inclusive ranges
        
    Returns:
        List of non-overlapping merged ranges sorted by start position
        
    Examples:
        merge_ranges([(1, 5), (3, 7)]) -> [(1, 7)]  # Overlapping
        merge_ranges([(1, 5), (6, 10)]) -> [(1, 10)]  # Adjacent
        merge_ranges([(1, 5), (10, 15)]) -> [(1, 5), (10, 15)]  # Gap between
    """
    # Handle empty input
    if not ranges:
        return []
    
    # Sort ranges by start position
    sorted_ranges = sorted(ranges)
    
    # Initialize merged list with first range
    merged = [sorted_ranges[0]]
    
    # Process each subsequent range
    for start, end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]
        
        # Check if current range overlaps or is adjacent to previous
        # Adjacent means start == last_end + 1 (e.g., 1-5 and 6-10)
        if start <= last_end + 1:
            # Merge by extending the end to the maximum of both ranges
            # Use max() to handle cases where smaller range is inside larger one
            merged[-1] = (last_start, max(last_end, end))
        else:
            # Non-overlapping and non-adjacent, add as separate range
            merged.append((start, end))
    
    return merged


def count_total_fresh_ids(ranges: List[Tuple[int, int]]) -> int:
    """
    Count the total number of unique fresh ingredient IDs across all ranges.
    
    This is the Part 2 solution. Unlike Part 1, we count ALL IDs covered by
    the ranges, not just those in the available IDs list.
    
    Uses interval merging to avoid double-counting IDs that appear in
    multiple overlapping ranges.
    
    Args:
        ranges: List of (start, end) tuples representing fresh ID ranges
        
    Returns:
        Total count of unique fresh IDs across all ranges
        
    Example:
        ranges = [(3, 5), (10, 14), (16, 20), (12, 18)]
        After merging: [(3, 5), (10, 20)]
        Count: (5-3+1) + (20-10+1) = 3 + 11 = 14
    """
    # Handle empty input
    if not ranges:
        return 0
    
    # Merge overlapping ranges to avoid double-counting
    merged = merge_ranges(ranges)
    
    # Sum the size of each merged range
    # Range size is inclusive: end - start + 1
    total = 0
    for start, end in merged:
        total += (end - start + 1)
    
    return total


def main():
    """Main function to run both parts of the puzzle."""
    try:
        with open('input.txt', 'r') as f:
            input_text = f.read()
    except FileNotFoundError:
        print("Error: input.txt not found")
        return
    
    # Parse input
    ranges, available_ids = parse_input(input_text)
    
    # Part 1: Count fresh ingredients from available list
    part1_answer = count_fresh_ingredients(ranges, available_ids)
    print(f"Part 1: {part1_answer}")
    
    # Part 2: Count total unique fresh IDs across all ranges
    part2_answer = count_total_fresh_ids(ranges)
    print(f"Part 2: {part2_answer}")


if __name__ == '__main__':
    main()
