#!/usr/bin/env python3
"""
Test cases for Day 07: Laboratories
Run these tests before implementing the solution (TDD).

This test suite validates the tachyon beam simulation, including:
- Input parsing for grid, start position, and splitters
- Beam splitting behavior when encountering splitters
- Beam merging when multiple beams reach the same position
- Edge cases with boundary conditions
"""

import unittest
from solution import parse_input, solve_part1, solve_part2


class TestDay07Parsing(unittest.TestCase):
    """Tests for input parsing logic."""
    
    def test_parse_example_input(self):
        """Test parsing the main example input from spec."""
        input_text = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""
        
        data = parse_input(input_text)
        
        # Should parse grid dimensions
        self.assertIsNotNone(data)
        
        # Should identify start position (row 0, column 7)
        # Should identify grid dimensions (16 rows, 15 columns)
        # Should identify all splitter positions
        # The exact structure depends on implementation, but should contain these elements
    
    def test_parse_simple_grid(self):
        """Test parsing a simple grid with one splitter."""
        input_text = """...S...
.......
...^...
......."""
        
        data = parse_input(input_text)
        self.assertIsNotNone(data)
        
        # Should identify start at column 3
        # Should identify one splitter at row 2, column 3
    
    def test_parse_no_splitters(self):
        """Test parsing grid with no splitters."""
        input_text = """...S...
.......
.......
......."""
        
        data = parse_input(input_text)
        self.assertIsNotNone(data)
        
        # Should handle grid with no splitters
    
    def test_parse_start_at_left_edge(self):
        """Test parsing with start position at left edge."""
        input_text = """S......
.......
...^...
......."""
        
        data = parse_input(input_text)
        self.assertIsNotNone(data)
        
        # Should handle start at column 0
    
    def test_parse_start_at_right_edge(self):
        """Test parsing with start position at right edge."""
        input_text = """......S
.......
...^...
......."""
        
        data = parse_input(input_text)
        self.assertIsNotNone(data)
        
        # Should handle start at last column


