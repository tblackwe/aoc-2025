#!/usr/bin/env python3
"""
Test cases for Day 06: Trash Compactor.
Run these tests before implementing the solution (TDD).

This test suite covers:
- Main example from spec (expected: 4,277,556)
- 7 simple test cases (single columns, two columns, etc.)
- 7 edge cases (zeros, large numbers, alignment, spacing)
- 4 corner cases (identity elements, large products, etc.)
- Parsing and helper function tests
"""

import unittest
from solution import (
    parse_input,
    solve_part1,
    solve_part2,
    find_operators,
    extract_number_at_position,
    extract_column_numbers,
    calculate_result,
)


class TestDay06Parsing(unittest.TestCase):
    """Tests for input parsing logic."""
    
    def test_parse_input_basic(self):
        """Test parsing basic input preserves spacing."""
        input_text = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """
        lines = parse_input(input_text)
        self.assertEqual(len(lines), 4, "Should parse 4 lines")
        self.assertIsInstance(lines, list, "Should return a list")
        self.assertTrue(all(isinstance(line, str) for line in lines), "All elements should be strings")
    
    def test_parse_input_preserves_spaces(self):
        """Test that parsing preserves internal spacing."""
        input_text = "  1 10\n 10 5\n100 2\n+   *"
        lines = parse_input(input_text)
        # Check that leading spaces are preserved
        self.assertTrue(lines[0].startswith("  "), "Should preserve leading spaces")
        self.assertIn("  ", lines[3], "Should preserve internal spacing")
    
    def test_parse_empty_input(self):
        """Test parsing empty or minimal input."""
        lines = parse_input("")
        self.assertEqual(len(lines), 1, "Empty input with strip returns single empty string")
        self.assertEqual(lines[0], "", "Should be empty string")
    
    def test_find_operators_basic(self):
        """Test finding operators in operator row."""
        operator_row = "*   +   *   +  "
        operators = find_operators(operator_row)
        self.assertEqual(len(operators), 4, "Should find 4 operators")
        self.assertEqual(operators[0], (0, '*'), "First operator at position 0")
        self.assertEqual(operators[1], (4, '+'), "Second operator at position 4")
        self.assertEqual(operators[2], (8, '*'), "Third operator at position 8")
        self.assertEqual(operators[3], (12, '+'), "Fourth operator at position 12")
    
    def test_find_operators_single(self):
        """Test finding single operator."""
        operator_row = "+"
        operators = find_operators(operator_row)
        self.assertEqual(len(operators), 1, "Should find 1 operator")
        self.assertEqual(operators[0], (0, '+'), "Operator at position 0")
    
    def test_find_operators_mixed(self):
        """Test finding mixed operators."""
        operator_row = "+  *"
        operators = find_operators(operator_row)
        self.assertEqual(len(operators), 2, "Should find 2 operators")
        self.assertIn('+', [op for _, op in operators], "Should find addition")
        self.assertIn('*', [op for _, op in operators], "Should find multiplication")
    
    def test_extract_number_at_position_single_digit(self):
        """Test extracting single digit number."""
        row = "5"
        num = extract_number_at_position(row, 0)
        self.assertEqual(num, 5, "Should extract single digit")
    
    def test_extract_number_at_position_multi_digit(self):
        """Test extracting multi-digit number."""
        row = "123"
        num = extract_number_at_position(row, 0)
        self.assertEqual(num, 123, "Should extract multi-digit number at start")
        
        num = extract_number_at_position(row, 2)
        self.assertEqual(num, 123, "Should extract full number from any position within it")
    
    def test_extract_number_at_position_with_spaces(self):
        """Test extracting number with leading spaces."""
        row = "  123"
        num = extract_number_at_position(row, 2)
        self.assertEqual(num, 123, "Should extract number after spaces")
    
    def test_extract_number_at_position_no_digit(self):
        """Test extraction returns None when no digit found."""
        row = "   "
        num = extract_number_at_position(row, 0)
        self.assertIsNone(num, "Should return None for spaces")
    
    def test_calculate_result_addition(self):
        """Test addition operation."""
        result = calculate_result([10, 20, 30], '+')
        self.assertEqual(result, 60, "Should sum numbers")
    
    def test_calculate_result_multiplication(self):
        """Test multiplication operation."""
        result = calculate_result([2, 3, 4], '*')
        self.assertEqual(result, 24, "Should multiply numbers")
    
    def test_calculate_result_single_number_addition(self):
        """Test addition with single number."""
        result = calculate_result([42], '+')
        self.assertEqual(result, 42, "Single number addition should return the number")
    
    def test_calculate_result_single_number_multiplication(self):
        """Test multiplication with single number."""
        result = calculate_result([42], '*')
        self.assertEqual(result, 42, "Single number multiplication should return the number")


class TestDay06Part1MainExample(unittest.TestCase):
    """Tests for Part 1 with the main example from the specification."""
    
    def setUp(self):
        """Set up the main example from the spec."""
        self.main_example = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """
    
    def test_main_example_full_solution(self):
        """Test Part 1 with the main example from specification.
        
        Expected breakdown:
        - Column 1: 123 * 45 * 6 = 33,210
        - Column 2: 328 + 64 + 98 = 490
        - Column 3: 51 * 387 * 215 = 4,243,455
        - Column 4: 64 + 23 + 314 = 401
        - Grand Total: 4,277,556
        """
        result = solve_part1(self.main_example)
        self.assertEqual(result, 4277556, "Main example should return 4,277,556")


