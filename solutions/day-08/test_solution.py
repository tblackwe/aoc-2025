#!/usr/bin/env python3
"""
Test cases for Day 08: Playground solution.
Run these tests BEFORE implementing the solution (TDD).

This test suite validates:
- Input parsing of 3D coordinates
- 3D Euclidean distance calculations
- Union-Find data structure operations
- Complete solution with example inputs
- Edge cases: small inputs, collinear points, equal distances
"""

import unittest
import math
from solution import parse_input, solve_part1, solve_part2


class TestDay08Parsing(unittest.TestCase):
    """Tests for input parsing logic."""
    
    def test_parse_example_input(self):
        """Test parsing the example input from spec (20 junction boxes)."""
        example_input = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""
        
        data = parse_input(example_input)
        
        # Should parse exactly 20 junction boxes
        self.assertEqual(len(data), 20, "Should parse 20 junction boxes")
        
        # First position should be (162, 817, 812)
        self.assertEqual(data[0], (162, 817, 812), "First box position incorrect")
        
        # Last position should be (425, 690, 689)
        self.assertEqual(data[19], (425, 690, 689), "Last box position incorrect")
        
        # Verify some middle positions
        self.assertEqual(data[5], (466, 668, 158), "Box at index 5 incorrect")
        self.assertEqual(data[10], (216, 146, 977), "Box at index 10 incorrect")
        
        # All positions should be tuples of 3 integers
        for i, pos in enumerate(data):
            self.assertIsInstance(pos, tuple, f"Position {i} should be a tuple")
            self.assertEqual(len(pos), 3, f"Position {i} should have 3 coordinates")
            self.assertIsInstance(pos[0], int, f"Position {i} X should be int")
            self.assertIsInstance(pos[1], int, f"Position {i} Y should be int")
            self.assertIsInstance(pos[2], int, f"Position {i} Z should be int")
    
    def test_parse_single_box(self):
        """Test parsing minimal single junction box."""
        single_input = "0,0,0"
        data = parse_input(single_input)
        
        self.assertEqual(len(data), 1, "Should parse 1 junction box")
        self.assertEqual(data[0], (0, 0, 0), "Single box at origin incorrect")
    
    def test_parse_simple_3_boxes(self):
        """Test parsing 3 boxes in a line."""
        simple_input = """0,0,0
1,0,0
10,0,0"""
        
        data = parse_input(simple_input)
        
        self.assertEqual(len(data), 3, "Should parse 3 junction boxes")
        self.assertEqual(data[0], (0, 0, 0))
        self.assertEqual(data[1], (1, 0, 0))
        self.assertEqual(data[2], (10, 0, 0))
    
    def test_parse_negative_coordinates(self):
        """Test parsing boxes with negative coordinates."""
        negative_input = """-10,-20,-30
5,-15,0
-1,-1,-1"""
        
        data = parse_input(negative_input)
        
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0], (-10, -20, -30))
        self.assertEqual(data[1], (5, -15, 0))
        self.assertEqual(data[2], (-1, -1, -1))
    
    def test_parse_whitespace_handling(self):
        """Test parsing handles whitespace correctly."""
        whitespace_input = """  0,0,0  
1,1,1
  2,2,2"""
        
        data = parse_input(whitespace_input)
        
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0], (0, 0, 0))
        self.assertEqual(data[2], (2, 2, 2))


