#!/usr/bin/env python3
"""
Test cases for Day 5: Cafeteria solution.
Run these tests before implementing the solution (TDD).

These tests validate:
- Input parsing (ranges and available IDs)
- Freshness checking logic (is_fresh function)
- Fresh ingredient counting (Part 1 solution)
- Range merging logic (merge_ranges function for Part 2)
- Total fresh ID counting (Part 2 solution)
- All edge cases from the specification
"""

import unittest
from solution import (
    parse_input, 
    is_fresh, 
    count_fresh_ingredients,
    merge_ranges,
    count_total_fresh_ids
)


class TestDay05Parsing(unittest.TestCase):
    """Tests for input parsing logic."""
    
    def test_parse_example_input(self):
        """Test parsing the example input from specification."""
        input_text = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""
        ranges, available = parse_input(input_text)
        
        expected_ranges = [(3, 5), (10, 14), (16, 20), (12, 18)]
        expected_available = [1, 5, 8, 11, 17, 32]
        
        self.assertEqual(ranges, expected_ranges, "Ranges parsing failed")
        self.assertEqual(available, expected_available, "Available IDs parsing failed")
    
    def test_parse_single_range(self):
        """Test parsing input with single range."""
        input_text = """5-5

5
10"""
        ranges, available = parse_input(input_text)
        
        self.assertEqual(ranges, [(5, 5)])
        self.assertEqual(available, [5, 10])
    
    def test_parse_empty_available_list(self):
        """Test parsing when available IDs section is empty."""
        input_text = """1-10

"""
        ranges, available = parse_input(input_text)
        
        self.assertEqual(ranges, [(1, 10)])
        self.assertEqual(available, [], "Empty available list should return empty list")
    
    def test_parse_no_ranges(self):
        """Test parsing when ranges section is empty."""
        input_text = """
1
5
10"""
        ranges, available = parse_input(input_text)
        
        self.assertEqual(ranges, [], "Empty ranges section should return empty list")
        self.assertEqual(available, [1, 5, 10])
    
    def test_parse_large_values(self):
        """Test parsing with large range values."""
        input_text = """1000000-1000010

999999
1000000
1000005"""
        ranges, available = parse_input(input_text)
        
        self.assertEqual(ranges, [(1000000, 1000010)])
        self.assertEqual(available, [999999, 1000000, 1000005])
    
    def test_parse_multiple_overlapping_ranges(self):
        """Test parsing multiple overlapping ranges."""
        input_text = """1-10
5-15
10-20
15-25

1"""
        ranges, available = parse_input(input_text)
        
        self.assertEqual(ranges, [(1, 10), (5, 15), (10, 20), (15, 25)])
        self.assertEqual(available, [1])


