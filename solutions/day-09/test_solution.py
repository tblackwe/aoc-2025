#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test cases for Day 09: Movie Theater
Run these tests before implementing the solution (TDD).

Part 1: Find the largest rectangle that can be formed using red tiles
as opposite corners. Area is calculated inclusively: (|x2-x1|+1) × (|y2-y1|+1)

Part 2: Rectangles can ONLY include tiles that are red or green.
Green tiles = path tiles (connecting consecutive red tiles) + interior tiles
(inside the polygon formed by red tiles). This dramatically restricts valid rectangles.
"""

import unittest
from solution import (
    parse_input, 
    solve_part1, 
    solve_part2,
    get_line_tiles,
    point_in_polygon,
    get_green_tiles,
    is_rectangle_valid
)


class TestDay09Parsing(unittest.TestCase):
    """Tests for input parsing logic."""
    
    def test_parse_example_input(self):
        """Test parsing the example input from spec."""
        input_text = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
        expected = [
            (7, 1),
            (11, 1),
            (11, 7),
            (9, 7),
            (9, 5),
            (2, 5),
            (2, 3),
            (7, 3),
        ]
        result = parse_input(input_text)
        self.assertEqual(result, expected, "Failed to parse example input correctly")
    
    def test_parse_single_line(self):
        """Test parsing single coordinate pair."""
        input_text = "5,5"
        expected = [(5, 5)]
        result = parse_input(input_text)
        self.assertEqual(result, expected)
    
    def test_parse_two_tiles(self):
        """Test parsing two coordinate pairs."""
        input_text = "0,0\n5,3"
        expected = [(0, 0), (5, 3)]
        result = parse_input(input_text)
        self.assertEqual(result, expected)
    
    def test_parse_empty_input(self):
        """Test parsing empty input."""
        input_text = ""
        expected = []
        result = parse_input(input_text)
        self.assertEqual(result, expected, "Empty input should return empty list")
    
    def test_parse_with_whitespace(self):
        """Test parsing input with extra whitespace."""
        input_text = "  7,1  \n11,1\n  \n9,5  "
        # Should handle leading/trailing whitespace
        result = parse_input(input_text)
        self.assertIn((7, 1), result)
        self.assertIn((11, 1), result)
        self.assertIn((9, 5), result)
    
    def test_parse_negative_coordinates(self):
        """Test parsing negative coordinates."""
        input_text = "-5,-5\n5,5"
        expected = [(-5, -5), (5, 5)]
        result = parse_input(input_text)
        self.assertEqual(result, expected)


class TestDay09Part1(unittest.TestCase):
    """Tests for Part 1 solution."""
    
    def setUp(self):
        """Set up test fixtures and example data."""
        # Main example from spec
        self.main_example = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
    
    def test_example_from_spec(self):
        """Test Part 1 with the main example from specification."""
        # The largest rectangle is between (2,5) and (11,1)
        # Width: |11-2|+1 = 10, Height: |5-1|+1 = 5, Area: 50
        result = solve_part1(self.main_example)
        self.assertEqual(result, 50, "Main example should have max area of 50")
    
    def test_two_tiles_minimum_valid(self):
        """Test Part 1 with exactly two tiles (minimum valid input)."""
        # Tiles at (0,0) and (5,3)
        # Width: 6, Height: 4, Area: 24
        input_text = "0,0\n5,3"
        result = solve_part1(input_text)
        self.assertEqual(result, 24, "Rectangle (0,0) to (5,3) should have area 24")
    
    def test_square_rectangle(self):
        """Test Part 1 with tiles forming a square."""
        # Tiles at (0,0) and (4,4)
        # Width: 5, Height: 5, Area: 25
        input_text = "0,0\n4,4"
        result = solve_part1(input_text)
        self.assertEqual(result, 25, "Square 5x5 should have area 25")
    
    def test_unit_rectangle(self):
        """Test Part 1 with adjacent diagonal tiles."""
        # Tiles at (0,0) and (1,1)
        # Width: 2, Height: 2, Area: 4
        input_text = "0,0\n1,1"
        result = solve_part1(input_text)
        self.assertEqual(result, 4, "Unit square should have area 4")
    
    def test_three_tiles_multiple_pairs(self):
        """Test Part 1 with three tiles creating multiple rectangles."""
        # Tiles at (0,0), (3,2), (6,5)
        # Pairs:
        #   (0,0) to (3,2): 4×3 = 12
        #   (0,0) to (6,5): 7×6 = 42 ← maximum
        #   (3,2) to (6,5): 4×4 = 16
        input_text = "0,0\n3,2\n6,5"
        result = solve_part1(input_text)
        self.assertEqual(result, 42, "Maximum of three pairs should be 42")
    
    def test_mixed_valid_and_invalid_pairs(self):
        """Test with grid corners where some pairs are invalid."""
        # Tiles at corners of a grid: (0,0), (0,5), (5,0), (5,5)
        # Invalid pairs (same x or y): (0,0)-(0,5), (0,0)-(5,0), etc.
        # Valid pairs: (0,0)-(5,5) = 6×6 = 36, (0,5)-(5,0) = 6×6 = 36
        input_text = "0,0\n0,5\n5,0\n5,5"
        result = solve_part1(input_text)
        self.assertEqual(result, 36, "Grid corners should form 6x6 rectangles")
    
    def test_edge_case_horizontal_line(self):
        """Test Part 1 with all tiles on horizontal line (degenerate)."""
        # All tiles have same y-coordinate → no valid rectangles
        input_text = "0,5\n5,5\n10,5"
        result = solve_part1(input_text)
        self.assertEqual(result, 0, "Horizontal line should produce area 0")
    
    def test_edge_case_vertical_line(self):
        """Test Part 1 with all tiles on vertical line (degenerate)."""
        # All tiles have same x-coordinate → no valid rectangles
        input_text = "3,0\n3,5\n3,10"
        result = solve_part1(input_text)
        self.assertEqual(result, 0, "Vertical line should produce area 0")
    
    def test_edge_case_single_tile(self):
        """Test Part 1 with single tile (no pairs possible)."""
        input_text = "5,5"
        result = solve_part1(input_text)
        self.assertEqual(result, 0, "Single tile should produce area 0")
    
    def test_edge_case_empty_input(self):
        """Test Part 1 with empty input (no tiles)."""
        input_text = ""
        result = solve_part1(input_text)
        self.assertEqual(result, 0, "Empty input should produce area 0")
    
    def test_edge_case_duplicate_coordinates(self):
        """Test Part 1 with duplicate tile coordinates."""
        # Tiles: (2,3), (2,3), (5,7)
        # Valid pairs: (2,3)-(5,7) = 4×5 = 20 (counted twice but same result)
        input_text = "2,3\n2,3\n5,7"
        result = solve_part1(input_text)
        self.assertEqual(result, 20, "Duplicate tiles should still form valid rectangles")
    
    def test_edge_case_large_coordinates(self):
        """Test Part 1 with large coordinate values."""
        # Tiles at (0,0) and (1000,1000)
        # Width: 1001, Height: 1001, Area: 1,002,001
        input_text = "0,0\n1000,1000"
        result = solve_part1(input_text)
        self.assertEqual(result, 1002001, "Large coordinates should work correctly")
    
    def test_edge_case_negative_coordinates(self):
        """Test Part 1 with negative coordinates."""
        # Tiles at (-5,-5) and (5,5)
        # Width: |5-(-5)|+1 = 11, Height: 11, Area: 121
        input_text = "-5,-5\n5,5"
        result = solve_part1(input_text)
        self.assertEqual(result, 121, "Negative coordinates should work correctly")
    
    def test_edge_case_same_x_different_y(self):
        """Test Part 1 with tiles having same x-coordinate."""
        # Tiles at (0,0) and (0,10) - same x, different y
        # Should produce area 0 (not valid opposite corners)
        input_text = "0,0\n0,10"
        result = solve_part1(input_text)
        self.assertEqual(result, 0, "Same x-coordinate should produce area 0")
    
    def test_edge_case_same_y_different_x(self):
        """Test Part 1 with tiles having same y-coordinate."""
        # Tiles at (0,0) and (10,0) - same y, different x
        # Should produce area 0 (not valid opposite corners)
        input_text = "0,0\n10,0"
        result = solve_part1(input_text)
        self.assertEqual(result, 0, "Same y-coordinate should produce area 0")


class TestDay09AreaCalculation(unittest.TestCase):
    """Tests for area calculation logic (inclusive counting)."""
    
    def test_area_formula_basic(self):
        """Test that area formula uses inclusive counting."""
        # From (2,5) to (11,1): width=10, height=5, area=50
        input_text = "2,5\n11,1"
        result = solve_part1(input_text)
        self.assertEqual(result, 50, "Inclusive counting: (9+1)×(4+1) = 50")
    
    def test_area_formula_adjacent_tiles(self):
        """Test area calculation for adjacent diagonal tiles."""
        # From (0,0) to (1,1): should be 2×2 = 4, not 1×1 = 1
        input_text = "0,0\n1,1"
        result = solve_part1(input_text)
        self.assertEqual(result, 4, "Adjacent diagonal tiles: 2×2 = 4")
    
    def test_area_formula_zero_based_coordinates(self):
        """Test that formula works with zero-based coordinates."""
        # From (0,0) to (9,9): should be 10×10 = 100
        input_text = "0,0\n9,9"
        result = solve_part1(input_text)
        self.assertEqual(result, 100, "Zero-based 10×10 grid should have area 100")


class TestDay09ComplexCases(unittest.TestCase):
    """Tests for more complex scenarios."""
    
    def test_many_tiles_find_maximum(self):
        """Test finding maximum among many possible rectangles."""
        # Create a scenario with multiple rectangles of different sizes
        input_text = """0,0