class TestDay07Part1(unittest.TestCase):
    """Tests for Part 1 solution - counting beam splits."""
    
    def setUp(self):
        """Set up test fixtures and example data."""
        # Main example from spec
        self.main_example = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""
    
    def test_example_from_spec(self):
        """Test Part 1 with the main example from specification.
        
        The beam starts at S (row 0, col 7) and travels downward.
        It splits 21 times total as it encounters splitters:
        - Row 2: 1 split
        - Row 4: 2 splits
        - Row 6: 3 splits
        - Row 8: 4 splits
        - Row 10: 5 splits
        - Row 12: 5 splits (with beam merging)
        - Row 14: 1 split
        Total: 21 splits
        """
        data = parse_input(self.main_example)
        result = solve_part1(data)
        self.assertEqual(result, 21, "Main example should produce 21 splits")
    
    def test_single_splitter(self):
        """Test Part 1 with a single splitter directly below start.
        
        Beam goes straight down and hits one splitter.
        Expected: 1 split
        """
        input_text = """...S...
.......
...^...
......."""
        
        data = parse_input(input_text)
        result = solve_part1(data)
        self.assertEqual(result, 1, "Single splitter should produce 1 split")
    
    def test_no_splitters(self):
        """Test Part 1 with no splitters.
        
        Beam just passes through empty space and exits.
        Expected: 0 splits
        """
        input_text = """...S...
.......
.......
......."""
        
        data = parse_input(input_text)
        result = solve_part1(data)
        self.assertEqual(result, 0, "No splitters should produce 0 splits")
    
    def test_two_splitters_adjacent(self):
        """Test Part 1 with two adjacent splitters.
        
        Starting configuration:
        ...S...
        .......
        ..^.^..
        .......
        
        Beam at col 3 goes down to row 2. There's a splitter at col 2 and col 4.
        The beam at col 3 passes between them (no split at row 2).
        Expected: 0 splits (beam passes between splitters)
        """
        input_text = """...S...
.......
..^.^..
......."""
        
        data = parse_input(input_text)
        result = solve_part1(data)
        self.assertEqual(result, 0, "Beam passing between two splitters should produce 0 splits")
    
    def test_vertical_stack_splitters(self):
        """Test Part 1 with vertical stack of splitters.
        
        Configuration:
        ...S...
        .......
        ...^...  <- First split (1 total)
        .......
        ..^.^..  <- Both beams hit splitters (3 total)
        .......
        
        Row 0-1: Beam at col 3
        Row 2: Beam hits splitter at col 3, splits into col 2 and col 4 (1 split)
        Row 3: Beams at col 2 and col 4
        Row 4: Beam at col 2 hits splitter, beam at col 4 hits splitter (2 more splits)
                Creates beams at col 1, 3, 3, 5 -> merge to col 1, 3, 5
        Expected: 3 splits total
        """
        input_text = """...S...
.......
...^...
.......
..^.^..
......."""
        
        data = parse_input(input_text)
        result = solve_part1(data)
        self.assertEqual(result, 3, "Vertical stack should produce 3 splits with merging")
    
    def test_beam_merging(self):
        """Test Part 1 with explicit beam merging scenario.
        
        Configuration:
        ..S.S..
        .......
        .^...^.
        .......
        ..^.^..
        .......
        
        Two starting beams at col 2 and col 4.
        Row 2: Both hit splitters (2 splits)
                Left beam (col 2) splits to col 1 and 3
                Right beam (col 4) splits to col 3 and 5
                Beams at col 3 merge
        Row 3: Beams at col 1, 3, 5
        Row 4: Beams at col 1 and 5 pass through, beam at col 3 is between splitters
        Expected: 2 splits
        """
        input_text = """..S.S..
.......
.^...^.
.......
..^.^..
......."""
        
        data = parse_input(input_text)
        result = solve_part1(data)
        self.assertEqual(result, 2, "Beam merging should count each split once")
    
    def test_edge_case_start_at_column_zero(self):
        """Test Part 1 with start at left edge (column 0).
        
        Configuration:
        S......
        .......
        ^......
        .......
        
        Beam at col 0 hits splitter at col 0.
        Splits to col -1 (out of bounds) and col 1.
        Only col 1 beam continues.
        Expected: 1 split (even though one beam goes out of bounds)
        """
        input_text = """S......
.......
^......
......."""
        
        data = parse_input(input_text)
        result = solve_part1(data)
        self.assertEqual(result, 1, "Splitter at edge should still count as 1 split")
    
    def test_edge_case_start_at_last_column(self):
        """Test Part 1 with start at right edge.
        
        Configuration:
        ......S
        .......
        ......^
        .......
        
        Beam at col 6 hits splitter at col 6.
        Splits to col 5 and col 7 (out of bounds).
        Only col 5 beam continues.
        Expected: 1 split
        """
        input_text = """......S
.......
......^
......."""
        
        data = parse_input(input_text)
        result = solve_part1(data)
        self.assertEqual(result, 1, "Splitter at right edge should count as 1 split")
    
    def test_splitter_on_last_row(self):
        """Test Part 1 with splitter on the last row.
        
        Configuration:
        ...S...
        .......
        ...^...
        
        Beam hits splitter on last row.
        New beams are created but immediately exit.
        Expected: 1 split
        """
        input_text = """...S...
.......
...^..."""
        
        data = parse_input(input_text)
        result = solve_part1(data)
        self.assertEqual(result, 1, "Splitter on last row should still count")
    
    def test_beam_misses_all_splitters(self):
        """Test Part 1 where beam path doesn't hit any splitters.
        
        Configuration:
        ...S...
        .......
        ^.....^
        .......
        
        Beam at col 3 passes between splitters at col 0 and col 6.
        Expected: 0 splits
        """
        input_text = """...S...
.......
^.....^
......."""
        
        data = parse_input(input_text)
        result = solve_part1(data)
        self.assertEqual(result, 0, "Beam missing all splitters should produce 0 splits")
    
    def test_complex_merging_pattern(self):
        """Test Part 1 with complex merging pattern.
        
        Configuration:
        ....S....
        .........
        ....^....  <- 1 split (beams at col 3, 5)
        .........
        ...^.^...  <- 2 splits (beams at col 3, 5 both hit)
        .........     Creates beams at 2,4,4,6 -> merge to 2,4,6
        
        Expected: 3 splits total
        """
        input_text = """....S....
.........
....^....
.........
...^.^...
........."""
        
        data = parse_input(input_text)
        result = solve_part1(data)
        self.assertEqual(result, 3, "Complex merging should count all splits correctly")
    
    def test_single_row_grid(self):
        """Test Part 1 with minimal single row grid.
        
        Configuration:
        S
        
        Beam starts and immediately exits.
        Expected: 0 splits
        """
        input_text = """S"""
        
        data = parse_input(input_text)
        result = solve_part1(data)
        self.assertEqual(result, 0, "Single row should produce 0 splits")
    
    def test_empty_grid_below_start(self):
        """Test Part 1 with many empty rows below start.
        
        Configuration:
        S
        .
        .
        .
        .
        .
        
        Beam travels through all empty rows and exits.
        Expected: 0 splits
        """
        input_text = """S
.
.
.
.
."""
        
        data = parse_input(input_text)
        result = solve_part1(data)
        self.assertEqual(result, 0, "Empty rows should produce 0 splits")
    
    def test_all_beams_exit_at_edges(self):
        """Test Part 1 where all beams exit at edges after splitting.
        
        Configuration:
        .S.
        ...
        .^.
        ...
        
        Beam at col 1 hits splitter at col 1.
        Creates beams at col 0 and col 2.
        Both beams exit at bottom.
        Expected: 1 split
        """
        input_text = """.S.
...
.^.
..."""
        
        data = parse_input(input_text)
        result = solve_part1(data)
        self.assertEqual(result, 1, "Beams exiting at edges should still count split")