class TestDay05IsFresh(unittest.TestCase):
    """Tests for the is_fresh() helper function."""
    
    def test_id_within_single_range(self):
        """Test ID that falls within a single range."""
        ranges = [(3, 5)]
        self.assertTrue(is_fresh(4, ranges), "ID 4 should be fresh in range 3-5")
    
    def test_id_at_range_start_boundary(self):
        """Test ID at the start boundary (inclusive)."""
        ranges = [(5, 10)]
        self.assertTrue(is_fresh(5, ranges), "ID 5 should be fresh (start boundary is inclusive)")
    
    def test_id_at_range_end_boundary(self):
        """Test ID at the end boundary (inclusive)."""
        ranges = [(5, 10)]
        self.assertTrue(is_fresh(10, ranges), "ID 10 should be fresh (end boundary is inclusive)")
    
    def test_id_outside_single_range(self):
        """Test ID that falls outside all ranges."""
        ranges = [(10, 20)]
        self.assertFalse(is_fresh(5, ranges), "ID 5 should be spoiled (outside range 10-20)")
        self.assertFalse(is_fresh(25, ranges), "ID 25 should be spoiled (outside range 10-20)")
    
    def test_id_in_overlapping_ranges(self):
        """Test ID that falls within multiple overlapping ranges."""
        ranges = [(10, 14), (12, 18), (16, 20)]
        self.assertTrue(is_fresh(17, ranges), "ID 17 should be fresh (in ranges 12-18 and 16-20)")
        self.assertTrue(is_fresh(13, ranges), "ID 13 should be fresh (in ranges 10-14 and 12-18)")
    
    def test_id_in_gap_between_ranges(self):
        """Test ID that falls in gap between non-overlapping ranges."""
        ranges = [(1, 5), (10, 15)]
        self.assertFalse(is_fresh(7, ranges), "ID 7 should be spoiled (in gap between ranges)")
    
    def test_id_with_empty_ranges(self):
        """Test ID checking with no ranges (all spoiled)."""
        ranges = []
        self.assertFalse(is_fresh(5, ranges), "ID 5 should be spoiled (no ranges defined)")
    
    def test_id_just_before_range(self):
        """Test ID just before range start."""
        ranges = [(5, 10)]
        self.assertFalse(is_fresh(4, ranges), "ID 4 should be spoiled (just before range 5-10)")
    
    def test_id_just_after_range(self):
        """Test ID just after range end."""
        ranges = [(5, 10)]
        self.assertFalse(is_fresh(11, ranges), "ID 11 should be spoiled (just after range 5-10)")
    
    def test_id_in_single_element_range(self):
        """Test ID in a single-element range."""
        ranges = [(5, 5)]
        self.assertTrue(is_fresh(5, ranges), "ID 5 should be fresh (range is 5-5)")
        self.assertFalse(is_fresh(4, ranges), "ID 4 should be spoiled")
        self.assertFalse(is_fresh(6, ranges), "ID 6 should be spoiled")


class TestDay05CountFreshIngredients(unittest.TestCase):
    """Tests for the count_fresh_ingredients() function (Part 1 solution)."""
    
    def test_example_from_spec(self):
        """Test Part 1 with the example from specification."""
        ranges = [(3, 5), (10, 14), (16, 20), (12, 18)]
        available = [1, 5, 8, 11, 17, 32]
        
        result = count_fresh_ingredients(ranges, available)
        
        self.assertEqual(result, 3, "Example should have 3 fresh ingredients (5, 11, 17)")
    
    def test_single_id_range(self):
        """Test with single-element range (Edge Case 1)."""
        ranges = [(5, 5)]
        available = [5, 10]
        
        result = count_fresh_ingredients(ranges, available)
        
        self.assertEqual(result, 1, "Only ID 5 should be fresh")
    
    def test_empty_available_list(self):
        """Test with empty available list (Edge Case 2)."""
        ranges = [(1, 10)]
        available = []
        
        result = count_fresh_ingredients(ranges, available)
        
        self.assertEqual(result, 0, "No available IDs means 0 fresh")
    
    def test_no_ranges(self):
        """Test with no ranges defined (Edge Case 3)."""
        ranges = []
        available = [1, 5, 10]
        
        result = count_fresh_ingredients(ranges, available)
        
        self.assertEqual(result, 0, "No ranges means all IDs are spoiled")
    
    def test_all_available_ids_fresh(self):
        """Test when all available IDs are fresh (Edge Case 4)."""
        ranges = [(1, 100)]
        available = [5, 10, 50, 99]
        
        result = count_fresh_ingredients(ranges, available)
        
        self.assertEqual(result, 4, "All 4 IDs should be fresh")
    
    def test_all_available_ids_spoiled(self):
        """Test when all available IDs are spoiled (Edge Case 5)."""
        ranges = [(10, 20)]
        available = [1, 5, 25, 30]
        
        result = count_fresh_ingredients(ranges, available)
        
        self.assertEqual(result, 0, "All IDs should be spoiled (outside range)")
    
    def test_boundary_testing(self):
        """Test boundary values (inclusive ranges) (Edge Case 6)."""
        ranges = [(5, 10)]
        available = [4, 5, 10, 11]
        
        result = count_fresh_ingredients(ranges, available)
        
        self.assertEqual(result, 2, "IDs 5 and 10 should be fresh (boundaries are inclusive)")
    
    def test_completely_overlapping_ranges(self):
        """Test with completely overlapping ranges (Edge Case 7)."""
        ranges = [(5, 20), (10, 15)]
        available = [7, 12, 18]
        
        result = count_fresh_ingredients(ranges, available)
        
        self.assertEqual(result, 3, "All 3 IDs should be fresh (within outer range)")
    
    def test_adjacent_non_overlapping_ranges(self):
        """Test adjacent but non-overlapping ranges (Edge Case 8)."""
        ranges = [(1, 5), (6, 10)]
        available = [5, 6]
        
        result = count_fresh_ingredients(ranges, available)
        
        self.assertEqual(result, 2, "Both boundary IDs should be fresh")
    
    def test_gap_between_ranges(self):
        """Test ID in gap between ranges (Edge Case 9)."""
        ranges = [(1, 5), (10, 15)]
        available = [7, 12]
        
        result = count_fresh_ingredients(ranges, available)
        
        self.assertEqual(result, 1, "Only ID 12 should be fresh, ID 7 is in gap")
    
    def test_large_range_values(self):
        """Test with large range values (Edge Case 10)."""
        ranges = [(1000000, 1000010)]
        available = [999999, 1000000, 1000005, 1000010, 1000011]
        
        result = count_fresh_ingredients(ranges, available)
        
        self.assertEqual(result, 3, "IDs 1000000, 1000005, 1000010 should be fresh")
    
    def test_many_overlapping_ranges(self):
        """Test with many overlapping ranges (Edge Case 11)."""
        ranges = [(1, 10), (5, 15), (10, 20), (15, 25)]
        available = [1, 7, 13, 18, 30]
        
        result = count_fresh_ingredients(ranges, available)
        
        self.assertEqual(result, 4, "IDs 1, 7, 13, 18 should be fresh (not 30)")