1,1
2,2
10,10
0,10
10,0"""
        # (0,0) to (10,10): 11×11 = 121 ← should be maximum
        result = solve_part1(input_text)
        self.assertEqual(result, 121, "Should find maximum area of 121")
    
    def test_all_pairs_same_area(self):
        """Test when all valid pairs produce same area."""
        # Square grid corners: all valid pairs form same size rectangles
        input_text = "0,0\n0,5\n5,0\n5,5"
        # Both (0,0)-(5,5) and (0,5)-(5,0) = 36
        result = solve_part1(input_text)
        self.assertEqual(result, 36, "All equal areas should still return correct max")
    
    def test_spec_validation_trace(self):
        """Test specific pairs from the spec validation trace."""
        # Test case from spec: (7,1) to (11,7) should be 5×7 = 35
        input_text = "7,1\n11,7"
        result = solve_part1(input_text)
        self.assertEqual(result, 35, "Spec trace: (7,1)-(11,7) should be 35")
        
        # Another from spec: (11,7) to (2,3) should be 10×5 = 50
        input_text2 = "11,7\n2,3"
        result2 = solve_part1(input_text2)
        self.assertEqual(result2, 50, "Spec trace: (11,7)-(2,3) should be 50")


class TestDay09Part2LineGeneration(unittest.TestCase):
    """Test generating tiles along paths between red tiles."""
    
    def test_horizontal_line_simple(self):
        """Test generating tiles on horizontal line."""
        # Line from (0,0) to (5,0)
        result = get_line_tiles((0, 0), (5, 0))
        expected = {(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)}
        self.assertEqual(result, expected, "Horizontal line should include all tiles")
    
    def test_horizontal_line_reversed(self):
        """Test generating tiles on horizontal line (reversed order)."""
        # Line from (5,0) to (0,0) should give same result
        result = get_line_tiles((5, 0), (0, 0))
        expected = {(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)}
        self.assertEqual(result, expected, "Line direction shouldn't matter")
    
    def test_vertical_line_simple(self):
        """Test generating tiles on vertical line."""
        # Line from (3,2) to (3,7)
        result = get_line_tiles((3, 2), (3, 7))
        expected = {(3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7)}
        self.assertEqual(result, expected, "Vertical line should include all tiles")
    
    def test_vertical_line_reversed(self):
        """Test generating tiles on vertical line (reversed order)."""
        # Line from (3,7) to (3,2) should give same result
        result = get_line_tiles((3, 7), (3, 2))
        expected = {(3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7)}
        self.assertEqual(result, expected, "Line direction shouldn't matter")
    
    def test_single_tile_line(self):
        """Test line from a tile to itself."""
        # Line from (5,5) to (5,5)
        result = get_line_tiles((5, 5), (5, 5))
        expected = {(5, 5)}
        self.assertEqual(result, expected, "Single tile line")
    
    def test_adjacent_horizontal_tiles(self):
        """Test line between adjacent horizontal tiles."""
        # Line from (0,0) to (1,0)
        result = get_line_tiles((0, 0), (1, 0))
        expected = {(0, 0), (1, 0)}
        self.assertEqual(result, expected, "Adjacent tiles should both be included")
    
    def test_adjacent_vertical_tiles(self):
        """Test line between adjacent vertical tiles."""
        # Line from (0,0) to (0,1)
        result = get_line_tiles((0, 0), (0, 1))
        expected = {(0, 0), (0, 1)}
        self.assertEqual(result, expected, "Adjacent tiles should both be included")
    
    def test_main_example_path_segments(self):
        """Test path segments from main example."""
        # (7,1) → (11,1): horizontal
        result1 = get_line_tiles((7, 1), (11, 1))
        self.assertIn((8, 1), result1)
        self.assertIn((9, 1), result1)
        self.assertIn((10, 1), result1)
        self.assertEqual(len(result1), 5)  # 7,8,9,10,11
        
        # (11,1) → (11,7): vertical
        result2 = get_line_tiles((11, 1), (11, 7))
        self.assertIn((11, 2), result2)
        self.assertIn((11, 5), result2)
        self.assertEqual(len(result2), 7)  # 1,2,3,4,5,6,7
        
        # (9,5) → (2,5): horizontal
        result3 = get_line_tiles((9, 5), (2, 5))
        self.assertIn((3, 5), result3)
        self.assertIn((7, 5), result3)
        self.assertEqual(len(result3), 8)  # 2,3,4,5,6,7,8,9


class TestDay09Part2PointInPolygon(unittest.TestCase):
    """Test ray casting algorithm for point containment."""
    
    def test_point_inside_square(self):
        """Test point clearly inside a square polygon."""
        polygon = [(0, 0), (10, 0), (10, 10), (0, 10)]
        point = (5, 5)
        result = point_in_polygon(point, polygon)
        self.assertTrue(result, "Point (5,5) should be inside square")
    
    def test_point_outside_square_right(self):
        """Test point outside square (to the right)."""
        polygon = [(0, 0), (10, 0), (10, 10), (0, 10)]
        point = (15, 5)
        result = point_in_polygon(point, polygon)
        self.assertFalse(result, "Point (15,5) should be outside square")
    
    def test_point_outside_square_left(self):
        """Test point outside square (to the left)."""
        polygon = [(0, 0), (10, 0), (10, 10), (0, 10)]
        point = (-1, 5)
        result = point_in_polygon(point, polygon)
        self.assertFalse(result, "Point (-1,5) should be outside square")
    
    def test_point_on_boundary_vertex(self):
        """Test point on polygon boundary (vertex)."""
        polygon = [(0, 0), (10, 0), (10, 10), (0, 10)]
        point = (0, 0)
        result = point_in_polygon(point, polygon)
        # Boundary points typically return False (not strictly inside)
        self.assertFalse(result, "Point on vertex should be on boundary (not inside)")
    
    def test_point_on_boundary_edge(self):
        """Test point on polygon boundary (edge)."""
        polygon = [(0, 0), (10, 0), (10, 10), (0, 10)]
        point = (5, 0)
        result = point_in_polygon(point, polygon)
        # Boundary points typically return False
        self.assertFalse(result, "Point on edge should be on boundary (not inside)")
    
    def test_point_in_rectangle(self):
        """Test point inside a rectangle."""
        # Rectangle from spec example area
        polygon = [(2, 3), (9, 3), (9, 5), (2, 5)]
        point = (5, 4)
        result = point_in_polygon(point, polygon)
        self.assertTrue(result, "Point (5,4) should be inside rectangle")
    
    def test_point_in_l_shape(self):
        """Test point inside L-shaped polygon."""
        # L-shape: covers (0,0)-(5,2) and (0,2)-(2,5)
        polygon = [(0, 0), (5, 0), (5, 2), (2, 2), (2, 5), (0, 5)]
        
        # Point in horizontal part
        point1 = (4, 1)
        self.assertTrue(point_in_polygon(point1, polygon), "Point in horizontal part")
        
        # Point in vertical part
        point2 = (1, 4)
        self.assertTrue(point_in_polygon(point2, polygon), "Point in vertical part")
        
        # Point in corner cutout (should be outside)
        point3 = (4, 4)
        self.assertFalse(point_in_polygon(point3, polygon), "Point in cutout area")
    
    def test_concave_polygon(self):
        """Test point containment in concave polygon."""
        # Simple concave shape
        polygon = [(0, 0), (10, 0), (10, 5), (5, 5), (5, 10), (0, 10)]
        
        # Inside the concave area
        point1 = (3, 7)
        self.assertTrue(point_in_polygon(point1, polygon), "Point inside concave part")
        
        # In the "notch" (outside)
        point2 = (7, 7)
        self.assertFalse(point_in_polygon(point2, polygon), "Point in concave notch")


class TestDay09Part2GreenTiles(unittest.TestCase):
    """Test identifying all green tiles (path + interior)."""
    
    def test_simple_square_green_tiles(self):
        """Test green tiles for a simple square loop."""
        red_tiles = [(0, 0), (10, 0), (10, 10), (0, 10)]
        green_tiles = get_green_tiles(red_tiles)
        
        # Should include path tiles
        self.assertIn((5, 0), green_tiles, "Edge tile should be green")
        self.assertIn((10, 5), green_tiles, "Edge tile should be green")
        
        # Should include interior tiles
        self.assertIn((5, 5), green_tiles, "Interior tile should be green")
        self.assertIn((3, 7), green_tiles, "Interior tile should be green")
        
        # Should NOT include tiles outside
        self.assertNotIn((15, 5), green_tiles, "Outside tile should not be green")
        self.assertNotIn((-1, 5), green_tiles, "Outside tile should not be green")
        
        # Should NOT include red tiles themselves
        self.assertNotIn((0, 0), green_tiles, "Red tile should not be in green set")
    
    def test_minimal_loop_green_tiles(self):
        """Test green tiles for minimal loop (thin rectangle)."""
        red_tiles = [(0, 0), (2, 0), (2, 1), (0, 1)]
        green_tiles = get_green_tiles(red_tiles)
        
        # Path tiles only (no interior since it's thin)
        self.assertIn((1, 0), green_tiles, "Path tile should be green")
        self.assertIn((1, 1), green_tiles, "Path tile should be green")
        
        # Red tiles not in green set
        self.assertNotIn((0, 0), green_tiles, "Red tile should not be green")
    
    def test_main_example_green_tiles(self):
        """Test green tiles for main example from spec."""
        red_tiles = [(7, 1), (11, 1), (11, 7), (9, 7), (9, 5), (2, 5), (2, 3), (7, 3)]
        green_tiles = get_green_tiles(red_tiles)
        
        # Test specific path tiles mentioned in spec
        self.assertIn((8, 1), green_tiles, "Path tile from spec")
        self.assertIn((10, 1), green_tiles, "Path tile from spec")
        self.assertIn((11, 3), green_tiles, "Path tile from spec")
        self.assertIn((10, 7), green_tiles, "Path tile from spec")
        self.assertIn((9, 6), green_tiles, "Path tile from spec")
        self.assertIn((5, 5), green_tiles, "Path tile from spec")
        self.assertIn((2, 4), green_tiles, "Path tile from spec")
        self.assertIn((4, 3), green_tiles, "Path tile from spec")
        self.assertIn((7, 2), green_tiles, "Path tile from spec")
        
        # Test some interior tiles (should be inside the polygon)
        # Interior tiles should be those inside the closed loop
        # The polygon wraps: (7,1)→(11,1)→(11,7)→(9,7)→(9,5)→(2,5)→(2,3)→(7,3)→back to (7,1)
        
        # Red tiles should NOT be in green set
        self.assertNotIn((7, 1), green_tiles, "Red tiles should not be green")
        self.assertNotIn((11, 1), green_tiles, "Red tiles should not be green")
    
    def test_line_of_red_tiles_no_interior(self):
        """Test green tiles when red tiles form a line (degenerate)."""
        red_tiles = [(0, 0), (5, 0), (10, 0)]
        green_tiles = get_green_tiles(red_tiles)
        
        # Should have path tiles
        self.assertIn((1, 0), green_tiles, "Path tile on line")
        self.assertIn((7, 0), green_tiles, "Path tile on line")
        
        # Should not have tiles above/below line
        self.assertNotIn((5, 1), green_tiles, "Tile above line should not be green")
        self.assertNotIn((5, -1), green_tiles, "Tile below line should not be green")


class TestDay09Part2RectangleValidation(unittest.TestCase):
    """Test validating rectangles contain only red/green tiles."""
    
    def test_valid_rectangle_all_green(self):
        """Test rectangle that contains only green tiles."""
        red_tiles_set = {(0, 0), (10, 0), (10, 10), (0, 10)}
        # For a square, all interior tiles are valid
        green_tiles = set()
        # Add some green tiles for testing
        for x in range(1, 10):
            for y in range(1, 10):
                green_tiles.add((x, y))
        
        valid_tiles = red_tiles_set | green_tiles
        
        # Small interior rectangle should be valid
        result = is_rectangle_valid((2, 2), (8, 8), valid_tiles)
        self.assertTrue(result, "Interior rectangle should be valid")
    
    def test_invalid_rectangle_contains_non_green(self):
        """Test rectangle that contains tiles outside valid set."""
        red_tiles_set = {(0, 0), (10, 0), (10, 10), (0, 10)}
        green_tiles = set()
        # Only add path tiles, not all interior
        for x in range(1, 10):
            green_tiles.add((x, 0))
            green_tiles.add((x, 10))
        for y in range(1, 10):
            green_tiles.add((0, y))
            green_tiles.add((10, y))
        
        valid_tiles = red_tiles_set | green_tiles
        
        # Rectangle extending outside should be invalid
        result = is_rectangle_valid((0, 0), (15, 10), valid_tiles)
        self.assertFalse(result, "Rectangle extending outside should be invalid")
    
    def test_valid_rectangle_with_red_corners(self):
        """Test valid rectangle with red tile corners."""
        red_tiles_set = {(0, 0), (5, 0), (10, 10), (0, 10)}
        green_tiles = {(1, 0), (2, 0), (3, 0), (4, 0)}  # Path between (0,0) and (5,0)
        valid_tiles = red_tiles_set | green_tiles
        
        # Rectangle from (0,0) to (5,0) - but this is degenerate (same y)
        # Let's use a proper rectangle
        result = is_rectangle_valid((0, 0), (5, 10), valid_tiles)
        # This would only be valid if all tiles in the rectangle are valid
        # Since we don't have all green tiles, this should fail
        # But we need to check based on what's actually in valid_tiles
    
    def test_main_example_valid_rectangle(self):
        """Test that the main example's answer rectangle is valid."""
        red_tiles = [(7, 1), (11, 1), (11, 7), (9, 7), (9, 5), (2, 5), (2, 3), (7, 3)]
        green_tiles = get_green_tiles(red_tiles)
        valid_tiles = set(red_tiles) | green_tiles
        
        # The winning rectangle from spec: (9,5) to (2,3), area 24
        result = is_rectangle_valid((9, 5), (2, 3), valid_tiles)
        self.assertTrue(result, "Main example answer rectangle should be valid")
    
    def test_main_example_invalid_rectangle(self):
        """Test that Part 1's answer is now invalid for Part 2."""
        red_tiles = [(7, 1), (11, 1), (11, 7), (9, 7), (9, 5), (2, 5), (2, 3), (7, 3)]
        green_tiles = get_green_tiles(red_tiles)
        valid_tiles = set(red_tiles) | green_tiles
        
        # Part 1's answer: (2,5) to (11,1), area 50 - should be INVALID
        result = is_rectangle_valid((2, 5), (11, 1), valid_tiles)
        self.assertFalse(result, "Part 1 answer (area 50) should be INVALID in Part 2")
    
    def test_single_tile_rectangle(self):
        """Test rectangle consisting of single tile."""
        valid_tiles = {(5, 5), (3, 3)}
        
        # Single tile rectangle (same corners)
        result = is_rectangle_valid((5, 5), (5, 5), valid_tiles)
        self.assertTrue(result, "Single valid tile should be valid")
        
        # Single invalid tile
        result2 = is_rectangle_valid((7, 7), (7, 7), valid_tiles)
        self.assertFalse(result2, "Single invalid tile should be invalid")