class TestDay08DistanceCalculation(unittest.TestCase):
    """Tests for 3D Euclidean distance calculations."""
    
    def test_distance_unit_x_axis(self):
        """Test distance along X axis."""
        # Import distance function from solution
        try:
            from solution import euclidean_distance
        except ImportError:
            self.skipTest("euclidean_distance not yet implemented")
        
        pos1 = (0, 0, 0)
        pos2 = (1, 0, 0)
        
        distance = euclidean_distance(pos1, pos2)
        self.assertAlmostEqual(distance, 1.0, places=5, 
                              msg="Distance along X axis should be 1")
    
    def test_distance_unit_y_axis(self):
        """Test distance along Y axis."""
        try:
            from solution import euclidean_distance
        except ImportError:
            self.skipTest("euclidean_distance not yet implemented")
        
        pos1 = (0, 0, 0)
        pos2 = (0, 1, 0)
        
        distance = euclidean_distance(pos1, pos2)
        self.assertAlmostEqual(distance, 1.0, places=5,
                              msg="Distance along Y axis should be 1")
    
    def test_distance_unit_z_axis(self):
        """Test distance along Z axis."""
        try:
            from solution import euclidean_distance
        except ImportError:
            self.skipTest("euclidean_distance not yet implemented")
        
        pos1 = (0, 0, 0)
        pos2 = (0, 0, 1)
        
        distance = euclidean_distance(pos1, pos2)
        self.assertAlmostEqual(distance, 1.0, places=5,
                              msg="Distance along Z axis should be 1")
    
    def test_distance_3d_diagonal(self):
        """Test distance on 3D diagonal."""
        try:
            from solution import euclidean_distance
        except ImportError:
            self.skipTest("euclidean_distance not yet implemented")
        
        pos1 = (0, 0, 0)
        pos2 = (1, 1, 1)
        
        distance = euclidean_distance(pos1, pos2)
        expected = math.sqrt(3)  # sqrt(1² + 1² + 1²)
        self.assertAlmostEqual(distance, expected, places=5,
                              msg="Distance on 3D diagonal should be sqrt(3)")
    
    def test_distance_symmetry(self):
        """Test that distance is symmetric (d(A,B) = d(B,A))."""
        try:
            from solution import euclidean_distance
        except ImportError:
            self.skipTest("euclidean_distance not yet implemented")
        
        pos1 = (10, 20, 30)
        pos2 = (40, 50, 60)
        
        dist1 = euclidean_distance(pos1, pos2)
        dist2 = euclidean_distance(pos2, pos1)
        
        self.assertAlmostEqual(dist1, dist2, places=5,
                              msg="Distance should be symmetric")
    
    def test_distance_zero(self):
        """Test distance from point to itself is zero."""
        try:
            from solution import euclidean_distance
        except ImportError:
            self.skipTest("euclidean_distance not yet implemented")
        
        pos = (5, 10, 15)
        
        distance = euclidean_distance(pos, pos)
        self.assertAlmostEqual(distance, 0.0, places=5,
                              msg="Distance from point to itself should be 0")
    
    def test_distance_large_values(self):
        """Test distance calculation with large coordinate values."""
        try:
            from solution import euclidean_distance
        except ImportError:
            self.skipTest("euclidean_distance not yet implemented")
        
        pos1 = (162, 817, 812)
        pos2 = (425, 690, 689)
        
        # Expected: sqrt((425-162)² + (690-817)² + (689-812)²)
        # = sqrt(263² + (-127)² + (-123)²)
        # = sqrt(69129 + 16129 + 15129)
        # = sqrt(100387) ≈ 316.83
        distance = euclidean_distance(pos1, pos2)
        expected = math.sqrt((425-162)**2 + (690-817)**2 + (689-812)**2)
        
        self.assertAlmostEqual(distance, expected, places=2,
                              msg="Distance calculation incorrect for large values")


class TestDay08UnionFind(unittest.TestCase):
    """Tests for Union-Find data structure."""
    
    def test_union_find_initialization(self):
        """Test UnionFind initialization with n elements."""
        try:
            from solution import UnionFind
        except ImportError:
            self.skipTest("UnionFind not yet implemented")
        
        uf = UnionFind(5)
        
        # Initially, each element should be its own root
        for i in range(5):
            self.assertEqual(uf.find(i), i, 
                           f"Element {i} should initially be its own root")
    
    def test_union_find_basic_union(self):
        """Test basic union operation."""
        try:
            from solution import UnionFind
        except ImportError:
            self.skipTest("UnionFind not yet implemented")
        
        uf = UnionFind(5)
        
        # Union elements 0 and 1
        result = uf.union(0, 1)
        self.assertTrue(result, "Union of separate elements should return True")
        
        # They should now have the same root
        self.assertEqual(uf.find(0), uf.find(1),
                        "Elements 0 and 1 should have same root after union")
    
    def test_union_find_already_connected(self):
        """Test union returns False when elements already connected."""
        try:
            from solution import UnionFind
        except ImportError:
            self.skipTest("UnionFind not yet implemented")
        
        uf = UnionFind(5)
        
        # Union 0 and 1
        uf.union(0, 1)
        
        # Union 1 and 2
        uf.union(1, 2)
        
        # Now 0 and 2 are already connected
        result = uf.union(0, 2)
        self.assertFalse(result, 
                        "Union of already-connected elements should return False")
    
    def test_union_find_transitive_connection(self):
        """Test transitive connections (if A-B and B-C, then A-C)."""
        try:
            from solution import UnionFind
        except ImportError:
            self.skipTest("UnionFind not yet implemented")
        
        uf = UnionFind(5)
        
        # Connect 0-1 and 1-2
        uf.union(0, 1)
        uf.union(1, 2)
        
        # 0 and 2 should be transitively connected
        self.assertEqual(uf.find(0), uf.find(2),
                        "Elements 0 and 2 should be connected transitively")
    
    def test_union_find_get_circuit_sizes(self):
        """Test getting circuit sizes."""
        try:
            from solution import UnionFind
        except ImportError:
            self.skipTest("UnionFind not yet implemented")
        
        uf = UnionFind(5)
        
        # Create circuit: {0,1,2} and leave {3}, {4} separate
        uf.union(0, 1)
        uf.union(1, 2)
        
        sizes = uf.get_circuit_sizes()
        sizes_sorted = sorted(sizes, reverse=True)
        
        # Should have circuits of size [3, 1, 1]
        self.assertEqual(sizes_sorted, [3, 1, 1],
                        "Circuit sizes incorrect after unions")
    
    def test_union_find_multiple_circuits(self):
        """Test multiple separate circuits."""
        try:
            from solution import UnionFind
        except ImportError:
            self.skipTest("UnionFind not yet implemented")
        
        uf = UnionFind(10)
        
        # Create circuits: {0,1,2}, {3,4}, {5,6,7,8}, {9}
        uf.union(0, 1)
        uf.union(1, 2)
        uf.union(3, 4)
        uf.union(5, 6)
        uf.union(6, 7)
        uf.union(7, 8)
        
        sizes = uf.get_circuit_sizes()
        sizes_sorted = sorted(sizes, reverse=True)
        
        # Should have circuits of size [4, 3, 2, 1]
        self.assertEqual(sizes_sorted, [4, 3, 2, 1],
                        "Multiple circuit sizes incorrect")