class TestDay05EdgeCasesParameterized(unittest.TestCase):
    """Parameterized tests for comprehensive edge case coverage."""
    
    def test_multiple_boundary_cases(self):
        """Test multiple boundary scenarios in one parameterized test."""
        test_cases = [
            # (ranges, available, expected_count, description)
            ([(1, 5)], [1], 1, "first element of range"),
            ([(1, 5)], [5], 1, "last element of range"),
            ([(1, 5)], [3], 1, "middle element of range"),
            ([(1, 5)], [0], 0, "before range start"),
            ([(1, 5)], [6], 0, "after range end"),
            ([(1, 5), (7, 10)], [6], 0, "between two ranges"),
            ([(1, 5), (5, 10)], [5], 1, "overlap at boundary"),
        ]
        
        for ranges, available, expected, description in test_cases:
            with self.subTest(description=description):
                result = count_fresh_ingredients(ranges, available)
                self.assertEqual(result, expected, f"Failed for: {description}")


class TestDay05IntegrationWithParsing(unittest.TestCase):
    """Integration tests that combine parsing and counting."""
    
    def test_end_to_end_example(self):
        """Test complete flow from input string to answer."""
        input_text = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""
        ranges, available = parse_input(input_text)
        result = count_fresh_ingredients(ranges, available)
        
        self.assertEqual(result, 3, "End-to-end example should yield 3 fresh ingredients")
    
    def test_end_to_end_all_fresh(self):
        """Test complete flow where all IDs are fresh."""
        input_text = """1-100

10
20
30"""
        ranges, available = parse_input(input_text)
        result = count_fresh_ingredients(ranges, available)
        
        self.assertEqual(result, 3, "All IDs should be fresh")
    
    def test_end_to_end_none_fresh(self):
        """Test complete flow where no IDs are fresh."""
        input_text = """50-60

1
2
3
100"""
        ranges, available = parse_input(input_text)
        result = count_fresh_ingredients(ranges, available)
        
        self.assertEqual(result, 0, "No IDs should be fresh")


