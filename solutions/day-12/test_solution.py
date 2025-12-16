#!/usr/bin/env python3
"""
Test cases for Day 12: Christmas Tree Farm solution.
Run these tests before implementing the solution (TDD).

This puzzle involves 2D bin packing with polyominoes:
- Parse present shapes from ASCII art
- Parse region specifications
- Determine if all required presents fit in each region
- Presents can be rotated and flipped
- Empty spaces (.) in shapes don't block other presents

Functions that need to be implemented in solution.py:
- parse_input(text) -> Tuple[List[Shape], List[Region]]
- solve_part1(data) -> int
- get_all_orientations(shape) -> List[Shape]
- normalize_shape(shape) -> Shape  
- can_place_shape(grid, shape, row, col, width, height) -> bool
- rotate_90(shape) -> Shape
- flip_horizontal(shape) -> Shape
- solve_region(shapes, region) -> bool
"""

import unittest
import sys


class TestDay12Parsing(unittest.TestCase):
    """Tests for input parsing logic."""
    
    def test_parse_single_shape_simple(self):
        """Test parsing a simple single shape."""
        from solution import parse_input
        
        input_text = """0:
###
#.#
#.#
"""
        shapes, regions = parse_input(input_text)
        
        # Shape 0 should have # cells at positions (0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,2)
        self.assertEqual(len(shapes), 1)
        expected_cells = {(0,0), (0,1), (0,2), (1,0), (1,2), (2,0), (2,2)}
        self.assertEqual(set(shapes[0]), expected_cells)
        self.assertEqual(len(regions), 0)
    
    def test_parse_multiple_shapes(self):
        """Test parsing multiple shapes from input."""
        from solution import parse_input
        
        input_text = """0:
###

1:
#.
##
"""
        shapes, regions = parse_input(input_text)
        
        self.assertEqual(len(shapes), 2)
        # Shape 0: three cells in a row
        self.assertEqual(set(shapes[0]), {(0,0), (0,1), (0,2)})
        # Shape 1: L-shape
        self.assertEqual(set(shapes[1]), {(0,0), (1,0), (1,1)})
    
    def test_parse_shape_with_empty_spaces(self):
        """Test that . characters are correctly ignored in shapes."""
        from solution import parse_input
        
        input_text = """0:
#..
##.
.##
"""
        shapes, regions = parse_input(input_text)
        
        # Only # characters should be in the shape
        expected = {(0,0), (1,0), (1,1), (2,1), (2,2)}
        self.assertEqual(set(shapes[0]), expected)
    
    def test_parse_single_region(self):
        """Test parsing a single region specification."""
        from solution import parse_input
        
        input_text = """0:
###

4x4: 0 0 0 0 2 0
"""
        shapes, regions = parse_input(input_text)
        
        self.assertEqual(len(regions), 1)
        region = regions[0]
        self.assertEqual(region['width'], 4)
        self.assertEqual(region['height'], 4)
        # Count of each shape: shape 4 appears twice
        self.assertEqual(region['required'], [0, 0, 0, 0, 2, 0])
    
    def test_parse_multiple_regions(self):
        """Test parsing multiple region specifications."""
        from solution import parse_input
        
        input_text = """0:
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
"""
        shapes, regions = parse_input(input_text)
        
        self.assertEqual(len(regions), 2)
        self.assertEqual(regions[0]['width'], 4)
        self.assertEqual(regions[0]['height'], 4)
        self.assertEqual(regions[1]['width'], 12)
        self.assertEqual(regions[1]['height'], 5)
    
    def test_parse_example_from_spec(self):
        """Test parsing the full example from the specification."""
        from solution import parse_input
        
        input_text = """0:
###
#.#
#.#

1:
#..
##.
.##

2:
##.
###
#.#

3:
..#
.##
###

4:
##.
##.
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""
        shapes, regions = parse_input(input_text)
        
        # Should have 6 shapes (indices 0-5)
        self.assertEqual(len(shapes), 6)
        
        # Should have 3 regions
        self.assertEqual(len(regions), 3)
        
        # Verify shape 4 structure
        # Shape 4 is:
        # ##.
        # ##.
        # ###
        expected_shape_4 = {(0,0), (0,1), (1,0), (1,1), (2,0), (2,1), (2,2)}
        self.assertEqual(set(shapes[4]), expected_shape_4)
    
    def test_parse_empty_input(self):
        """Test parsing empty input returns empty structures."""
        from solution import parse_input
        
        input_text = ""
        shapes, regions = parse_input(input_text)
        
        self.assertEqual(len(shapes), 0)
        self.assertEqual(len(regions), 0)


class TestDay12ShapeTransformations(unittest.TestCase):
    """Tests for shape rotation and flipping operations."""
    
    def test_rotate_90_simple(self):
        """Test 90-degree rotation of a simple shape."""
        from solution import rotate_90, normalize_shape
        
        # L-shape: 
        # #.
        # ##
        shape = [(0, 0), (1, 0), (1, 1)]
        rotated = rotate_90(shape)
        
        # After 90° clockwise rotation should become:
        # ##
        # #.
        normalized = normalize_shape(rotated)
        expected = {(0, 0), (0, 1), (1, 0)}
        self.assertEqual(set(normalized), expected)
    
    def test_rotate_90_four_times_identity(self):
        """Test that rotating 4 times returns to original shape."""
        from solution import rotate_90, normalize_shape
        
        shape = [(0, 0), (0, 1), (1, 0)]
        
        rotated = shape
        for _ in range(4):
            rotated = rotate_90(rotated)
        
        # After 4 rotations, should be back to original (when normalized)
        self.assertEqual(set(normalize_shape(rotated)), set(normalize_shape(shape)))
    
    def test_flip_horizontal_simple(self):
        """Test horizontal flip of a simple shape."""
        from solution import flip_horizontal, normalize_shape
        
        # L-shape:
        # #.
        # ##
        shape = [(0, 0), (1, 0), (1, 1)]
        flipped = flip_horizontal(shape)
        
        # After horizontal flip should become:
        # .#
        # ##
        normalized = normalize_shape(flipped)
        expected = {(0, 0), (1, 0), (1, 1)}  # Note: this is normalized
        self.assertEqual(set(normalized), expected)
    
    def test_flip_horizontal_twice_identity(self):
        """Test that flipping twice returns to original shape."""
        from solution import flip_horizontal, normalize_shape
        
        shape = [(0, 0), (0, 1), (0, 2)]
        
        flipped_once = flip_horizontal(shape)
        flipped_twice = flip_horizontal(flipped_once)
        
        # After 2 flips, should be back to original (when normalized)
        self.assertEqual(set(normalize_shape(flipped_twice)), set(normalize_shape(shape)))
    
    def test_normalize_shape_to_origin(self):
        """Test that normalization moves shape to start at (0,0)."""
        from solution import normalize_shape
        
        # Shape offset from origin
        shape = [(5, 3), (5, 4), (6, 3)]
        normalized = normalize_shape(shape)
        
        # Should start at (0, 0)
        coords = list(normalized)
        min_row = min(r for r, c in coords)
        min_col = min(c for r, c in coords)
        
        self.assertEqual(min_row, 0)
        self.assertEqual(min_col, 0)
    
    def test_get_all_orientations_simple(self):
        """Test generating all unique orientations of a shape."""
        from solution import get_all_orientations
        
        # Simple 2x1 rectangle
        shape = [(0, 0), (0, 1)]
        orientations = get_all_orientations(shape)
        
        # A 2x1 rectangle has 2 unique orientations (horizontal and vertical)
        # Even though there are 8 possible transforms, many are duplicates
        self.assertGreater(len(orientations), 0)
        self.assertLessEqual(len(orientations), 8)
        
        # All orientations should be normalized
        for orientation in orientations:
            coords = list(orientation)
            min_row = min(r for r, c in coords)
            min_col = min(c for r, c in coords)
            self.assertEqual(min_row, 0)
            self.assertEqual(min_col, 0)
    
    def test_get_all_orientations_symmetric_square(self):
        """Test that a fully symmetric shape has only 1 orientation."""
        from solution import get_all_orientations
        
        # 1x1 square
        shape = [(0, 0)]
        orientations = get_all_orientations(shape)
        
        # Should have only 1 unique orientation
        self.assertEqual(len(orientations), 1)
    
    def test_get_all_orientations_asymmetric(self):
        """Test that an asymmetric shape has multiple orientations."""
        from solution import get_all_orientations
        
        # L-shape (completely asymmetric)
        shape = [(0, 0), (1, 0), (1, 1)]
        orientations = get_all_orientations(shape)
        
        # L-shape should have 4 or 8 unique orientations
        # depending on implementation (rotations and flips)
        self.assertGreater(len(orientations), 1)


class TestDay12PlacementValidation(unittest.TestCase):
    """Tests for shape placement validation."""
    
    def test_can_place_shape_empty_grid(self):
        """Test placing a shape on an empty grid."""
        from solution import can_place_shape
        
        grid = set()
        shape = [(0, 0), (0, 1), (0, 2)]
        width, height = 5, 5
        
        # Should be able to place at origin
        self.assertTrue(can_place_shape(grid, shape, 0, 0, width, height))
    
    def test_can_place_shape_within_bounds(self):
        """Test that shapes must fit within grid boundaries."""
        from solution import can_place_shape
        
        grid = set()
        shape = [(0, 0), (0, 1), (0, 2)]  # 1x3 shape
        width, height = 4, 4
        
        # Can place at (0, 0) - fits
        self.assertTrue(can_place_shape(grid, shape, 0, 0, width, height))
        
        # Cannot place at (0, 2) - would go to column 4 (out of bounds)
        self.assertFalse(can_place_shape(grid, shape, 0, 2, width, height))
        
        # Cannot place at (0, 3) - definitely out of bounds
        self.assertFalse(can_place_shape(grid, shape, 0, 3, width, height))
    
    def test_can_place_shape_no_overlap(self):
        """Test that shapes cannot overlap with occupied cells."""
        from solution import can_place_shape
        
        # Grid with some cells occupied
        grid = {(0, 0), (0, 1), (1, 0)}
        shape = [(0, 0), (0, 1)]
        width, height = 5, 5
        
        # Cannot place at (0, 0) - overlaps
        self.assertFalse(can_place_shape(grid, shape, 0, 0, width, height))
        
        # Can place at (2, 2) - no overlap
        self.assertTrue(can_place_shape(grid, shape, 2, 2, width, height))
    
    def test_can_place_shape_adjacent_ok(self):
        """Test that shapes can be placed adjacent to each other."""
        from solution import can_place_shape
        
        grid = {(0, 0), (0, 1)}
        shape = [(0, 0), (0, 1)]
        width, height = 5, 5
        
        # Can place adjacent (not overlapping)
        self.assertTrue(can_place_shape(grid, shape, 0, 2, width, height))
        self.assertTrue(can_place_shape(grid, shape, 1, 0, width, height))
    
    def test_can_place_shape_edge_of_grid(self):
        """Test placing shapes at the edge of the grid."""
        from solution import can_place_shape
        
        grid = set()
        shape = [(0, 0), (1, 0)]  # 2x1 vertical
        width, height = 3, 3
        
        # Can place at bottom edge
        self.assertTrue(can_place_shape(grid, shape, 1, 0, width, height))
        
        # Cannot place at row 2 (would need rows 2 and 3)
        self.assertFalse(can_place_shape(grid, shape, 2, 0, width, height))
    
    def test_can_place_shape_single_cell(self):
        """Test placing a single cell shape."""
        from solution import can_place_shape
        
        grid = set()
        shape = [(0, 0)]
        width, height = 2, 2
        
        # Should be able to place at all positions
        for row in range(2):
            for col in range(2):
                self.assertTrue(can_place_shape(grid, shape, row, col, width, height))


class TestDay12Part1Examples(unittest.TestCase):
    """Tests for Part 1 solution with examples from spec."""
    
    def test_example_region_1_feasible(self):
        """Test Region 1 from spec: 4x4 with 2 copies of shape 4 - FEASIBLE."""
        from solution import parse_input, solve_region
        
        input_text = """0:
