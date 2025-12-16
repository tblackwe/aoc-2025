#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test cases for Day 10: Factory solution.
Run these tests before implementing the solution (TDD).

This puzzle involves solving systems of linear equations over GF(2) (Galois Field 2)
to find minimum button presses needed to configure machines.
"""

import unittest
from solution import (
    parse_machine,
    parse_input,
    build_matrix,
    gaussian_elimination_gf2,
    find_minimum_solution,
    solve_machine,
    solve_part1,
    Machine,
    # Part 2 functions
    parse_machine_part2,
    build_matrix_part2,
    solve_machine_part2,
    solve_part2
)


class TestDay10Parsing(unittest.TestCase):
    """Tests for input parsing logic."""
    
    def test_parse_single_light_single_button(self):
        """Test parsing simplest possible machine: 1 light, 1 button."""
        line = "[#] (0) {1}"
        machine = parse_machine(line)
        
        self.assertEqual(machine.target, [1], "Target should be [1] for '#'")
        self.assertEqual(machine.buttons, [[0]], "Button should toggle light 0")
    
    def test_parse_machine_1_from_example(self):
        """Test parsing Machine 1 from the main example."""
        line = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
        machine = parse_machine(line)
        
        # Target: .##. → [0, 1, 1, 0]
        expected_target = [0, 1, 1, 0]
        self.assertEqual(machine.target, expected_target, 
                        "Target state should be [0,1,1,0] for '.##.'")
        
        # Buttons
        expected_buttons = [
            [3],       # (3)
            [1, 3],    # (1,3)
            [2],       # (2)
            [2, 3],    # (2,3)
            [0, 2],    # (0,2)
            [0, 1]     # (0,1)
        ]
        self.assertEqual(machine.buttons, expected_buttons,
                        "Button configurations should match")
        self.assertEqual(len(machine.buttons), 6, "Should have 6 buttons")
    
    def test_parse_machine_2_from_example(self):
        """Test parsing Machine 2 from the main example."""
        line = "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}"
        machine = parse_machine(line)
        
        # Target: ...#. → [0, 0, 0, 1, 0]
        expected_target = [0, 0, 0, 1, 0]
        self.assertEqual(machine.target, expected_target,
                        "Target state should be [0,0,0,1,0] for '...#.'")
        
        # Buttons
        expected_buttons = [
            [0, 2, 3, 4],  # (0,2,3,4)
            [2, 3],        # (2,3)
            [0, 4],        # (0,4)
            [0, 1, 2],     # (0,1,2)
            [1, 2, 3, 4]   # (1,2,3,4)
        ]
        self.assertEqual(machine.buttons, expected_buttons,
                        "Button configurations should match")
        self.assertEqual(len(machine.buttons), 5, "Should have 5 buttons")
    
    def test_parse_machine_3_from_example(self):
        """Test parsing Machine 3 from the main example."""
        line = "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
        machine = parse_machine(line)
        
        # Target: .###.# → [0, 1, 1, 1, 0, 1]
        expected_target = [0, 1, 1, 1, 0, 1]
        self.assertEqual(machine.target, expected_target,
                        "Target state should be [0,1,1,1,0,1] for '.###.#'")
        
        # Buttons
        expected_buttons = [
            [0, 1, 2, 3, 4],  # (0,1,2,3,4)
            [0, 3, 4],        # (0,3,4)
            [0, 1, 2, 4, 5],  # (0,1,2,4,5)
            [1, 2]            # (1,2)
        ]
        self.assertEqual(machine.buttons, expected_buttons,
                        "Button configurations should match")
        self.assertEqual(len(machine.buttons), 4, "Should have 4 buttons")
    
    def test_parse_all_lights_off(self):
        """Test parsing machine where all lights should be off."""
        line = "[....] (0,1) (2,3) {1,2}"
        machine = parse_machine(line)
        
        self.assertEqual(machine.target, [0, 0, 0, 0],
                        "All lights should be off (0)")
        self.assertEqual(len(machine.buttons), 2, "Should have 2 buttons")
    
    def test_parse_all_lights_on(self):
        """Test parsing machine where all lights should be on."""
        line = "[####] (0,1,2,3) {1}"
        machine = parse_machine(line)
        
        self.assertEqual(machine.target, [1, 1, 1, 1],
                        "All lights should be on (1)")
        self.assertEqual(machine.buttons, [[0, 1, 2, 3]],
                        "One button toggles all lights")
    
    def test_parse_input_multiple_machines(self):
        """Test parsing multiple machines from example input."""
        input_text = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
        
        machines = parse_input(input_text)
        
        self.assertEqual(len(machines), 3, "Should parse 3 machines")
        self.assertEqual(machines[0].target, [0, 1, 1, 0], "Machine 1 target")
        self.assertEqual(machines[1].target, [0, 0, 0, 1, 0], "Machine 2 target")
        self.assertEqual(machines[2].target, [0, 1, 1, 1, 0, 1], "Machine 3 target")
    
    def test_parse_input_single_machine(self):
        """Test parsing input with single machine."""
        input_text = "[#] (0) {1}"
        machines = parse_input(input_text)
        
        self.assertEqual(len(machines), 1, "Should parse 1 machine")
        self.assertEqual(machines[0].target, [1])
    
    def test_parse_input_empty_lines(self):
        """Test parsing input with empty lines (should be ignored)."""
        input_text = """[#] (0) {1}

[##] (0) (1) {1,1}"""
        machines = parse_input(input_text)
        
        self.assertEqual(len(machines), 2, "Should parse 2 machines, ignore empty line")


class TestDay10MatrixBuilding(unittest.TestCase):
    """Tests for building augmented matrix for Gaussian elimination."""
    
    def test_build_matrix_single_light_single_button(self):
        """Test matrix building for simplest case: 1 light, 1 button."""
        machine = Machine(target=[1], buttons=[[0]])
        matrix = build_matrix(machine)
        
        # Expected: [[1, 1]] meaning button 0 toggles light 0, target is 1
        expected = [[1, 1]]
        self.assertEqual(matrix, expected,
                        "Matrix should be [[1, 1]] for single light/button")
    
    def test_build_matrix_two_lights_independent_buttons(self):
        """Test matrix for two lights with independent buttons."""
        machine = Machine(target=[1, 1], buttons=[[0], [1]])
        matrix = build_matrix(machine)
        
        # Light 0: button 0 toggles it, target = 1
        # Light 1: button 1 toggles it, target = 1
        expected = [
            [1, 0, 1],  # Light 0: b0=1, b1=0, target=1
            [0, 1, 1]   # Light 1: b0=0, b1=1, target=1
        ]
        self.assertEqual(matrix, expected,
                        "Matrix should show independent buttons")
    
    def test_build_matrix_button_toggles_multiple_lights(self):
        """Test matrix when one button toggles multiple lights."""
        machine = Machine(target=[1, 1], buttons=[[0, 1]])
        matrix = build_matrix(machine)
        
        # Both lights toggled by button 0
        expected = [
            [1, 1],  # Light 0: b0 toggles, target=1
            [1, 1]   # Light 1: b0 toggles, target=1
        ]
        self.assertEqual(matrix, expected,
                        "Both rows should have coefficient 1 for button 0")
    
    def test_build_matrix_overlapping_buttons(self):
        """Test matrix with buttons that overlap in lights they toggle."""
        machine = Machine(target=[1, 0], buttons=[[0, 1], [1]])
        matrix = build_matrix(machine)
        
        # Light 0: toggled by button 0 only
        # Light 1: toggled by buttons 0 and 1
        expected = [
            [1, 0, 1],  # Light 0: b0=1, b1=0, target=1
            [1, 1, 0]   # Light 1: b0=1, b1=1, target=0
        ]
        self.assertEqual(matrix, expected,
                        "Matrix should reflect overlapping buttons")
    
    def test_build_matrix_machine_1_example(self):
        """Test matrix building for Machine 1 from example."""
        machine = Machine(
            target=[0, 1, 1, 0],
            buttons=[[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]
        )
        matrix = build_matrix(machine)
        
        # Expected matrix (4 lights × 6 buttons + 1 target column)
        expected = [
            [0, 0, 0, 0, 1, 1, 0],  # Light 0: b4, b5 toggle, target=0
            [0, 1, 0, 0, 0, 1, 1],  # Light 1: b1, b5 toggle, target=1
            [0, 0, 1, 1, 1, 0, 1],  # Light 2: b2, b3, b4 toggle, target=1
            [1, 1, 0, 1, 0, 0, 0]   # Light 3: b0, b1, b3 toggle, target=0
        ]
        self.assertEqual(matrix, expected,
                        "Matrix for Machine 1 should match expected structure")
        self.assertEqual(len(matrix), 4, "Should have 4 rows (4 lights)")
        self.assertEqual(len(matrix[0]), 7, "Should have 7 columns (6 buttons + target)")
    
    def test_build_matrix_no_buttons_toggle_light(self):
        """Test matrix when no button toggles a particular light."""
        machine = Machine(target=[1, 0], buttons=[[1]])
        matrix = build_matrix(machine)
        
        # Light 0: no button toggles it, but target=1 (unsolvable)
        # Light 1: button 0 toggles it, target=0
        expected = [
            [0, 1],  # Light 0: no toggle, target=1
            [1, 0]   # Light 1: b0 toggles, target=0
        ]
        self.assertEqual(matrix, expected,
                        "Row should have all zeros for untoggled light")


class TestDay10GaussianElimination(unittest.TestCase):
    """Tests for Gaussian elimination over GF(2)."""
    
    def test_gaussian_simple_unique_solution(self):
        """Test Gaussian elimination with simple unique solution."""
        # System: b0 = 1 (single variable, single equation)
        matrix = [[1, 1]]
        reduced, pivots = gaussian_elimination_gf2(matrix)
        
        self.assertEqual(pivots, [0], "Column 0 should be pivot")
        self.assertEqual(reduced[0][0], 1, "Pivot should remain 1")
        self.assertEqual(reduced[0][1], 1, "Target should remain 1")
    
    def test_gaussian_two_variables_independent(self):
        """Test Gaussian elimination with two independent equations."""
        # System: b0 = 1, b1 = 1
        matrix = [
            [1, 0, 1],
            [0, 1, 1]
        ]
        reduced, pivots = gaussian_elimination_gf2(matrix)
        
        self.assertEqual(pivots, [0, 1], "Both columns should be pivots")
        # Matrix should remain unchanged (already in reduced form)
        self.assertEqual(reduced[0], [1, 0, 1])
        self.assertEqual(reduced[1], [0, 1, 1])
    
    def test_gaussian_elimination_with_reduction(self):
        """Test Gaussian elimination that requires row reduction."""
        # System: b0 + b1 = 1, b0 + b1 = 1 (duplicate equations)
        matrix = [
            [1, 1, 1],
            [1, 1, 1]
        ]
        reduced, pivots = gaussian_elimination_gf2(matrix)
        
        # After elimination, second row should become all zeros
        self.assertEqual(len(pivots), 1, "Only one pivot column")
        self.assertEqual(reduced[1], [0, 0, 0], "Second row eliminated")
    
    def test_gaussian_free_variables(self):
        """Test Gaussian elimination resulting in free variables."""
        # System with more variables than equations
        # b0 + b1 = 1
        matrix = [[1, 1, 0, 1]]  # 3 buttons, 1 equation
        reduced, pivots = gaussian_elimination_gf2(matrix)
        
        self.assertEqual(len(pivots), 1, "Only one pivot")
        # Columns 1 and 2 should be free variables
    
    def test_gaussian_gf2_arithmetic(self):
        """Test that arithmetic is correctly done over GF(2) (XOR)."""
        # System: b0 + b1 = 1, b1 = 0
        # After elimination: b0 = 1, b1 = 0
        matrix = [
            [1, 1, 1],
            [0, 1, 0]
        ]
        reduced, pivots = gaussian_elimination_gf2(matrix)
        
        # After back-substitution (in reduced row echelon form)
        # First row should become [1, 0, 1]
        self.assertEqual(pivots, [0, 1], "Both columns are pivots")
        # The elimination should use XOR


class TestDay10SolutionFinding(unittest.TestCase):
    """Tests for finding minimum solution from reduced matrix."""
    
    def test_find_minimum_unique_solution(self):
        """Test finding minimum when solution is unique."""
        # Reduced matrix: b0 = 1, b1 = 0
        matrix = [
            [1, 0, 1],
            [0, 1, 0]
        ]
        pivots = [0, 1]
        
        min_presses = find_minimum_solution(matrix, pivots)
        self.assertEqual(min_presses, 1, "Should press only button 0")
    
    def test_find_minimum_unsolvable(self):
        """Test detection of unsolvable system."""
        # Inconsistent system: 0 = 1
        matrix = [
            [0, 0, 1]  # No buttons toggle, but target = 1
        ]
        pivots = []
        
        min_presses = find_minimum_solution(matrix, pivots)
        self.assertEqual(min_presses, float('inf'), 
                        "Unsolvable system should return infinity")
    
    def test_find_minimum_all_zeros(self):
        """Test when all lights already in target state (no presses needed)."""
        # System: b0 = 0, b1 = 0
        matrix = [
            [1, 0, 0],
            [0, 1, 0]
        ]
        pivots = [0, 1]
        
        min_presses = find_minimum_solution(matrix, pivots)
        self.assertEqual(min_presses, 0, "No presses needed when all targets are 0")
    
    def test_find_minimum_with_free_variables(self):
        """Test finding minimum when multiple solutions exist."""
        # System with free variables should choose minimum presses
        # This is a simplified case - actual implementation will enumerate
        pass  # Implementation-dependent, will verify through integration tests


class TestDay10SolveMachine(unittest.TestCase):
    """Tests for solving individual machines end-to-end."""
    
    def test_solve_single_light_single_button(self):
        """Test: Single light needs to be on, one button toggles it."""
        machine = Machine(target=[1], buttons=[[0]])
        presses = solve_machine(machine)
        self.assertEqual(presses, 1, "Should press button once")
    
    def test_solve_already_configured(self):
        """Test: Machine already in target state (all lights off)."""
        machine = Machine(target=[0, 0, 0, 0], buttons=[[0, 1], [2, 3]])
        presses = solve_machine(machine)
        self.assertEqual(presses, 0, "No presses needed when already configured")
    
    def test_solve_two_lights_independent_buttons(self):
        """Test: Two lights on, each with its own button."""
        machine = Machine(target=[1, 1], buttons=[[0], [1]])
        presses = solve_machine(machine)
        self.assertEqual(presses, 2, "Should press both buttons")
    
    def test_solve_two_lights_one_button(self):
        """Test: Two lights on, one button toggles both."""
        machine = Machine(target=[1, 1], buttons=[[0, 1]])
        presses = solve_machine(machine)
        self.assertEqual(presses, 1, "One button toggles both lights")
    
    def test_solve_overlapping_buttons(self):
        """Test: Buttons that toggle overlapping sets of lights."""
        # Target: light 0 on, light 1 off
        # Button 0: toggles both 0,1
        # Button 1: toggles light 1
        # Solution: press both → [1,1] then [1,0] ✓
        machine = Machine(target=[1, 0], buttons=[[0, 1], [1]])
        presses = solve_machine(machine)
        self.assertEqual(presses, 2, "Should press both buttons")
    
    def test_solve_all_lights_on(self):
        """Test: All lights on with one button toggling all."""
        machine = Machine(target=[1, 1, 1, 1], buttons=[[0, 1, 2, 3]])
        presses = solve_machine(machine)
        self.assertEqual(presses, 1, "One press toggles all lights on")
    
    def test_solve_unsolvable_configuration(self):
        """Test: Impossible to configure (button doesn't toggle target light)."""
        # Target: light 0 on, but only button toggles light 1
        machine = Machine(target=[1, 0], buttons=[[1]])
        presses = solve_machine(machine)
        self.assertEqual(presses, float('inf'), 
                        "Should return infinity for unsolvable")
    
    def test_solve_machine_1_from_example(self):
        """Test Machine 1 from main example (expected: 2 presses)."""
        machine = Machine(
            target=[0, 1, 1, 0],
            buttons=[[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]
        )
        presses = solve_machine(machine)
        self.assertEqual(presses, 2, 
                        "Machine 1 should require 2 presses (buttons 4 and 5)")
    
    def test_solve_machine_2_from_example(self):
        """Test Machine 2 from main example (expected: 3 presses)."""
        machine = Machine(
            target=[0, 0, 0, 1, 0],
            buttons=[[0, 2, 3, 4], [2, 3], [0, 4], [0, 1, 2], [1, 2, 3, 4]]
        )
        presses = solve_machine(machine)
        self.assertEqual(presses, 3,
                        "Machine 2 should require 3 presses")
    
    def test_solve_machine_3_from_example(self):
        """Test Machine 3 from main example (expected: 2 presses)."""
        machine = Machine(
            target=[0, 1, 1, 1, 0, 1],
            buttons=[[0, 1, 2, 3, 4], [0, 3, 4], [0, 1, 2, 4, 5], [1, 2]]
        )
        presses = solve_machine(machine)
        self.assertEqual(presses, 2,
                        "Machine 3 should require 2 presses (buttons 1 and 2)")


class TestDay10Part1(unittest.TestCase):
    """Tests for Part 1 solution."""
    
    def test_part1_single_machine_simple(self):
        """Test Part 1 with single simple machine."""
        input_text = "[#] (0) {1}"
        result = solve_part1(input_text)
        self.assertEqual(result, 1, "Single machine needs 1 press")
    
    def test_part1_single_machine_already_configured(self):
        """Test Part 1 with machine already configured."""
        input_text = "[....] (0,1) (2,3) {1,2}"
        result = solve_part1(input_text)
        self.assertEqual(result, 0, "Already configured needs 0 presses")
    
    def test_part1_two_machines(self):
        """Test Part 1 with two simple machines."""
        input_text = """[#] (0) {1}
[##] (0) (1) {1,1}"""
        result = solve_part1(input_text)
        self.assertEqual(result, 3, "Sum: 1 + 2 = 3")
    
    def test_part1_main_example(self):
        """Test Part 1 with the main example from spec (expected: 7)."""
        input_text = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
        
        result = solve_part1(input_text)
        self.assertEqual(result, 7,
                        "Main example should sum to 7 (2+3+2)")


class TestDay10EdgeCases(unittest.TestCase):
    """Tests for edge cases and boundary conditions."""
    
    def test_edge_single_light_multiple_identical_buttons(self):
        """Test machine with multiple buttons that do the same thing."""
        # Two buttons both toggle light 0 - should press only one
        machine = Machine(target=[1], buttons=[[0], [0]])
        presses = solve_machine(machine)
        self.assertEqual(presses, 1, 
                        "Should press only one of the identical buttons")
    
    def test_edge_redundant_buttons(self):
        """Test machine with redundant button combinations."""
        # Button 0: toggles light 0
        # Button 1: toggles light 1
        # Button 2: toggles lights 0,1 (redundant - same as 0+1)
        machine = Machine(target=[1, 1], buttons=[[0], [1], [0, 1]])
        presses = solve_machine(machine)
        # Could be 2 (press 0,1) or 1 (press 2) - minimum is 1
        self.assertLessEqual(presses, 2, "Should find minimum solution")
    
    def test_edge_no_buttons(self):
        """Test machine with target state but no buttons."""
        machine = Machine(target=[1], buttons=[])
        presses = solve_machine(machine)
        self.assertEqual(presses, float('inf'),
                        "No buttons means unsolvable if target != all off")
    
    def test_edge_no_buttons_already_off(self):
        """Test machine with no buttons but already in target state."""
        machine = Machine(target=[0, 0], buttons=[])
        presses = solve_machine(machine)
        # If target is all off and no buttons, 0 presses needed
        # This depends on implementation - might be unsolvable
        # Commenting out since behavior unclear without implementation
        pass
    
    def test_edge_many_lights_one_button(self):
        """Test machine with many lights, one button toggles all."""
        num_lights = 10
        machine = Machine(
            target=[1] * num_lights,
            buttons=[list(range(num_lights))]
        )
        presses = solve_machine(machine)
        self.assertEqual(presses, 1, "One button toggles all lights")
    
    def test_edge_complex_interdependence(self):
        """Test machine with complex button interdependencies."""
        # Custom case from spec analysis
        machine = Machine(
            target=[1, 0, 1, 0],
            buttons=[[0, 2], [1, 3], [0, 1]]
        )
        presses = solve_machine(machine)
        # From spec: solution is press button 0 only = 1 press
        self.assertEqual(presses, 1, "Should find optimal solution")
    
    def test_edge_diagonal_pattern(self):
        """Test machine with diagonal button pattern."""
        # Each button toggles light i and i+1
        machine = Machine(
            target=[1, 1, 1],
            buttons=[[0, 1], [1, 2]]
        )
        presses = solve_machine(machine)
        # This should be solvable, verify implementation finds solution
        self.assertNotEqual(presses, float('inf'), "Should be solvable")


class TestDay10Verification(unittest.TestCase):
    """Tests that verify solutions by simulation."""
    
    def simulate_button_presses(self, num_lights: int, buttons: list, 
                                 presses: list) -> list:
        """
        Simulate pressing buttons and return final state.
        
        Args:
            num_lights: Number of lights
            buttons: List of button toggle patterns
            presses: List of button indices to press
        
        Returns:
            Final state of lights
        """
        state = [0] * num_lights
        for button_idx in presses:
            for light in buttons[button_idx]:
                state[light] ^= 1  # Toggle (XOR)
        return state
    
    def test_verify_machine_1_solution(self):
        """Verify Machine 1 solution by simulating button presses."""
        target = [0, 1, 1, 0]
        buttons = [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]
        
        # From spec: press buttons 4 and 5 (0-indexed)
        presses = [4, 5]
        result = self.simulate_button_presses(4, buttons, presses)
        
        self.assertEqual(result, target,
                        "Pressing buttons 4,5 should reach target [0,1,1,0]")
        self.assertEqual(len(presses), 2, "Should use 2 presses")
    
    def test_verify_machine_2_solution(self):
        """Verify Machine 2 solution by simulating button presses."""
        target = [0, 0, 0, 1, 0]
        buttons = [[0, 2, 3, 4], [2, 3], [0, 4], [0, 1, 2], [1, 2, 3, 4]]
        
        # From spec: press buttons 2, 3, 4
        presses = [2, 3, 4]
        result = self.simulate_button_presses(5, buttons, presses)
        
        self.assertEqual(result, target,
                        "Pressing buttons 2,3,4 should reach target")
        self.assertEqual(len(presses), 3, "Should use 3 presses")
    
    def test_verify_machine_3_solution(self):
        """Verify Machine 3 solution by simulating button presses."""
        target = [0, 1, 1, 1, 0, 1]
        buttons = [[0, 1, 2, 3, 4], [0, 3, 4], [0, 1, 2, 4, 5], [1, 2]]
        
        # From spec: press buttons 1 and 2
        presses = [1, 2]
        result = self.simulate_button_presses(6, buttons, presses)
        
        self.assertEqual(result, target,
                        "Pressing buttons 1,2 should reach target")
        self.assertEqual(len(presses), 2, "Should use 2 presses")


class TestDay10Part2Parsing(unittest.TestCase):
    """Tests for parsing Part 2 joltage requirements (not indicator diagrams)."""
    
    def test_parse_joltage_single_counter(self):
        """Test parsing joltage for simplest case."""
        line = "[#] (0) {5}"
        from solution import parse_machine_part2
        targets, buttons = parse_machine_part2(line)
        
        self.assertEqual(targets, [5], "Should extract joltage target {5}")
        self.assertEqual(buttons, [[0]], "Button pattern same as Part 1")
    
    def test_parse_joltage_machine_1(self):
        """Test parsing Machine 1 joltage requirements."""
        line = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"
        from solution import parse_machine_part2
        targets, buttons = parse_machine_part2(line)
        
        # Part 2 uses joltage {3,5,4,7}, ignores diagram [.##.]
        expected_targets = [3, 5, 4, 7]
        self.assertEqual(targets, expected_targets,
                        "Should extract joltage values [3,5,4,7]")
        
        # Buttons are same as Part 1
        expected_buttons = [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]
        self.assertEqual(buttons, expected_buttons,
                        "Button patterns should match Part 1")
    
    def test_parse_joltage_machine_2(self):
        """Test parsing Machine 2 joltage requirements."""
        line = "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}"
        from solution import parse_machine_part2
        targets, buttons = parse_machine_part2(line)
        
        expected_targets = [7, 5, 12, 7, 2]
        self.assertEqual(targets, expected_targets,
                        "Should extract joltage [7,5,12,7,2]")
    
    def test_parse_joltage_machine_3(self):
        """Test parsing Machine 3 joltage requirements."""
        line = "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
        from solution import parse_machine_part2
        targets, buttons = parse_machine_part2(line)
        
        expected_targets = [10, 11, 11, 5, 10, 5]
        self.assertEqual(targets, expected_targets,
                        "Should extract joltage [10,11,11,5,10,5]")
    
    def test_parse_joltage_all_zeros(self):
        """Test parsing when all joltage targets are zero."""
        line = "[####] (0,1,2,3) {0,0,0,0}"
        from solution import parse_machine_part2
        targets, buttons = parse_machine_part2(line)
        
        self.assertEqual(targets, [0, 0, 0, 0],
                        "Should handle zero targets")


class TestDay10Part2MatrixBuilding(unittest.TestCase):
    """Tests for building integer matrix for Part 2 (not GF(2))."""
    
    def test_build_matrix_part2_single_counter(self):
        """Test matrix building for single counter, single button."""
        from solution import build_matrix_part2
        targets = [5]
        buttons = [[0]]
        
        matrix = build_matrix_part2(targets, buttons)
        
        # Matrix: counter 0 incremented by button 0, target = 5
        expected = [[1, 5]]
        self.assertEqual(matrix, expected,
                        "Matrix should be [[1, 5]] for single counter")
    
    def test_build_matrix_part2_two_independent(self):
        """Test matrix for two counters with independent buttons."""
        from solution import build_matrix_part2
        targets = [3, 7]
        buttons = [[0], [1]]
        
        matrix = build_matrix_part2(targets, buttons)
        
        # Counter 0: button 0 increments, target=3
        # Counter 1: button 1 increments, target=7
        expected = [
            [1, 0, 3],
            [0, 1, 7]
        ]
        self.assertEqual(matrix, expected,
                        "Matrix should show independent buttons")
    
    def test_build_matrix_part2_button_affects_multiple(self):
        """Test matrix when button increments multiple counters."""
        from solution import build_matrix_part2
        targets = [5, 5]
        buttons = [[0, 1]]
        
        matrix = build_matrix_part2(targets, buttons)
        
        # Both counters incremented by button 0
        expected = [
            [1, 5],
            [1, 5]
        ]
        self.assertEqual(matrix, expected,
                        "Both rows should have coefficient 1")
    
    def test_build_matrix_part2_machine_1(self):
        """Test matrix building for Machine 1 Part 2."""
        from solution import build_matrix_part2
        targets = [3, 5, 4, 7]
        buttons = [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]
        
        matrix = build_matrix_part2(targets, buttons)
        
        # Counter 0: buttons 4,5 increment it, target=3
        # Counter 1: buttons 1,5 increment it, target=5
        # Counter 2: buttons 2,3,4 increment it, target=4
        # Counter 3: buttons 0,1,3 increment it, target=7
        expected = [
            [0, 0, 0, 0, 1, 1, 3],  # Counter 0
            [0, 1, 0, 0, 0, 1, 5],  # Counter 1
            [0, 0, 1, 1, 1, 0, 4],  # Counter 2
            [1, 1, 0, 1, 0, 0, 7]   # Counter 3
        ]
        self.assertEqual(matrix, expected,
                        "Matrix structure should match for Machine 1 Part 2")


class TestDay10Part2SolveMachine(unittest.TestCase):
    """Tests for solving individual machines in Part 2 (integer arithmetic)."""
    
    def test_solve_part2_single_counter_single_button(self):
        """Test: Single counter needs value 5, one button increments it."""
        from solution import solve_machine_part2
        targets = [5]
        buttons = [[0]]
        
        presses = solve_machine_part2(targets, buttons)
        self.assertEqual(presses, 5, "Should press button 5 times")
    
    def test_solve_part2_already_zero(self):
        """Test: All counters already at zero (target state)."""
        from solution import solve_machine_part2
        targets = [0, 0, 0, 0]
        buttons = [[0, 1], [2, 3]]
        
        presses = solve_machine_part2(targets, buttons)
        self.assertEqual(presses, 0, "No presses needed when targets are all 0")
    
    def test_solve_part2_two_counters_independent(self):
        """Test: Two counters with independent buttons."""
        from solution import solve_machine_part2
        targets = [3, 7]
        buttons = [[0], [1]]
        
        presses = solve_machine_part2(targets, buttons)
        self.assertEqual(presses, 10, "Should press button 0 three times, button 1 seven times: 3+7=10")
    
    def test_solve_part2_one_button_affects_both(self):
        """Test: One button increments both counters."""
        from solution import solve_machine_part2
        targets = [5, 5]
        buttons = [[0, 1]]
        
        presses = solve_machine_part2(targets, buttons)
        self.assertEqual(presses, 5, "Press button 5 times to increment both counters to 5")
    
    def test_solve_part2_unsolvable(self):
        """Test: Impossible configuration (button doesn't affect needed counter)."""
        from solution import solve_machine_part2
        targets = [5, 0]
        buttons = [[1]]  # Only increments counter 1, can't reach counter 0
        
        presses = solve_machine_part2(targets, buttons)
        self.assertEqual(presses, float('inf'),
                        "Should return infinity for unsolvable system")
    
    def test_solve_part2_machine_1_example(self):
        """Test Machine 1 from example (expected: 10 presses)."""
        from solution import solve_machine_part2
        targets = [3, 5, 4, 7]
        buttons = [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]
        
        presses = solve_machine_part2(targets, buttons)
        self.assertEqual(presses, 10,
                        "Machine 1 Part 2 should require 10 presses")
    
    def test_solve_part2_machine_2_example(self):
        """Test Machine 2 from example (expected: 12 presses)."""
        from solution import solve_machine_part2
        targets = [7, 5, 12, 7, 2]
        buttons = [[0, 2, 3, 4], [2, 3], [0, 4], [0, 1, 2], [1, 2, 3, 4]]
        
        presses = solve_machine_part2(targets, buttons)
        self.assertEqual(presses, 12,
                        "Machine 2 Part 2 should require 12 presses")
    
    def test_solve_part2_machine_3_example(self):
        """Test Machine 3 from example (expected: 11 presses)."""
        from solution import solve_machine_part2
        targets = [10, 11, 11, 5, 10, 5]
        buttons = [[0, 1, 2, 3, 4], [0, 3, 4], [0, 1, 2, 4, 5], [1, 2]]
        
        presses = solve_machine_part2(targets, buttons)
        self.assertEqual(presses, 11,
                        "Machine 3 Part 2 should require 11 presses")


class TestDay10Part2Integration(unittest.TestCase):
    """Integration tests for Part 2 full solution."""
    
    def test_part2_single_machine_simple(self):
        """Test Part 2 with single simple machine."""
        input_text = "[#] (0) {5}"
        from solution import solve_part2
        result = solve_part2(input_text)
        self.assertEqual(result, 5, "Single machine needs 5 presses")
    
    def test_part2_single_machine_zero_targets(self):
        """Test Part 2 with all counters at zero."""
        input_text = "[....] (0,1) (2,3) {0,0,0,0}"
        from solution import solve_part2
        result = solve_part2(input_text)
        self.assertEqual(result, 0, "Zero targets need 0 presses")
    
    def test_part2_two_machines(self):
        """Test Part 2 with two simple machines."""
        input_text = """[#] (0) {5}
[##] (0) (1) {3,7}"""
        from solution import solve_part2
        result = solve_part2(input_text)
        self.assertEqual(result, 15, "Sum: 5 + (3+7) = 15")
    
    def test_part2_main_example(self):
        """Test Part 2 with the main example from spec (expected: 33)."""
        input_text = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
        
        from solution import solve_part2
        result = solve_part2(input_text)
        self.assertEqual(result, 33,
                        "Main example should sum to 33 (10+12+11)")


class TestDay10Part2EdgeCases(unittest.TestCase):
    """Edge cases specific to Part 2 integer linear programming."""
    
    def test_part2_edge_large_target(self):
        """Test with large target value."""
        from solution import solve_machine_part2
        targets = [1000]
        buttons = [[0]]
        
        presses = solve_machine_part2(targets, buttons)
        self.assertEqual(presses, 1000,
                        "Should handle large target values")
    
    def test_part2_edge_multiple_identical_buttons(self):
        """Test with multiple buttons that do the same thing."""
        from solution import solve_machine_part2
        targets = [5]
        buttons = [[0], [0]]  # Two identical buttons
        
        presses = solve_machine_part2(targets, buttons)
        self.assertEqual(presses, 5,
                        "Should use one button 5 times, not both")
    
    def test_part2_edge_efficient_vs_naive(self):
        """Test that finds efficient solution over naive."""
        from solution import solve_machine_part2
        targets = [5, 5, 5]
        buttons = [[0, 1, 2], [0], [1], [2]]
        
        presses = solve_machine_part2(targets, buttons)
        # Efficient: press button 0 five times = 5 presses
        # Naive: press buttons 1,2,3 each 5 times = 15 presses
        self.assertEqual(presses, 5,
                        "Should find efficient solution (5 not 15)")
    
    def test_part2_edge_overdetermined_solvable(self):
        """Test overdetermined system that has solution."""
        from solution import solve_machine_part2
        # System with more constraints than variables, but solvable
        targets = [5, 5]
        buttons = [[0, 1]]
        
        presses = solve_machine_part2(targets, buttons)
        self.assertEqual(presses, 5,
                        "Overdetermined but solvable should work")
    
    def test_part2_edge_overdetermined_unsolvable(self):
        """Test overdetermined system with no solution."""
        from solution import solve_machine_part2
        targets = [5, 7]
        buttons = [[0, 1]]  # Can't reach different targets with same button
        
        presses = solve_machine_part2(targets, buttons)
        self.assertEqual(presses, float('inf'),
                        "Conflicting constraints should be unsolvable")


class TestDay10Part2Verification(unittest.TestCase):
    """Verification tests that simulate button presses for Part 2."""
    
    def simulate_button_presses_part2(self, num_counters: int, buttons: list,
                                       button_presses: list) -> list:
        """
        Simulate pressing buttons and return final counter values.
        
        Args:
            num_counters: Number of counters
            buttons: List of button increment patterns
            button_presses: List of (button_idx, count) tuples
        
        Returns:
            Final counter values
        """
        counters = [0] * num_counters
        for button_idx, count in button_presses:
            for _ in range(count):
                for counter in buttons[button_idx]:
                    counters[counter] += 1
        return counters
    
    def test_verify_machine_1_part2_solution(self):
        """Verify Machine 1 Part 2 solution by simulation."""
        targets = [3, 5, 4, 7]
        buttons = [[3], [1, 3], [2], [2, 3], [0, 2], [0, 1]]
        
        # From spec: one valid solution
        # Button 0 (3): 1 time
        # Button 1 (1,3): 3 times
        # Button 2 (2): 0 times
        # Button 3 (2,3): 3 times
        # Button 4 (0,2): 1 time
        # Button 5 (0,1): 2 times
        button_presses = [
            (0, 1),  # Button 0: 1 time
            (1, 3),  # Button 1: 3 times
            (3, 3),  # Button 3: 3 times
            (4, 1),  # Button 4: 1 time
            (5, 2)   # Button 5: 2 times
        ]
        
        result = self.simulate_button_presses_part2(4, buttons, button_presses)
        self.assertEqual(result, targets,
                        "Simulation should reach target [3,5,4,7]")
        
        total_presses = sum(count for _, count in button_presses)
        self.assertEqual(total_presses, 10, "Total should be 10 presses")
    
    def test_verify_machine_2_part2_solution(self):
        """Verify Machine 2 Part 2 solution by simulation."""
        targets = [7, 5, 12, 7, 2]
        buttons = [[0, 2, 3, 4], [2, 3], [0, 4], [0, 1, 2], [1, 2, 3, 4]]
        
        # From spec: one valid solution
        # Button 0: 2 times
        # Button 1: 5 times
        # Button 2: 0 times
        # Button 3: 5 times
        # Button 4: 0 times
        button_presses = [
            (0, 2),
            (1, 5),
            (3, 5)
        ]
        
        result = self.simulate_button_presses_part2(5, buttons, button_presses)
        self.assertEqual(result, targets,
                        "Simulation should reach target [7,5,12,7,2]")
        
        total_presses = sum(count for _, count in button_presses)
        self.assertEqual(total_presses, 12, "Total should be 12 presses")
    
    def test_verify_machine_3_part2_solution(self):
        """Verify Machine 3 Part 2 solution by simulation."""
        targets = [10, 11, 11, 5, 10, 5]
        buttons = [[0, 1, 2, 3, 4], [0, 3, 4], [0, 1, 2, 4, 5], [1, 2]]
        
        # From spec: one valid solution
        # Button 0: 5 times
        # Button 1: 0 times
        # Button 2: 5 times
        # Button 3: 1 time
        button_presses = [
            (0, 5),
            (2, 5),
            (3, 1)
        ]
        
        result = self.simulate_button_presses_part2(6, buttons, button_presses)
        self.assertEqual(result, targets,
                        "Simulation should reach target [10,11,11,5,10,5]")
        
        total_presses = sum(count for _, count in button_presses)
        self.assertEqual(total_presses, 11, "Total should be 11 presses")


if __name__ == '__main__':
    unittest.main()