class TestDay07Part2(unittest.TestCase):
    """Tests for Part 2 solution - counting quantum timelines (never merge)."""
    
    def setUp(self):
        """Set up test fixtures and example data."""
        self.main_example = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
..............."""
    
    def test_example_from_spec_part2(self):
        """Test Part 2 with the main example from specification.
        
        In Part 2, we count unique quantum timelines that NEVER merge,
        even if they reach the same position. Each unique path through
        the splitter network represents a distinct timeline.
        
        The main example creates 40 unique timelines.
        """
        data = parse_input(self.main_example)
        result = solve_part2(data)
        self.assertEqual(result, 40, "Main example should produce 40 timelines")
    
    def test_single_splitter(self):
        """Test Part 2 with a single splitter.
        
        Configuration:
        ...S...
        .......
        ...^...
        .......
        
        The particle starts at col 3, hits the splitter, creating:
        - Timeline 1: Goes left (col 2) and exits
        - Timeline 2: Goes right (col 4) and exits
        
        Expected: 2 timelines
        """
        input_text = """...S...
.......
...^...
......."""
        
        data = parse_input(input_text)
        result = solve_part2(data)
        self.assertEqual(result, 2, "Single splitter should produce 2 timelines")
    
    def test_no_splitters(self):
        """Test Part 2 with no splitters.
        
        Configuration:
        ...S...
        .......
        .......
        .......
        
        The particle travels straight down with no branching.
        Expected: 1 timeline (single path, no splits)
        """
        input_text = """...S...
.......
.......
......."""
        
        data = parse_input(input_text)
        result = solve_part2(data)
        self.assertEqual(result, 1, "No splitters should produce 1 timeline")
    
    def test_two_splitters_vertically_stacked_aligned(self):
        """Test Part 2 with two splitters creating 4 timelines.
        
        Configuration:
        ...S...
        .......
        ...^...  <- First splitter at col 3
        .......
        ..^.^..  <- Splitters at col 2 and col 4
        .......
        
        Timeline tree:
        1. Start at col 3
        2. Hit splitter at row 2, col 3 → branches to col 2 and col 4
        3. Timeline at col 2 hits splitter at row 4, col 2 → branches to col 1 and col 3
        4. Timeline at col 4 hits splitter at row 4, col 4 → branches to col 3 and col 5
        
        Final timelines: 4 (ending at cols 1, 3, 3, 5)
        Note: Two timelines end at col 3, but they took different paths, so count as 2 separate timelines!
        
        Expected: 4 timelines (2^2 exponential growth)
        """
        input_text = """...S...