class TestDay08Part1(unittest.TestCase):
    """Tests for Part 1 solution."""
    
    def setUp(self):
        """Set up test fixtures and example data."""
        self.example_input = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""
        
        self.simple_3_boxes = """0,0,0
1,0,0
10,0,0"""
        
        self.simple_4_boxes = """0,0,0
1,0,0
0,1,0
0,0,1"""
        
        self.collinear = """0,0,0
1,0,0
2,0,0
3,0,0
4,0,0"""
        
        self.skip_connected = """0,0,0
1,0,0
2,0,0
10,0,0"""
    
    def test_example_from_spec_9_connections(self):
        """Test Part 1 with the example from specification (9 successful connections).
        
        IMPORTANT: The spec traces 10 pairs, but connection attempt #4 is SKIPPED
        because boxes 9 and 0 are already connected. Therefore, only 9 ACTUAL
        successful union operations occur. The num_connections parameter counts
        only successful connections (skips don't count toward the total).
        
        After 9 successful connections, circuits are [5,4,2,2,1,1,1,1,1,1,1]
        Three largest: 5, 4, 2
        Product: 5 × 4 × 2 = 40
        """
        data = parse_input(self.example_input)
        
        # 9 successful connections (not 10 - one pair is skipped)
        result = solve_part1(data, num_connections=9)
        
        self.assertEqual(result, 40,
                        "Example with 9 successful connections should produce 40")
    
    def test_simple_3_boxes_1_connection(self):
        """Test Part 1 with 3 boxes and 1 connection."""
        data = parse_input(self.simple_3_boxes)
        
        # After 1 connection: [2, 1]
        # Product of three largest when only 2 circuits: need to handle gracefully
        # For this test, check with 1 connection that we get reasonable result
        # The closest pair is (0,0,0)-(1,0,0) distance 1
        # This creates circuits [2, 1]
        # If we need 3 largest but only have 2, might return product with 1s
        # or handle edge case differently
        result = solve_part1(data, num_connections=1)
        
        # Expected behavior: [2, 1, 1] (padding with 1s for missing circuits)
        # Product: 2 × 1 × 1 = 2
        # OR could be [2, 1] and product of available = 2
        # Check implementation handles this edge case
        self.assertIsInstance(result, int, "Should return an integer")
        self.assertGreaterEqual(result, 2, "Product should be at least 2")
    
    def test_simple_4_boxes_3_connections(self):
        """Test Part 1 with 4 boxes at unit cube corners."""
        data = parse_input(self.simple_4_boxes)
        
        # All edges have length 1 (to adjacent corners) or sqrt(2) (to diagonal)
        # After 3 connections with distance 1: could form [4] or [3,1] etc.
        result = solve_part1(data, num_connections=3)
        
        self.assertIsInstance(result, int, "Should return an integer")
        self.assertGreater(result, 0, "Product should be positive")
    
    def test_collinear_points_4_connections(self):
        """Test Part 1 with collinear points."""
        data = parse_input(self.collinear)
        
        # Points at 0, 1, 2, 3, 4 on x-axis
        # Closest pairs: (0,1), (1,2), (2,3), (3,4) all distance 1
        # After 4 connections: all in one circuit [5]
        # Product: 5 × 1 × 1 = 5 (or handle single circuit)
        result = solve_part1(data, num_connections=4)
        
        self.assertIsInstance(result, int, "Should return an integer")
        # With all connected, should have [5, 1, 1] or handle gracefully
        self.assertGreaterEqual(result, 5, "Should form one large circuit")
    
    def test_skip_already_connected_pairs(self):
        """Test that already-connected pairs are skipped correctly."""
        data = parse_input(self.skip_connected)
        
        # 4 boxes: (0,0,0), (1,0,0), (2,0,0), (10,0,0)
        # Distances: 0-1=1, 1-2=1, 0-2=2, 0-3=10, 1-3=9, 2-3=8
        # Sorted: (0,1), (1,2), (0,2), (2,3), (1,3), (0,3)
        # Connection 1: 0-1 → [2,1,1]
        # Connection 2: 1-2 → [3,1] (connects 0,1,2)
        # Next closest is 0-2 but already connected, skip
        # Connection 3: 2-3 → [4] (all connected)
        result = solve_part1(data, num_connections=3)
        
        # After 3 actual connections, all 4 should be in one circuit
        # Product: 4 × 1 × 1 = 4
        self.assertIsInstance(result, int, "Should return an integer")
        self.assertGreaterEqual(result, 4, "Should skip already-connected pairs")
    
    def test_part1_handles_fewer_than_3_circuits(self):
        """Test Part 1 gracefully handles fewer than 3 circuits."""
        # Create input with many connections forming large circuit
        data = parse_input(self.collinear)
        
        # Connect everything
        result = solve_part1(data, num_connections=10)
        
        # Should handle case where all or most boxes in single circuit
        self.assertIsInstance(result, int, "Should return an integer")
        self.assertGreater(result, 0, "Product should be positive")
    
    def test_part1_zero_connections(self):
        """Test Part 1 with zero connections (edge case)."""
        data = parse_input(self.simple_3_boxes)
        
        # With 0 connections: [1, 1, 1] (all separate)
        # Product: 1 × 1 × 1 = 1
        result = solve_part1(data, num_connections=0)
        
        self.assertEqual(result, 1, 
                        "Zero connections should give product of 1×1×1=1")