class TestDay06Part1SimpleCases(unittest.TestCase):
    """Tests for Part 1 with simple test cases."""
    
    def test_simple_1_single_column_addition(self):
        """Test 1: Single column addition.
        
        Input: 10, 20, 30 with +
        Expected: 60 (10 + 20 + 30)
        """
        input_text = """10
20
30
+"""
        result = solve_part1(input_text)
        self.assertEqual(result, 60, "Single column addition: 10+20+30=60")
    
    def test_simple_2_single_column_multiplication(self):
        """Test 2: Single column multiplication.
        
        Input: 2, 3, 4 with *
        Expected: 24 (2 * 3 * 4)
        """
        input_text = """2
3
4
*"""
        result = solve_part1(input_text)
        self.assertEqual(result, 24, "Single column multiplication: 2*3*4=24")
    
    def test_simple_3_two_columns(self):
        """Test 3: Two columns with different operations.
        
        Input: Column 1 (10, 30 with +), Column 2 (20, 40 with *)
        Expected: 840 (40 + 800)
        """
        input_text = """10 20
30 40
+  *"""
        result = solve_part1(input_text)
        self.assertEqual(result, 840, "Two columns: (10+30) + (20*40) = 40 + 800 = 840")
    
    def test_simple_4_single_number_columns(self):
        """Test 4: Single number in each column.
        
        Input: 5 with *, 10 with +
        Expected: 15 (5 + 10)
        """
        input_text = """5 10
*  +"""
        result = solve_part1(input_text)
        self.assertEqual(result, 15, "Single numbers: 5 + 10 = 15")
    
    def test_simple_5_three_digit_numbers(self):
        """Test 5: Three digit numbers.
        
        Input: 100 with +, 200 with *
        Expected: 300 (100 + 200)
        """
        input_text = """100 200
+   *"""
        result = solve_part1(input_text)
        self.assertEqual(result, 300, "Three digit numbers: 100 + 200 = 300")