.......
...^...
.......
..^.^..
......."""
        
        data = parse_input(input_text)
        result = solve_part2(data)
        self.assertEqual(result, 4, "Two vertically stacked splitters should produce 4 timelines")
    
    def test_different_paths_same_endpoint(self):
        """Test Part 2 demonstrating critical difference: same endpoint, different paths.
        
        Configuration:
        ....S....
        .........
        ....^....  <- Splitter at col 4
        .........
        ...^.^...  <- Splitters at col 3 and col 5
        .........
        
        Timeline tree:
        1. Start at col 4
        2. Row 2: Hit splitter → branches to col 3 and col 5
        3. Row 4:
           - Timeline at col 3 hits splitter → branches to col 2 and col 4
           - Timeline at col 5 hits splitter → branches to col 4 and col 6
        
        Final timelines: 4 (ending at cols 2, 4, 4, 6)
        
        The KEY INSIGHT: Two timelines end at column 4, but they are DIFFERENT timelines:
        - Timeline A: Started at 4 → went left to 3 → went right to 4
        - Timeline B: Started at 4 → went right to 5 → went left to 4
        
        Part 1 would merge these (count as 3 beams).
        Part 2 counts them separately (4 distinct timelines).
        
        Expected: 4 timelines
        """
        input_text = """....S....
.........
....^....
.........
...^.^...
........."""
        
        data = parse_input(input_text)
        result = solve_part2(data)
        self.assertEqual(result, 4, "Different paths to same endpoint should count as separate timelines")
    
    def test_no_splitters_hit(self):
        """Test Part 2 where particle misses all splitters.
        
        Configuration:
        ...S...
        .......
        ^.....^
        .......
        
        Particle at col 3 travels straight down between splitters at col 0 and col 6.
        No splitters encountered, no timeline branching.
        
        Expected: 1 timeline
        """
        input_text = """...S...