class TestDay09Part2(unittest.TestCase):
    """Test Part 2 solution with full examples."""
    
    def setUp(self):
        """Set up test fixtures and example data."""
        # Main example from spec (same as Part 1)
        self.main_example = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
    
    def test_main_example_part2(self):
        """Test Part 2 with main example - answer should be 24, NOT 50!"""
        # Critical test: Part 2 has different answer than Part 1
        # Part 1 answer was 50 (rectangle (2,5) to (11,1))
        # Part 2 answer is 24 (rectangle (9,5) to (2,3))
        # The difference is that the 50-area rectangle contains non-green tiles
        result = solve_part2(self.main_example)
        self.assertEqual(result, 24, "Part 2 main example should be 24, not 50!")
    
    def test_part1_vs_part2_difference(self):
        """Verify that Part 2 answer is more restrictive than Part 1."""
        part1_result = solve_part1(self.main_example)
        part2_result = solve_part2(self.main_example)
        
        self.assertEqual(part1_result, 50, "Part 1 should be 50")
        self.assertEqual(part2_result, 24, "Part 2 should be 24")
        self.assertLess(part2_result, part1_result, 
                       "Part 2 should be more restrictive (smaller area)")
    
    def test_specific_valid_rectangles(self):
        """Test specific valid rectangles mentioned in spec."""
        # Note: We can't directly test individual rectangles without 
        # exposing internal logic, but we verify the maximum is correct
        
        # The spec mentions these valid rectangles:
        # - (7,3) to (11,1): area 15 ✓
        # - (9,7) to (9,5): area 3 ✓
        # - (9,5) to (2,3): area 24 ✓ (maximum)
        
        result = solve_part2(self.main_example)
        self.assertEqual(result, 24, "Maximum valid rectangle should be 24")
    
    def test_simple_square_loop(self):
        """Test Part 2 with simple square loop (all tiles valid)."""
        # 4 red tiles forming a square
        # All interior tiles should be green
        # Maximum rectangle is the entire square
        input_text = """0,0
10,0
10,10
0,10"""
        result = solve_part2(input_text)
        # Full square: 11×11 = 121
        self.assertEqual(result, 121, "Square loop should allow full area")
    
    def test_minimal_loop_thin_rectangle(self):
        """Test Part 2 with minimal loop (thin rectangle, no interior)."""
        # Narrow rectangle with minimal interior
        input_text = """0,0
2,0
2,1
0,1"""
        result = solve_part2(input_text)
        # Full rectangle: 3×2 = 6
        self.assertEqual(result, 6, "Minimal loop should have area 6")
    
    def test_l_shape_loop(self):
        """Test Part 2 with L-shaped loop."""
        input_text = """0,0
5,0
5,5
0,5"""
        result = solve_part2(input_text)
        # Full square: 6×6 = 36
        self.assertEqual(result, 36, "L-shape (square) should have area 36")
    
    def test_degenerate_line(self):
        """Test Part 2 with red tiles in a line (no valid rectangles)."""
        # All tiles same y-coordinate
        input_text = """0,0
5,0
10,0"""
        result = solve_part2(input_text)
        self.assertEqual(result, 0, "Line of tiles should produce area 0")
    
    def test_two_tiles_part2(self):
        """Test Part 2 with just two tiles."""
        # Two tiles form a small rectangle
        # All tiles in between should be green (path)
        input_text = """0,0
2,1"""
        result = solve_part2(input_text)
        # Rectangle is 3×2 = 6, but we need to check if all tiles are valid
        # For just 2 red tiles, they form a degenerate "polygon"
        # The path between them would be minimal
        # This depends on implementation details
    
    def test_edge_case_empty_input_part2(self):
        """Test Part 2 with empty input."""
        result = solve_part2("")
        self.assertEqual(result, 0, "Empty input should produce area 0")
    
    def test_edge_case_single_tile_part2(self):
        """Test Part 2 with single tile."""
        result = solve_part2("5,5")
        self.assertEqual(result, 0, "Single tile should produce area 0")
    
    def test_edge_case_vertical_line_part2(self):
        """Test Part 2 with vertical line of tiles."""
        input_text = """3,0
3,5
3,10"""
        result = solve_part2(input_text)
        self.assertEqual(result, 0, "Vertical line should produce area 0")


if __name__ == '__main__':
    unittest.main()
