# Day 07: Laboratories - Test Suite Overview

## Summary
Comprehensive unit test suite for the tachyon beam simulation puzzle, following TDD principles.

**Total Tests: 26**
- ✅ All tests currently FAIL (expected - no implementation yet)
- ✅ Tests follow TDD: written BEFORE implementation
- ✅ Clear test names and documentation
- ✅ Helpful assertion messages

## Test Categories

### 1. TestDay07Parsing (5 tests)
Tests input parsing logic for grid structure, start position, and splitters.

- `test_parse_example_input` - Main 16x15 grid from spec
- `test_parse_simple_grid` - Simple grid with one splitter
- `test_parse_no_splitters` - Grid with no splitters
- `test_parse_start_at_left_edge` - Start at column 0
- `test_parse_start_at_right_edge` - Start at last column

**Key Validations:**
- Grid dimensions are identified
- Start position (S) is found
- All splitter positions (^) are catalogued
- Edge positions are handled correctly

---

### 2. TestDay07Part1 (14 tests)
Tests the core beam simulation and split counting logic.

#### Main Example Test
- `test_example_from_spec` - **Main spec example: expects 21 splits**

#### Basic Functionality Tests
- `test_single_splitter` - One splitter, expects 1 split
- `test_no_splitters` - No splitters, expects 0 splits
- `test_two_splitters_adjacent` - Beam passes between splitters, expects 0
- `test_vertical_stack_splitters` - Stacked splitters with merging, expects 3

#### Beam Behavior Tests
- `test_beam_merging` - Two beams merge at same position, expects 2
- `test_complex_merging_pattern` - Multiple merge scenarios, expects 3
- `test_beam_misses_all_splitters` - No hits, expects 0

#### Edge Case Tests
- `test_edge_case_start_at_column_zero` - Split at left edge, expects 1
- `test_edge_case_start_at_last_column` - Split at right edge, expects 1
- `test_splitter_on_last_row` - Splitter on bottom row, expects 1
- `test_single_row_grid` - Minimal grid (1 row), expects 0
- `test_empty_grid_below_start` - Many empty rows, expects 0
- `test_all_beams_exit_at_edges` - Beams exit after split, expects 1

**Key Validations:**
- Beams travel downward through grid
- Splits create two new beams (left and right)
- Beams merge when reaching same position
- Out-of-bounds beams are handled
- Split count is accurate

---

### 3. TestDay07EdgeCases (5 tests)
Additional robustness and stress tests.

- `test_wide_grid_single_beam` - Very wide grid (47 columns), expects 1
- `test_narrow_grid` - Minimal width (3 columns), expects 1
- `test_multiple_splitters_same_row` - Multiple splitters inline, expects 1
- `test_beam_splits_then_merges_then_splits_again` - Complex pattern, expects 5
- `test_maximum_edge_splits` - Cascading edge splits, expects 5

**Key Validations:**
- Handles extreme grid sizes
- Multiple splitters on same row
- Complex split-merge-split patterns
- Performance with many beams

---

### 4. TestDay07Part2 (2 tests)
Placeholder tests for Part 2 (requirements TBD).

- `test_example_from_spec_part2` - Main example (placeholder)
- `test_simple_case_part2` - Simple case (placeholder)

**Status:** These tests pass currently (return None) and will be updated once Part 2 is revealed.

---

## Key Test Scenarios Covered

### Beam Physics
✅ Downward movement
✅ Splitting on splitter (^)
✅ Beam merging (same position)
✅ Beam exit (bottom edge, out of bounds)

### Edge Cases
✅ Start at grid edges (left/right)
✅ Splitters at grid edges
✅ Splitters on last row
✅ Empty grids or single row
✅ Beams passing between splitters
✅ Out-of-bounds handling

### Complex Scenarios
✅ Vertical stacking with merging
✅ Multiple merge events
✅ Wide and narrow grids
✅ Multiple splitters per row
✅ Cascading splits

---

## Running the Tests

### Run all tests:
```bash
python3 -m unittest test_solution.py
```

### Run with verbose output:
```bash
python3 -m unittest test_solution.py -v
```

### Run specific test class:
```bash
python3 -m unittest test_solution.TestDay07Part1 -v
```

### Run specific test:
```bash
python3 -m unittest test_solution.TestDay07Part1.test_example_from_spec -v
```

---

## Expected Behavior (TDD)

### Before Implementation:
- ❌ 24 tests FAIL (parse_input and solve_part1 return None)
- ✅ 2 tests PASS (solve_part2 placeholders)
- This is CORRECT for TDD!

### After Implementation:
- ✅ All 26 tests should PASS
- Tests validate correctness
- Edge cases are handled

---

## Test Data Examples

### Main Example (21 splits)
```
.......S.......
...............
.......^.......  <- 1 split
...............
......^.^......  <- 2 splits
...............
.....^.^.^.....  <- 3 splits
...............
....^.^...^....  <- 4 splits
...............
...^.^...^.^...  <- 5 splits
...............
..^...^.....^..  <- 5 splits (merging)
...............
.^.^.^.^.^...^.  <- 1 split
...............
```

### Simple Example (3 splits)
```
...S...
.......
...^...  <- 1 split (beams to col 2, 4)
.......
..^.^..  <- 2 splits (both beams hit)
.......
Total: 3 splits
```

---

## Implementation Hints

The tests expect these function signatures:

```python
def parse_input(input_text: str):
    """
    Parse grid and return data structure containing:
    - Grid dimensions (rows, cols)
    - Start position (row, col)
    - Splitter positions (set or list)
    """
    pass

def solve_part1(data) -> int:
    """
    Simulate beam travel and return split count.
    
    Algorithm:
    1. Start with beam at start position
    2. Track active beams by column (per row)
    3. Process row by row:
       - Check if beam hits splitter
       - If yes: increment counter, create two new beams
       - If no: beam continues to next row
    4. Merge beams at same column
    5. Remove out-of-bounds beams
    6. Return total split count
    """
    pass

def solve_part2(data) -> int | None:
    """Part 2 implementation (TBD)"""
    return None
```

---

## Next Steps

1. ✅ Tests are written (COMPLETE)
2. ⬜ Implement `parse_input()` function
3. ⬜ Implement `solve_part1()` function
4. ⬜ Run tests - all should pass
5. ⬜ Solve Part 2 when revealed
6. ⬜ Update Part 2 tests with actual requirements

---

## Notes

- Tests are comprehensive and cover 26 different scenarios
- All edge cases from spec are included
- Test names are descriptive and self-documenting
- Each test has detailed docstrings explaining expected behavior
- Assertion messages provide helpful debugging info
- Tests follow TDD principles (fail first, pass after implementation)