.......
^.....^
......."""
        
        data = parse_input(input_text)
        result = solve_part2(data)
        self.assertEqual(result, 1, "Particle missing all splitters should produce 1 timeline")
    
    def test_three_level_binary_tree(self):
        """Test Part 2 with three levels of perfect binary splitting.
        
        Configuration:
        .......S.......
        ...............
        .......^.......  <- Row 2: 1 splitter
        ...............
        ......^.^......  <- Row 4: 2 splitters
        ...............
        .....^.^.^.....  <- Row 6: 3 splitters (but not all hit)
        ...............
        
        Timeline tree (if perfectly aligned):
        Row 0: 1 particle at col 7
        Row 2: Hits splitter at col 7 → 2 timelines (cols 6, 8)
        Row 4: Both hit splitters → 4 timelines (cols 5, 7, 7, 9)
        Row 6: If splitters at cols 5, 7, 9, all hit → 8 timelines
        
        But we need to trace carefully which columns hit which splitters.
        Let's trace:
        - Start col 7
        - Row 2 splitter at col 7: creates cols 6, 8
        - Row 4 splitters at cols 6, 8: both hit!
          - Col 6 → creates cols 5, 7
          - Col 8 → creates cols 7, 9
          - Total: 4 timelines at cols 5, 7, 7, 9
        - Row 6 splitters at cols 5, 7, 9:
          - Col 5 → hits splitter → creates cols 4, 6
          - Col 7 (first instance) → hits splitter → creates cols 6, 8
          - Col 7 (second instance) → hits splitter → creates cols 6, 8
          - Col 9 → hits splitter → creates cols 8, 10
          - Total: 8 timelines
        
        Expected: 8 timelines (2^3 for 3 levels)
        """
        input_text = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
..............."""
        
        data = parse_input(input_text)
        result = solve_part2(data)
        self.assertEqual(result, 8, "Three-level binary tree should produce 8 timelines")
    
    def test_edge_case_splitter_at_column_zero(self):
        """Test Part 2 with splitter at left edge.
        
        Configuration:
        S......
        .......
        ^......
        .......
        
        Particle at col 0 hits splitter at col 0.
        Creates timelines at cols -1 (out of bounds) and col 1.
        Both timelines count, even though col -1 is out of bounds!
        
        Expected: 2 timelines
        """
        input_text = """S......
.......
^......
......."""
        
        data = parse_input(input_text)
        result = solve_part2(data)
        self.assertEqual(result, 2, "Splitter at edge should produce 2 timelines (including out-of-bounds)")
    
    def test_edge_case_splitter_at_last_column(self):
        """Test Part 2 with splitter at right edge.
        
        Configuration:
        ......S
        .......
        ......^
        .......
        
        Particle at col 6 hits splitter at col 6.
        Creates timelines at col 5 and col 7 (out of bounds).
        
        Expected: 2 timelines
        """
        input_text = """......S
.......
......^
......."""
        
        data = parse_input(input_text)
        result = solve_part2(data)
        self.assertEqual(result, 2, "Splitter at right edge should produce 2 timelines")
    
    def test_splitter_on_last_row(self):
        """Test Part 2 with splitter on last row.
        
        Configuration:
        ...S...
        .......
        ...^...
        
        Particle hits splitter on last row, creates 2 timelines that immediately exit.
        
        Expected: 2 timelines
        """
        input_text = """...S...
.......
...^..."""
        
        data = parse_input(input_text)
        result = solve_part2(data)
        self.assertEqual(result, 2, "Splitter on last row should produce 2 timelines")
    
    def test_linear_chain_of_splitters(self):
        """Test Part 2 with linear chain demonstrating exponential growth.
        
        Configuration:
        S.....
        ......
        ^.....  <- First splitter
        ......
        ^.^...  <- Two splitters
        ......
        
        Wait, this won't create a perfect chain. Let me reconsider.
        For a true linear chain where every timeline hits a splitter:
        
        S at col 2
        Row 2: splitter at col 2 → 2 timelines (cols 1, 3)
        Row 4: splitters at cols 1, 3 → both hit → 4 timelines (cols 0, 2, 2, 4)
        
        Expected: 4 timelines (2^2)
        """
        input_text = """..S...
......
..^...
......
.^.^..
......"""
        
        data = parse_input(input_text)
        result = solve_part2(data)
        self.assertEqual(result, 4, "Linear chain should demonstrate exponential growth")
    
    def test_single_row_grid(self):
        """Test Part 2 with minimal single row grid.
        
        Configuration:
        S
        
        Particle starts and immediately exits with no branching.
        Expected: 1 timeline
        """
        input_text = """S"""
        
        data = parse_input(input_text)
        result = solve_part2(data)
        self.assertEqual(result, 1, "Single row should produce 1 timeline")
    
    def test_asymmetric_branching(self):
        """Test Part 2 with asymmetric branching pattern.
        
        Configuration:
        ...S...
        .......
        ...^...  <- Splitter at col 3
        .......
        ..^....  <- Only left branch hits a splitter
        .......
        
        Timeline tree:
        Start col 3 → row 2 splits to cols 2, 4
        - Col 2 hits splitter at row 4 → creates cols 1, 3 (2 timelines)
        - Col 4 passes through (no splitter) → 1 timeline
        Total: 3 timelines
        
        Expected: 3 timelines
        """
        input_text = """...S...
.......
...^...
.......
..^....
......."""
        
        data = parse_input(input_text)
        result = solve_part2(data)
        self.assertEqual(result, 3, "Asymmetric branching should count correctly")
    
    def test_wide_spread_timelines(self):
        """Test Part 2 with timelines spreading wider than grid.
        
        Configuration:
        .S.  <- Grid is only 3 columns wide
        ...
        .^.
        ...
        .^.
        ...
        
        Col 1 → split to 0, 2
        Col 0 → split to -1, 1 (col -1 is out of bounds but still counts)
        Col 2 → split to 1, 3 (col 3 is out of bounds but still counts)
        Total: 4 timelines (cols -1, 1, 1, 3)
        
        Expected: 4 timelines
        """
        input_text = """.S.
...
.^.
...
^.^
..."""
        
        data = parse_input(input_text)
        result = solve_part2(data)
        self.assertEqual(result, 4, "Timelines spreading beyond grid should count")
    
    def test_part1_vs_part2_difference(self):
        """Test demonstrating key difference between Part 1 and Part 2.
        
        Configuration:
        ...S...
        .......
        ...^...
        .......
        ..^.^..
        .......
        
        Part 1 (classical beams with merging):
        - Row 2: 1 split (col 3 → 2, 4)
        - Row 4: 2 splits (both hit) → creates cols 1, 3, 3, 5
        - Beams at col 3 MERGE → final beams: 1, 3, 5 (3 beams)
        - Total splits: 3
        
        Part 2 (quantum timelines without merging):
        - Row 2: Timeline splits (col 3 → 2, 4)
        - Row 4: Both timelines hit splitters
          - Col 2 → creates cols 1, 3
          - Col 4 → creates cols 3, 5
        - Timelines at col 3 DO NOT MERGE → 4 distinct timelines
        - Total timelines: 4
        
        This test verifies the fundamental difference.
        """
        input_text = """...S...
.......
...^...
.......
..^.^..
......."""
        
        data = parse_input(input_text)
        
        # Part 1 should give 3 splits
        part1_result = solve_part1(data)
        self.assertEqual(part1_result, 3, "Part 1 should count 3 splits")
        
        # Part 2 should give 4 timelines
        part2_result = solve_part2(data)
        self.assertEqual(part2_result, 4, "Part 2 should count 4 timelines (no merging)")