class TestDay05Part2MergeRanges(unittest.TestCase):
    """Tests for the merge_ranges() function (Part 2 helper)."""
    
    def test_merge_non_overlapping_ranges(self):
        """Test merging non-overlapping ranges (should remain separate)."""
        ranges = [(1, 5), (10, 15)]
        result = merge_ranges(ranges)
        expected = [(1, 5), (10, 15)]
        self.assertEqual(result, expected, "Non-overlapping ranges should remain separate")
    
    def test_merge_overlapping_ranges(self):
        """Test merging overlapping ranges."""
        ranges = [(1, 10), (5, 15)]
        result = merge_ranges(ranges)
        expected = [(1, 15)]
        self.assertEqual(result, expected, "Overlapping ranges should merge to (1, 15)")
    
    def test_merge_adjacent_ranges(self):
        """Test merging adjacent ranges (touching boundaries)."""
        ranges = [(1, 5), (6, 10)]
        result = merge_ranges(ranges)
        expected = [(1, 10)]
        self.assertEqual(result, expected, "Adjacent ranges (1-5 and 6-10) should merge to (1, 10)")
    
    def test_merge_multiple_overlaps(self):
        """Test merging multiple overlapping ranges."""
        ranges = [(1, 5), (3, 7), (6, 10)]
        result = merge_ranges(ranges)
        expected = [(1, 10)]
        self.assertEqual(result, expected, "Multiple overlaps should merge into single range")
    
    def test_merge_completely_contained_range(self):
        """Test merging when one range is completely contained in another."""
        ranges = [(1, 20), (5, 10), (12, 15)]
        result = merge_ranges(ranges)
        expected = [(1, 20)]
        self.assertEqual(result, expected, "Contained ranges should be absorbed into larger range")
    
    def test_merge_unsorted_input(self):
        """Test that merge handles unsorted input correctly."""
        ranges = [(10, 15), (1, 5), (3, 9)]
        result = merge_ranges(ranges)
        expected = [(1, 15)]
        self.assertEqual(result, expected, "Should sort and merge unsorted ranges correctly")
    
    def test_merge_single_range(self):
        """Test merging with single range."""
        ranges = [(5, 10)]
        result = merge_ranges(ranges)
        expected = [(5, 10)]
        self.assertEqual(result, expected, "Single range should remain unchanged")
    
    def test_merge_empty_list(self):
        """Test merging with empty range list."""
        ranges = []
        result = merge_ranges(ranges)
        expected = []
        self.assertEqual(result, expected, "Empty list should return empty list")
    
    def test_merge_single_element_ranges(self):
        """Test merging single-element ranges (X-X)."""
        ranges = [(5, 5), (7, 7), (6, 6)]
        result = merge_ranges(ranges)
        expected = [(5, 7)]
        self.assertEqual(result, expected, "Adjacent single-element ranges should merge")
    
    def test_merge_three_way_overlap(self):
        """Test three ranges that all overlap."""
        ranges = [(1, 10), (5, 15), (10, 20)]
        result = merge_ranges(ranges)
        expected = [(1, 20)]
        self.assertEqual(result, expected, "Three overlapping ranges should merge to (1, 20)")
    
    def test_merge_multiple_separate_groups(self):
        """Test merging with multiple separate groups of overlapping ranges."""
        ranges = [(1, 5), (3, 7), (20, 25), (22, 30), (50, 55)]
        result = merge_ranges(ranges)
        expected = [(1, 7), (20, 30), (50, 55)]
        self.assertEqual(result, expected, "Should create separate merged groups")
    
    def test_merge_exact_overlap(self):
        """Test merging identical ranges."""
        ranges = [(5, 10), (5, 10), (5, 10)]
        result = merge_ranges(ranges)
        expected = [(5, 10)]
        self.assertEqual(result, expected, "Identical ranges should merge to single range")
    
    def test_merge_large_values(self):
        """Test merging with large range values."""
        ranges = [(1000000, 1000010), (1000005, 1000015)]
        result = merge_ranges(ranges)
        expected = [(1000000, 1000015)]
        self.assertEqual(result, expected, "Large value ranges should merge correctly")