###
#.#
#.#

1:
#..
##.
.##

2:
##.
###
#.#

3:
..#
.##
###

4:
##.
##.
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
"""
        shapes, regions = parse_input(input_text)
        
        # For just region 1, should be feasible
        # We need a helper to test individual regions
        result = solve_region(shapes, regions[0])
        
        self.assertTrue(result, "Region 1 should be feasible (can fit 2 copies of shape 4)")
    
    def test_example_region_2_feasible(self):
        """Test Region 2 from spec: 12x5 with 6 presents - FEASIBLE."""
        from solution import parse_input, solve_region
        
        input_text = """0:
###
#.#
#.#

1:
#..
##.
.##

2:
##.
###
#.#

3:
..#
.##
###

4:
##.
##.
###

5:
###
.#.
###

12x5: 1 0 1 0 2 2
"""
        shapes, regions = parse_input(input_text)
        
        result = solve_region(shapes, regions[0])
        
        self.assertTrue(result, "Region 2 should be feasible")
    
    def test_example_region_3_not_feasible(self):
        """Test Region 3 from spec: 12x5 with 7 presents - NOT FEASIBLE."""
        from solution import parse_input, solve_region
        
        input_text = """0:
###
#.#
#.#

1:
#..
##.
.##

2:
##.
###
#.#