class TestDay07EdgeCases(unittest.TestCase):
    """Additional edge case tests for robustness."""
    
    def test_wide_grid_single_beam(self):
        """Test with very wide grid but single central beam path."""
        input_text = """.......................S.......................
...............................................
.......................^.......................
..............................................."""
        
        data = parse_input(input_text)
        result = solve_part1(data)
        self.assertEqual(result, 1, "Wide grid with single splitter should produce 1 split")
    
    def test_narrow_grid(self):
        """Test with minimal width grid (3 columns)."""
        input_text = """.S.
...
.^.
..."""
        
        data = parse_input(input_text)
        result = solve_part1(data)
        self.assertEqual(result, 1, "Narrow grid should work correctly")
    
    def test_multiple_splitters_same_row(self):
        """Test with multiple splitters on same row, various positions."""
        input_text = """...S...
.......
.^.^.^.
......."""
        
        data = parse_input(input_text)
        result = solve_part1(data)
        # Beam at col 3 hits splitter at col 3 (middle one)
        self.assertEqual(result, 1, "Should hit the splitter directly below start")
    
    def test_beam_splits_then_merges_then_splits_again(self):
        """Test multiple rounds of splitting and merging."""
        input_text = """.....S.....
...........
.....^.....
...........
....^.^....
...........
...^...^...
..........."""
        
        data = parse_input(input_text)
        result = solve_part1(data)
        # Row 2: 1 split (col 5 -> 4,6)
        # Row 4: 2 splits (both hit)
        # Row 6: 2 splits (cols 3 and 7)
        # Total: 5 splits
        self.assertEqual(result, 5, "Multiple rounds of split-merge-split should work")
    
    def test_maximum_edge_splits(self):
        """Test where every split sends beams to both edges."""
        input_text = """...S...
.......
...^...
.......
..^.^..
.......
.^...^.
......."""
        
        data = parse_input(input_text)
        result = solve_part1(data)
        # Row 2: 1 split (col 3 -> 2,4)
        # Row 4: 2 splits (cols 2,4 hit)
        # Row 6: 2 splits (cols 1,5 hit) -> creates 0,2,4,6
        # Total: 5 splits
        self.assertEqual(result, 5, "Cascading edge splits should count correctly")


if __name__ == '__main__':
    unittest.main()