class TestDay08Part2(unittest.TestCase):
    """Tests for Part 2 solution."""
    
    def setUp(self):
        """Set up test fixtures and example data."""
        self.example_input = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""
        
        self.simple_3_boxes = """0,0,0
5,0,0
10,0,0"""
        
        self.two_boxes_only = """100,200,300
400,500,600"""
        
        self.square_config = """0,0,0
10,0,0
10,10,0
0,10,0"""
    
    def test_example_from_spec_complete_circuit(self):
        """Test Part 2 with the example from specification (complete circuit).
        
        The example input has 20 junction boxes. To form a single circuit,
        we need exactly 19 successful connections (n-1 where n=20).
        
        According to the spec:
        - Last connection is between boxes at (216,146,977) and (117,168,530)
        - These are at indices 10 and 12 in the input
        - X coordinates: 216 and 117
        - Product: 216 × 117 = 25272
        """
        data = parse_input(self.example_input)
        
        # Verify we parsed 20 boxes
        self.assertEqual(len(data), 20, "Should parse 20 junction boxes")
        
        # Verify the key boxes are at the expected indices
        self.assertEqual(data[10], (216, 146, 977), "Box at index 10 should be (216,146,977)")
        self.assertEqual(data[12], (117, 168, 530), "Box at index 12 should be (117,168,530)")
        
        # Solve Part 2
        result = solve_part2(data)
        
        # Expected: 216 × 117 = 25272
        self.assertEqual(result, 25272,
                        "Example should produce 25272 (216 × 117)")
    
    def test_simple_3_boxes_collinear(self):
        """Test Part 2 with 3 boxes in a line.
        
        Boxes at (0,0,0), (5,0,0), (10,0,0)
        - Distance (0,0,0)-(5,0,0) = 5
        - Distance (5,0,0)-(10,0,0) = 5
        - Distance (0,0,0)-(10,0,0) = 10
        
        Greedy algorithm connects closest first:
        - Connection 1: (0,0,0)-(5,0,0) → circuits: [2,1]
        - Connection 2: (5,0,0)-(10,0,0) → circuits: [3] (all connected)
        
        Last connection is between indices 1 and 2 (boxes at (5,0,0) and (10,0,0))
        X coordinates: 5 and 10
        Product: 5 × 10 = 50
        """
        data = parse_input(self.simple_3_boxes)
        
        # Verify we parsed 3 boxes
        self.assertEqual(len(data), 3, "Should parse 3 junction boxes")
        
        # Solve Part 2
        result = solve_part2(data)
        
        # Expected: 5 × 10 = 50
        self.assertEqual(result, 50,
                        "3 collinear boxes should produce 50 (5 × 10)")
    
    def test_minimum_two_boxes_only(self):
        """Test Part 2 with minimum possible input (2 boxes).
        
        With only 2 boxes, we need exactly 1 connection to form a single circuit.
        Boxes at (100,200,300) and (400,500,600)
        
        This is the only connection, so it's also the last connection.
        X coordinates: 100 and 400
        Product: 100 × 400 = 40000
        """
        data = parse_input(self.two_boxes_only)
        
        # Verify we parsed 2 boxes
        self.assertEqual(len(data), 2, "Should parse 2 junction boxes")
        
        # Solve Part 2
        result = solve_part2(data)
        
        # Expected: 100 × 400 = 40000
        self.assertEqual(result, 40000,
                        "2 boxes should produce 40000 (100 × 400)")
    
    def test_x_coordinate_extraction_only(self):
        """Test that Part 2 uses ONLY X coordinates (not Y or Z).
        
        Create a case where using Y or Z would give a different result
        to verify we're using the correct coordinate.
        
        Boxes arranged so last connection has:
        - X coords that multiply to one value
        - Y coords that would multiply to a different value
        - Z coords that would multiply to yet another value
        """
        # Two boxes where X, Y, Z are all different
        test_input = """10,100,1000
20,200,2000"""
        
        data = parse_input(test_input)
        result = solve_part2(data)
        
        # X coordinates: 10 × 20 = 200
        # Y coordinates: 100 × 200 = 20000 (wrong!)
        # Z coordinates: 1000 × 2000 = 2000000 (wrong!)
        
        self.assertEqual(result, 200,
                        "Should use X coordinates only, not Y or Z")
        self.assertNotEqual(result, 20000, "Should not use Y coordinates")
        self.assertNotEqual(result, 2000000, "Should not use Z coordinates")
    
    def test_track_last_successful_connection(self):
        """Test that Part 2 correctly tracks the LAST successful connection.
        
        Use a simple case where we can verify:
        1. The algorithm makes exactly n-1 successful connections
        2. Already-connected pairs are skipped (don't count as the "last" connection)
        3. The final connection is correctly identified
        """
        # 4 boxes in a line: (0,0,0), (1,0,0), (2,0,0), (10,0,0)
        test_input = """0,0,0
1,0,0
2,0,0
10,0,0"""
        
        data = parse_input(test_input)
        
        # With 4 boxes, need exactly 3 successful connections
        # Distances: 0-1=1, 1-2=1, 0-2=2, 2-3=8, 1-3=9, 0-3=10
        # Order: (0,1), (1,2), (0,2), (2,3), (1,3), (0,3)
        # Connection 1: 0-1 → circuits: [2,1,1]
        # Connection 2: 1-2 → circuits: [3,1]
        # Attempt 3: 0-2 → already connected, skip
        # Connection 3: 2-3 → circuits: [4] (final connection!)
        
        # Last connection should be between indices 2 and 3
        # X coords: 2 and 10
        # Product: 2 × 10 = 20
        
        result = solve_part2(data)
        
        self.assertEqual(result, 20,
                        "Should track last successful connection, not skipped pairs")
    
    def test_square_configuration_equidistant_edges(self):
        """Test Part 2 with 4 boxes forming a square.
        
        Boxes at corners of a 10×10 square in the XY plane:
        - (0,0,0), (10,0,0), (10,10,0), (0,10,0)
        
        Distances:
        - Four edges of length 10
        - Two diagonals of length ~14.14
        
        The algorithm will connect the 3 shortest edges first (all length 10).
        The last connection will be the third edge chosen.
        
        Since multiple edges have the same length, the exact order depends
        on the sorting stability and pair generation order.
        
        Possible last connections (third edge with length 10):
        - Could be any of the four edges
        
        We verify that:
        1. The result is a valid product of X coordinates from the square
        2. The algorithm completes successfully
        3. All 4 boxes are connected after 3 connections
        """
        data = parse_input(self.square_config)
        
        # Verify we parsed 4 boxes
        self.assertEqual(len(data), 4, "Should parse 4 junction boxes")
        
        # Solve Part 2
        result = solve_part2(data)
        
        # Valid products from edges with length 10:
        # Edge (0,0,0)-(10,0,0): 0 × 10 = 0
        # Edge (10,0,0)-(10,10,0): 10 × 10 = 100
        # Edge (10,10,0)-(0,10,0): 10 × 0 = 0
        # Edge (0,10,0)-(0,0,0): 0 × 0 = 0
        
        # Most likely outcomes are 0 or 100
        valid_results = [0, 100]
        
        self.assertIn(result, valid_results,
                     f"Square configuration should produce one of {valid_results}, got {result}")
    
    def test_part2_returns_integer(self):
        """Test that Part 2 returns an integer (not None or other type)."""
        data = parse_input(self.two_boxes_only)
        result = solve_part2(data)
        
        self.assertIsInstance(result, int,
                            "Part 2 should return an integer")
    
    def test_part2_positive_result(self):
        """Test that Part 2 returns a positive result (non-zero X coordinates)."""
        # Use boxes with non-zero X coordinates
        test_input = """5,0,0
15,0,0
25,0,0"""
        
        data = parse_input(test_input)
        result = solve_part2(data)
        
        self.assertGreater(result, 0,
                          "Part 2 should return positive result for non-zero X coords")
    
    def test_part2_single_box_invalid(self):
        """Test Part 2 behavior with invalid input (single box).
        
        With only 1 box, it's impossible to form connections.
        The implementation should handle this gracefully.
        """
        single_box = """100,200,300"""
        data = parse_input(single_box)
        
        # With only 1 box, there are no pairs to connect
        # This is technically an invalid input for the problem
        # The implementation might return 0, None, or raise an exception
        # We just verify it doesn't crash
        try:
            result = solve_part2(data)
            # If it returns a value, it should be 0 or None
            self.assertIn(result, [0, None],
                         "Single box should return 0 or None")
        except (ValueError, IndexError):
            # It's also acceptable to raise an exception
            pass
    
    def test_part2_stops_at_exactly_n_minus_1_connections(self):
        """Test that Part 2 makes exactly n-1 successful connections.
        
        This is a critical requirement: with n boxes, we need exactly
        n-1 connections to form a single circuit (spanning tree).
        
        We use a simple case where we can verify the connection count.
        """
        # 5 collinear boxes
        test_input = """0,0,0
1,0,0
2,0,0
3,0,0
4,0,0"""
        
        data = parse_input(test_input)
        
        # With 5 boxes, need exactly 4 successful connections
        # All adjacent pairs have distance 1
        # Connections will be: (0,1), (1,2), (2,3), (3,4)
        # Last connection: (3,4)
        # X coords: 3 × 4 = 12
        
        result = solve_part2(data)
        
        self.assertEqual(result, 12,
                        "5 boxes should stop at 4th connection: 3 × 4 = 12")


class TestDay08Integration(unittest.TestCase):
    """Integration tests for complete solution flow."""
    
    def test_end_to_end_example(self):
        """Test complete end-to-end flow with example input.
        
        This uses 9 successful connections (not 10) because the spec example
        shows that one connection attempt is skipped when boxes are already connected.
        """
        example_input = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""
        
        # Parse
        data = parse_input(example_input)
        self.assertEqual(len(data), 20, "Should parse 20 boxes")
        
        # Solve with 9 successful connections (10 pairs processed, 1 skipped)
        result = solve_part1(data, num_connections=9)
        self.assertEqual(result, 40, "End-to-end test should produce 40")
    
    def test_parsing_and_solving_simple_case(self):
        """Test complete flow with simple 3-box case."""
        simple_input = """0,0,0
1,0,0
2,0,0"""
        
        # Parse
        data = parse_input(simple_input)
        self.assertEqual(len(data), 3)
        
        # Solve with 2 connections (should connect all 3)
        result = solve_part1(data, num_connections=2)
        
        # Should have [3, 1, 1] or similar
        self.assertIsInstance(result, int)
        self.assertGreater(result, 0)


if __name__ == '__main__':
    unittest.main()