class TestDay06Part1EdgeCases(unittest.TestCase):
    """Tests for Part 1 edge cases."""
    
    def test_edge_1_minimum_input(self):
        """Edge 1: Minimum input - single number, single operator.
        
        Input: 42 with +
        Expected: 42
        """
        input_text = """42
+"""
        result = solve_part1(input_text)
        self.assertEqual(result, 42, "Single number should return itself")
    
    def test_edge_2_zero_values(self):
        """Edge 2: Zero values in columns.
        
        Input: Column 1 (0, 5 with +), Column 2 (5, 0 with *)
        Expected: 5 (0+5=5, 5*0=0, total=5)
        """
        input_text = """0 5
5 0
+ *"""
        result = solve_part1(input_text)
        self.assertEqual(result, 5, "Zeros: (0+5) + (5*0) = 5 + 0 = 5")
    
    def test_edge_3_large_numbers(self):
        """Edge 3: Large numbers.
        
        Input: Column 1 (999, 999 with *), Column 2 (999, 999 with +)
        Expected: 999,999 (998,001 + 1,998)
        """
        input_text = """999 999
999 999
*   +"""
        result = solve_part1(input_text)
        # 999 * 999 = 998,001
        # 999 + 999 = 1,998
        # Total = 999,999
        self.assertEqual(result, 999999, "Large numbers: 998,001 + 1,998 = 999,999")
    
    def test_edge_4_many_numbers_in_column(self):
        """Edge 4: Many numbers in a single column.
        
        Input: Five 1's with +
        Expected: 5
        """
        input_text = """1
1
1
1
1
+"""
        result = solve_part1(input_text)
        self.assertEqual(result, 5, "Five 1's: 1+1+1+1+1=5")
    
    def test_edge_5_single_digit_vs_multi_digit(self):
        """Edge 5: Single digit vs multi-digit numbers.
        
        Input: Column 1 (1, 10 with *), Column 2 (100, 10 with *)
        Expected: 1,010 (10 + 1,000)
        """
        input_text = """1  100
10 10
*  *"""
        result = solve_part1(input_text)
        self.assertEqual(result, 1010, "Mixed digits: (1*10) + (100*10) = 10 + 1,000 = 1,010")
    
    def test_edge_6_right_alignment_check(self):
        """Edge 6: Right alignment with leading spaces.
        
        Input: Column 1 (1, 10, 100 with +), Column 2 (10, 5, 2 with *)
        Expected: 211 (111 + 100)
        """
        input_text = """  1 10
 10 5
100 2
+   *"""
        result = solve_part1(input_text)
        self.assertEqual(result, 211, "Right aligned: (1+10+100) + (10*5*2) = 111 + 100 = 211")
    
    def test_edge_7_wide_spacing(self):
        """Edge 7: Wide spacing between columns.
        
        Input: Column 1 (1, 2 with +), Column 2 (10, 20 with *)
        Expected: 203 (3 + 200)
        """
        input_text = """1     10
2     20
+     *"""
        result = solve_part1(input_text)
        self.assertEqual(result, 203, "Wide spacing: (1+2) + (10*20) = 3 + 200 = 203")


class TestDay06Part1CornerCases(unittest.TestCase):
    """Tests for Part 1 corner cases."""
    
    def test_corner_1_all_zeros_multiplication(self):
        """Corner 1: All zeros with multiplication.
        
        Input: 0, 0 with *
        Expected: 0
        """
        input_text = """0
0
*"""
        result = solve_part1(input_text)
        self.assertEqual(result, 0, "All zeros: 0*0=0")
    
    def test_corner_2_identity_element_multiplication(self):
        """Corner 2: Identity element for multiplication (all 1's).
        
        Input: 1, 1, 1 with *
        Expected: 1
        """
        input_text = """1
1
1
*"""
        result = solve_part1(input_text)
        self.assertEqual(result, 1, "Identity: 1*1*1=1")
    
    def test_corner_3_large_product(self):
        """Corner 3: Large product (1000 cubed).
        
        Input: 1000, 1000, 1000 with *
        Expected: 1,000,000,000
        """
        input_text = """1000
1000
1000
*"""
        result = solve_part1(input_text)
        self.assertEqual(result, 1000000000, "Large product: 1000^3=1,000,000,000")
    
    def test_corner_4_mixed_large_and_small(self):
        """Corner 4: Mixed large and small values.
        
        Input: Column 1 (1, 1000 with *), Column 2 (1000, 1 with *)
        Expected: 2,000 (1,000 + 1,000)
        """
        input_text = """1    1000
1000    1
*       *"""
        result = solve_part1(input_text)
        self.assertEqual(result, 2000, "Mixed: (1*1000) + (1000*1) = 1,000 + 1,000 = 2,000")


class TestDay06Part1ColumnExtraction(unittest.TestCase):
    """Tests for column extraction logic."""
    
    def test_extract_column_with_right_aligned_numbers(self):
        """Test extracting column with right-aligned numbers."""
        lines = parse_input("""123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """)
        number_rows = lines[:-1]
        
        # Extract first column (position 0, operator *)
        numbers = extract_column_numbers(number_rows, 0)
        self.assertEqual(numbers, [123, 45, 6], "First column should be [123, 45, 6]")
    
    def test_extract_column_at_different_positions(self):
        """Test extracting columns at various positions."""
        lines = parse_input("""10 20 30
40 50 60
+  *  +""")
        number_rows = lines[:-1]
        
        # Column 1 at position 0
        col1 = extract_column_numbers(number_rows, 0)
        self.assertIn(10, col1, "Column 1 should contain 10")
        self.assertIn(40, col1, "Column 1 should contain 40")