class TestDay05Part2CountTotalFresh(unittest.TestCase):
    """Tests for the count_total_fresh_ids() function (Part 2 solution)."""
    
    def test_part2_example_from_spec(self):
        """Test Part 2 with the example from specification (expected: 14)."""
        ranges = [(3, 5), (10, 14), (16, 20), (12, 18)]
        result = count_total_fresh_ids(ranges)
        self.assertEqual(result, 14, "Example should have 14 total fresh IDs")
    
    def test_part2_single_range(self):
        """Test Part 2 Case 1: Single range."""
        ranges = [(5, 10)]
        result = count_total_fresh_ids(ranges)
        expected = 6  # IDs: 5, 6, 7, 8, 9, 10
        self.assertEqual(result, expected, "Single range 5-10 should have 6 IDs")
    
    def test_part2_non_overlapping_ranges(self):
        """Test Part 2 Case 2: Multiple non-overlapping ranges."""
        ranges = [(1, 3), (10, 12), (20, 22)]
        result = count_total_fresh_ids(ranges)
        expected = 9  # 3 + 3 + 3
        self.assertEqual(result, expected, "Non-overlapping ranges should sum to 9 IDs")
    
    def test_part2_completely_overlapping_ranges(self):
        """Test Part 2 Case 3: Completely overlapping ranges."""
        ranges = [(5, 20), (10, 15), (12, 18)]
        result = count_total_fresh_ids(ranges)
        expected = 16  # All within 5-20: 5 through 20 inclusive
        self.assertEqual(result, expected, "Completely overlapping ranges should have 16 unique IDs")
    
    def test_part2_adjacent_ranges(self):
        """Test Part 2 Case 4: Adjacent ranges."""
        ranges = [(1, 5), (6, 10), (11, 15)]
        result = count_total_fresh_ids(ranges)
        expected = 15  # Should merge to 1-15
        self.assertEqual(result, expected, "Adjacent ranges should merge to 15 IDs")
    
    def test_part2_partially_overlapping_ranges(self):
        """Test Part 2 Case 5: Partially overlapping ranges."""
        ranges = [(1, 10), (5, 15), (10, 20)]
        result = count_total_fresh_ids(ranges)
        expected = 20  # Merges to 1-20
        self.assertEqual(result, expected, "Partially overlapping ranges should cover 1-20 (20 IDs)")
    
    def test_part2_many_overlapping_ranges(self):
        """Test Part 2 Case 6: Many small overlaps."""
        ranges = [(1, 5), (3, 7), (5, 9), (7, 11)]
        result = count_total_fresh_ids(ranges)
        expected = 11  # Merges to 1-11
        self.assertEqual(result, expected, "Many overlapping ranges should merge to 1-11 (11 IDs)")
    
    def test_part2_large_range_values(self):
        """Test Part 2 Case 7: Large range values."""
        ranges = [(1000000, 1000010), (1000005, 1000015)]
        result = count_total_fresh_ids(ranges)
        expected = 16  # Merges to 1000000-1000015 (16 IDs)
        self.assertEqual(result, expected, "Large ranges should merge correctly to 16 IDs")
    
    def test_part2_empty_range_list(self):
        """Test Part 2 Case 8: Empty range list."""
        ranges = []
        result = count_total_fresh_ids(ranges)
        expected = 0
        self.assertEqual(result, expected, "Empty range list should have 0 fresh IDs")
    
    def test_part2_complex_mix(self):
        """Test Part 2 Case 9: Complex mix of overlaps and gaps."""
        ranges = [(1, 5), (3, 7), (20, 25), (22, 30), (50, 55)]
        result = count_total_fresh_ids(ranges)
        # Group 1: (1, 5) + (3, 7) = (1, 7) = 7 IDs
        # Group 2: (20, 25) + (22, 30) = (20, 30) = 11 IDs
        # Group 3: (50, 55) = 6 IDs
        # Total: 7 + 11 + 6 = 24 IDs
        expected = 24
        self.assertEqual(result, expected, "Complex mix should yield 24 total IDs")
    
    def test_part2_single_element_ranges(self):
        """Test Part 2 with single-element ranges (X-X format)."""
        ranges = [(5, 5), (10, 10), (15, 15)]
        result = count_total_fresh_ids(ranges)
        expected = 3  # Three separate single-element ranges
        self.assertEqual(result, expected, "Three single-element ranges should have 3 IDs")
    
    def test_part2_adjacent_single_elements(self):
        """Test Part 2 with adjacent single-element ranges."""
        ranges = [(5, 5), (6, 6), (7, 7)]
        result = count_total_fresh_ids(ranges)
        expected = 3  # Should merge to (5, 7) = 3 IDs
        self.assertEqual(result, expected, "Adjacent single elements should merge to 3 IDs")
    
    def test_part2_duplicate_ranges(self):
        """Test Part 2 with duplicate ranges."""
        ranges = [(1, 10), (1, 10), (1, 10)]
        result = count_total_fresh_ids(ranges)
        expected = 10  # Should merge to single (1, 10) = 10 IDs
        self.assertEqual(result, expected, "Duplicate ranges should not double-count")
    
    def test_part2_one_range_contains_many(self):
        """Test Part 2 where one large range contains many smaller ranges."""
        ranges = [(1, 100), (10, 20), (30, 40), (50, 60)]
        result = count_total_fresh_ids(ranges)
        expected = 100  # All contained in (1, 100)
        self.assertEqual(result, expected, "Large containing range should absorb all others")
    
    def test_part2_boundary_adjacency(self):
        """Test Part 2 with ranges that exactly touch at boundaries."""
        ranges = [(1, 10), (11, 20), (21, 30)]
        result = count_total_fresh_ids(ranges)
        expected = 30  # Should merge to (1, 30)
        self.assertEqual(result, expected, "Boundary-adjacent ranges should merge")
    
    def test_part2_no_double_counting_overlaps(self):
        """Test Part 2 ensures no double-counting with heavy overlaps."""
        # Create overlapping ranges that could easily be double-counted
        ranges = [(1, 10), (5, 15), (10, 20), (15, 25)]
        result = count_total_fresh_ids(ranges)
        expected = 25  # Should merge to (1, 25) = 25 IDs, not sum of individual sizes
        self.assertEqual(result, expected, "Should not double-count overlapping IDs")