3:
..#
.##
###

4:
##.
##.
###

5:
###
.#.
###

12x5: 1 0 1 0 3 2
"""
        shapes, regions = parse_input(input_text)
        
        result = solve_region(shapes, regions[0])
        
        self.assertFalse(result, "Region 3 should NOT be feasible (too many presents)")
    
    def test_example_full_spec(self):
        """Test the complete example from specification - expect 2 feasible regions."""
        from solution import parse_input, solve_part1
        
        input_text = """0:
###
#.#
#.#

1:
#..
##.
.##

2:
##.
###
#.#

3:
..#
.##
###

4:
##.
##.
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""
        data = parse_input(input_text)
        result = solve_part1(data)
        
        self.assertEqual(result, 2, "Expected 2 out of 3 regions to be feasible")


class TestDay12Part1EdgeCases(unittest.TestCase):
    """Tests for edge cases in Part 1."""
    
    def test_empty_region_no_presents_required(self):
        """Test region that requires zero presents - should be feasible."""
        from solution import parse_input, solve_part1
        
        input_text = """0:
###

10x10: 0
"""
        data = parse_input(input_text)
        result = solve_part1(data)
        
        self.assertEqual(result, 1, "Region requiring no presents should be feasible")
    
    def test_single_cell_present_single_cell_region(self):
        """Test exact fit: 1x1 present in 1x1 region."""
        from solution import parse_input, solve_part1
        
        input_text = """0:
#

1x1: 1
"""
        data = parse_input(input_text)
        result = solve_part1(data)
        
        self.assertEqual(result, 1, "Single cell should fit in single cell region")
    
    def test_present_too_large_for_region(self):
        """Test present that is larger than region - not feasible."""
        from solution import parse_input, solve_part1
        
        input_text = """0:
###

2x2: 1
"""
        data = parse_input(input_text)
        result = solve_part1(data)
        
        self.assertEqual(result, 0, "3-cell shape cannot fit in 2x2 region")
    
    def test_area_constraint_too_many_presents(self):
        """Test that total present area exceeds region area."""
        from solution import parse_input, solve_part1
        
        input_text = """0:
###

3x3: 4
"""
        data = parse_input(input_text)
        result = solve_part1(data)
        
        # 4 copies of 3-cell shape = 12 cells, but region is only 3x3 = 9 cells
        self.assertEqual(result, 0, "Total present area exceeds region area")
    
    def test_multiple_regions_mixed_results(self):
        """Test multiple regions with some feasible and some not."""
        from solution import parse_input, solve_part1
        
        input_text = """0:
##

2x2: 1
4x4: 1
1x1: 1
"""
        data = parse_input(input_text)
        result = solve_part1(data)
        
        # Region 1 (2x2 with 1 2-cell shape): feasible
        # Region 2 (4x4 with 1 2-cell shape): feasible
        # Region 3 (1x1 with 1 2-cell shape): not feasible
        self.assertEqual(result, 2)
    
    def test_same_shape_multiple_copies_different_orientations(self):
        """Test placing multiple copies of same shape using different orientations."""
        from solution import parse_input, solve_part1
        
        input_text = """0:
##

2x2: 2
"""
        data = parse_input(input_text)
        result = solve_part1(data)
        
        # 2x2 region can fit two 2-cell shapes if oriented correctly
        # Horizontal at (0,0)-(0,1) and vertical at (0,1)-(1,1) would overlap
        # But horizontal at (0,0)-(0,1) and horizontal at (1,0)-(1,1) works
        self.assertEqual(result, 1, "Two 2-cell shapes should fit in 2x2 grid")
    
    def test_shape_rotation_required(self):
        """Test case where rotation is necessary to fit."""
        from solution import parse_input, solve_part1
        
        input_text = """0:
###

1x3: 1
3x1: 1
"""
        data = parse_input(input_text)
        result = solve_part1(data)
        
        # First region needs horizontal 3-cell: feasible
        # Second region needs vertical 3-cell (rotation): feasible
        self.assertEqual(result, 2)
    
    def test_complex_shape_placement(self):
        """Test with a more complex L-shaped piece."""
        from solution import parse_input, solve_part1
        
        input_text = """0:
#.
##

2x2: 1
"""
        data = parse_input(input_text)
        result = solve_part1(data)
        
        # L-shape with 3 cells should fit in 2x2 region
        self.assertEqual(result, 1)


class TestDay12Part1RealInput(unittest.TestCase):
    """Tests using the actual puzzle input."""
    
    def test_parse_real_input(self):
        """Test that real input parses correctly."""
        from solution import parse_input
        from pathlib import Path
        
        input_file = Path(__file__).parent / 'input.txt'
        
        if not input_file.exists():
            self.skipTest("input.txt not found")
        
        input_text = input_file.read_text()
        shapes, regions = parse_input(input_text)
        
        # Based on spec, should have 6 shapes (indices 0-5)
        self.assertEqual(len(shapes), 6)
        
        # Should have around 1000 regions
        self.assertGreater(len(regions), 900)
        self.assertLess(len(regions), 1100)
        
        # All regions should have counts for 6 shapes
        for region in regions:
            self.assertEqual(len(region['required']), 6)


if __name__ == '__main__':
    unittest.main()