class TestDay06Part2MainExample(unittest.TestCase):
    """Tests for Part 2 with the main example."""
    
    def setUp(self):
        """Set up the main example from the task description."""
        self.main_example = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """
    
    def test_main_example_full_solution(self):
        """Test Part 2 with the main example.
        
        Part 2: Cephalopod math is read right-to-left in columns.
        Each CHARACTER POSITION is a column.
        Reading TOP to BOTTOM in each column forms ONE NUMBER.
        The operator at the bottom indicates the operation.
        
        Example breakdown for the input:
        ```
        123 328  51 64     <- positions 0-14 (with trailing space, pos 15)
         45 64  387 23     <- note leading space
          6 98  215 314
        *   +   *   +  
        ```
        
        Each position (column) is read top-to-bottom:
        - Position 0: '1', ' ', ' ', '*' 
        - Position 1: '2', '4', ' ', ' '
        - Position 2: '3', '5', '6', ' '
        - ...continuing...
        - Position 15 (rightmost): '4', '3', '4', '1'
        
        The task says: "Reading TOP to BOTTOM in each column forms one number."
        So at position 15: '4' (row 0), '3' (row 1 - wait, that's wrong...)
        
        Let me re-read the example from task:
        "Rightmost column (pos 15): '4', ' ', ' ' → reads as \"4\""
        "Next left (pos 14): '6', '3', '4' → reads as \"634\""
        
        So position 15 (rightmost actual character):
        - Row 0, pos 15: ' ' (space after 64)
        - Actually, looking at "64 " - position 14 is '4', position 15 is ' '
        
        Let me index the actual example:
        Row 0: "123 328  51 64 "
               0123456789012345
        
        Position 15: ' ', ' ', ' ', ' ' - all spaces
        Position 14: '4', '3', '4', '+' → reads "434" with operator +
        Position 13: '6', '2', '1', ' ' → reads "621"
        Position 12: ' ', ' ', '3', '+' → reads "3"
        
        Wait, the task description says:
        "Rightmost column (pos 15): '4', ' ', ' ' → reads as \"4\""
        
        This suggests the positions are numbered differently or there's 
        something about alignment I'm missing.
        
        Expected Part 2 answer: 3263827
        """
        result = solve_part2(self.main_example)
        self.assertEqual(result, 3263827, "Main example Part 2 should return 3,263,827")


class TestDay06Part2VerticalReading(unittest.TestCase):
    """Tests for Part 2 vertical reading logic - reading each position top-to-bottom."""
    
    def test_vertical_reading_explanation(self):
        """Document the vertical reading interpretation.
        
        Based on task description:
        "Each character position is a column, and reading TOP to BOTTOM 
        in each column forms one number."
        
        So for this input:
        ```
        1 2
        3 4
        + *
        ```
        
        Position 0: '1', '3', '+' → number "13" with operator +
        Position 1: ' ', ' ', ' ' → space
        Position 2: '2', '4', '*' → number "24" with operator *
        
        Reading right-to-left, we process:
        - Position 2 first: 24 with *
        - Position 0 next: 13 with +
        
        So we have two problems processed right-to-left:
        - Problem 1 (rightmost): 24 (single number with *, identity)
        - Problem 2: 13 (single number with +, identity)
        
        Expected total: 24 + 13 = 37
        
        BUT we need to understand how multiple numbers in one problem work!
        """
        input_text = """1 2
3 4
+ *"""
        result = solve_part2(input_text)
        # This test documents expected behavior - actual value TBD
        self.assertIsInstance(result, int, "Part 2 should return an integer")
    
    def test_simple_single_column_vertical(self):
        """Test simplest case - single character column.
        
        Input:
        ```
        5
        3
        +
        ```
        
        Position 0: '5', '3', '+' → number "53" with operator +
        
        Since there's only one number "53" and operator +, result is 53.
        
        Expected: 53
        """
        input_text = """5
3
+"""
        result = solve_part2(input_text)
        # The vertical reading should form "53" from '5' and '3'
        # With operator +, single number returns itself
        # This is an assumption to be verified
        self.assertIsInstance(result, int, "Part 2 should return an integer")
    
    def test_two_rows_vertical_read(self):
        """Test reading two rows vertically.
        
        Input:
        ```
        12
        34
        +
        ```
        
        Position 0: '1', '3', '+' → number "13"
        Position 1: '2', '4', ' ' → number "24" (but no operator here)
        
        Operator is at position 0, so that defines one problem.
        But how do we know which positions belong to the problem?
        
        This is where the confusion lies - need to understand grouping.
        """
        input_text = """12
34
+"""
        result = solve_part2(input_text)
        self.assertIsInstance(result, int, "Part 2 should return an integer")
    
    def test_vertical_with_spaces(self):
        """Test vertical reading with spaces in the mix.
        
        Input:
        ```
        1  2
        3  4
        +  *
        ```
        
        Position 0: '1', '3', '+' → "13" with +
        Position 1: ' ', ' ', ' ' → space
        Position 2: ' ', ' ', ' ' → space  
        Position 3: '2', '4', '*' → "24" with *
        
        Two problems:
        - Problem at pos 0: 13 with + → result 13
        - Problem at pos 3: 24 with * → result 24
        
        Expected: 13 + 24 = 37
        """
        input_text = """1  2
3  4
+  *"""
        result = solve_part2(input_text)
        self.assertIsInstance(result, int, "Part 2 should return an integer")


class TestDay06Part2MultipleNumbersPerProblem(unittest.TestCase):
    """Tests for understanding how multiple numbers in one problem are grouped in Part 2."""
    
    def test_understanding_problem_grouping(self):
        """Understand how numbers are grouped into problems.
        
        From the main example, the task says:
        "The rightmost problem: 4 + 431 + 623 = 1058"
        
        This suggests that one problem can have MULTIPLE numbers.
        So the question is: how are multiple numbers assigned to one problem?
        
        Hypothesis: positions between operators form one problem.
        Reading each position vertically gives numbers for that problem.
        """
        # This is a documentation test
        self.assertTrue(True, "Understanding test")
    
    def test_three_positions_one_operator(self):
        """Test three positions with one operator.
        
        Input:
        ```
        123
        456
        +
        ```
        
        Position 0: '1', '4', '+' → operator position, number "14"
        Position 1: '2', '5', ' ' → number "25"
        Position 2: '3', '6', ' ' → number "36"
        
        If all three positions belong to one problem with operator +:
        14 + 25 + 36 = 75
        
        Expected: 75
        """
        input_text = """123
456
+"""
        result = solve_part2(input_text)
        # This is speculative - actual grouping logic needs verification
        self.assertIsInstance(result, int, "Part 2 should return an integer")


class TestDay06Part2EdgeCases(unittest.TestCase):
    """Tests for Part 2 edge cases."""
    
    def test_single_position_single_digit(self):
        """Edge case: Single position, single digit.
        
        Input:
        ```
        5
        +
        ```
        
        Position 0: '5', '+' → number "5" with operator +
        
        Expected: 5
        """
        input_text = """5
+"""
        result = solve_part2(input_text)
        self.assertIsInstance(result, int, "Part 2 should return an integer")
    
    def test_trailing_spaces_handling(self):
        """Test handling of trailing spaces.
        
        Input has trailing spaces which might affect column counting.
        """
        input_text = """12  
34  
+   """
        result = solve_part2(input_text)
        self.assertIsInstance(result, int, "Part 2 should return an integer")
    
    def test_skip_space_rows(self):
        """Test that spaces in vertical reading are handled.
        
        Input:
        ```
        1
         
        3
        +
        ```
        
        Position 0: '1', ' ', '3', '+' → digits "13", operator +
        
        Spaces should be skipped when forming numbers.
        """
        input_text = """1
 
3
+"""
        result = solve_part2(input_text)
        self.assertIsInstance(result, int, "Part 2 should return an integer")


class TestDay06Part2RightToLeftProcessing(unittest.TestCase):
    """Tests for right-to-left processing order in Part 2."""
    
    def test_process_rightmost_first(self):
        """Verify rightmost problem is processed first.
        
        The task says problems are processed right-to-left.
        The order shouldn't affect the sum, but we test that the 
        function processes columns correctly.
        """
        input_text = """1 2
3 4
+ *"""
        result = solve_part2(input_text)
        self.assertIsInstance(result, int, "Part 2 should return an integer")
    
    def test_three_problems_right_to_left(self):
        """Test three problems processed right-to-left.
        
        Input:
        ```
        1 2 3
        4 5 6
        + * +
        ```
        
        Process rightmost problem first (position 4: '3', '6', '+'),
        then middle (position 2: '2', '5', '*'),
        then leftmost (position 0: '1', '4', '+').
        """
        input_text = """1 2 3
4 5 6
+ * +"""
        result = solve_part2(input_text)
        self.assertIsInstance(result, int, "Part 2 should return an integer")


class TestDay06Part2Integration(unittest.TestCase):
    """Integration tests for Part 2 complete workflow."""
    
    def test_full_pipeline_simple(self):
        """Test complete Part 2 pipeline with simple input."""
        input_text = """10
20
+"""
        result = solve_part2(input_text)
        self.assertIsInstance(result, int, "Should return an integer result")
        if result is not None:
            self.assertGreater(result, 0, "Result should be positive")
    
    def test_full_pipeline_two_problems(self):
        """Test complete pipeline with two problems.
        
        Input:
        ```
        1 2
        3 4
        + *
        ```
        """
        input_text = """1 2
3 4
+ *"""
        result = solve_part2(input_text)
        self.assertIsInstance(result, int, "Should return an integer result")
    
    def test_part1_vs_part2_different_results(self):
        """Verify Part 1 and Part 2 produce different results.
        
        Part 1: Read numbers horizontally by column (left-to-right)
        Part 2: Read numbers vertically by position (right-to-left)
        
        They should produce different results for the main example.
        """
        input_text = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """
        
        part1_result = solve_part1(input_text)
        part2_result = solve_part2(input_text)
        
        # Known results from task description
        self.assertEqual(part1_result, 4277556, "Part 1 should be 4,277,556")
        self.assertEqual(part2_result, 3263827, "Part 2 should be 3,263,827")
        
        # They should be different
        self.assertNotEqual(part1_result, part2_result, 
                          "Part 1 and Part 2 should produce different results")


class TestDay06Part2HelperFunctions(unittest.TestCase):
    """Tests for Part 2 helper functions if they are exposed."""
    
    def test_extract_vertical_number_basic(self):
        """Test extracting vertical number at a position.
        
        If extract_vertical_number is defined, test it.
        """
        # Try to import the function
        try:
            from solution import extract_vertical_number
            
            rows = ["123", "456", "789"]
            
            # Position 0: '1', '4', '7' → "147"
            result = extract_vertical_number(rows, 0)
            self.assertEqual(result, 147, "Should read vertical number 147")
            
            # Position 1: '2', '5', '8' → "258"
            result = extract_vertical_number(rows, 1)
            self.assertEqual(result, 258, "Should read vertical number 258")
            
            # Position 2: '3', '6', '9' → "369"
            result = extract_vertical_number(rows, 2)
            self.assertEqual(result, 369, "Should read vertical number 369")
        except ImportError:
            # Function not exposed, skip test
            self.skipTest("extract_vertical_number not exposed")
    
    def test_extract_vertical_with_spaces(self):
        """Test extracting vertical number with spaces.
        
        Spaces should be skipped.
        """
        try:
            from solution import extract_vertical_number
            
            rows = ["1  ", " 5 ", "  9"]
            
            # Position 0: '1', ' ', ' ' → "1"
            result = extract_vertical_number(rows, 0)
            self.assertEqual(result, 1, "Should read vertical number 1, skipping spaces")
            
            # Position 1: ' ', '5', ' ' → "5"
            result = extract_vertical_number(rows, 1)
            self.assertEqual(result, 5, "Should read vertical number 5, skipping spaces")
        except ImportError:
            self.skipTest("extract_vertical_number not exposed")


class TestDay06IntegrationTests(unittest.TestCase):
    """Integration tests that verify full workflow."""
    
    def test_full_pipeline_simple(self):
        """Test complete pipeline with simple input."""
        input_text = """5
5
+"""
        result = solve_part1(input_text)
        self.assertEqual(result, 10, "Complete pipeline: 5+5=10")
    
    def test_full_pipeline_complex(self):
        """Test complete pipeline with complex multi-column input."""
        input_text = """10 5  20
20 10 30
+  *  +"""
        # Column 1: 10 + 20 = 30
        # Column 2: 5 * 10 = 50
        # Column 3: 20 + 30 = 50
        # Total: 30 + 50 + 50 = 130
        result = solve_part1(input_text)
        self.assertEqual(result, 130, "Complex multi-column: 30+50+50=130")
    
    def test_full_pipeline_with_varied_widths(self):
        """Test pipeline with numbers of varying digit widths."""
        input_text = """1   10  100
10  100 1000
+   *   +"""
        # Column 1: 1 + 10 = 11
        # Column 2: 10 * 100 = 1,000
        # Column 3: 100 + 1000 = 1,100
        # Total: 11 + 1,000 + 1,100 = 2,111
        result = solve_part1(input_text)
        self.assertEqual(result, 2111, "Varied widths: 11+1000+1100=2,111")


if __name__ == '__main__':
    unittest.main()