class TestDay05Part2Integration(unittest.TestCase):
    """Integration tests for Part 2 combining parsing and counting."""
    
    def test_part2_end_to_end_example(self):
        """Test Part 2 complete flow from input string to answer."""
        input_text = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""
        # For Part 2, we ignore the available IDs section
        sections = input_text.strip().split('\n\n')
        range_lines = sections[0].strip().split('\n')
        ranges = []
        for line in range_lines:
            start, end = map(int, line.split('-'))
            ranges.append((start, end))
        
        result = count_total_fresh_ids(ranges)
        self.assertEqual(result, 14, "Part 2 example should yield 14 total fresh IDs")
    
    def test_part2_end_to_end_simple(self):
        """Test Part 2 with simple non-overlapping ranges."""
        input_text = """1-5
10-15

100"""
        sections = input_text.strip().split('\n\n')
        range_lines = sections[0].strip().split('\n')
        ranges = []
        for line in range_lines:
            start, end = map(int, line.split('-'))
            ranges.append((start, end))
        
        result = count_total_fresh_ids(ranges)
        expected = 11  # 5 IDs (1-5) + 6 IDs (10-15) = 11
        self.assertEqual(result, expected, "Should have 11 total fresh IDs")
    
    def test_part2_end_to_end_all_overlap(self):
        """Test Part 2 where all ranges overlap completely."""
        input_text = """1-100
10-50
25-75

5"""
        sections = input_text.strip().split('\n\n')
        range_lines = sections[0].strip().split('\n')
        ranges = []
        for line in range_lines:
            start, end = map(int, line.split('-'))
            ranges.append((start, end))
        
        result = count_total_fresh_ids(ranges)
        expected = 100  # All contained in 1-100
        self.assertEqual(result, expected, "Should have 100 total fresh IDs")


if __name__ == '__main__':
    unittest.main()
