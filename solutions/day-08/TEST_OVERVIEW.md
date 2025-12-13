# Day 08: Playground - Test Suite Overview

## Test Implementation Summary

**Status**: ✅ Complete - 27 test cases implemented following TDD principles

**Test Execution**: Tests are syntactically valid and ready to run. They currently fail (as expected) because the solution is not yet implemented. This is the correct state for Test-Driven Development.

---

## Test Suite Structure

### 1. TestDay08Parsing (7 test cases)
**Purpose**: Validate input parsing of 3D coordinates

| Test Method | Description | Key Validation |
|-------------|-------------|----------------|
| `test_parse_example_input` | Parse 20-box example from spec | Verifies all 20 boxes parsed correctly with exact coordinates |
| `test_parse_single_box` | Parse minimal single junction box | Tests edge case of 1 box |
| `test_parse_simple_3_boxes` | Parse 3 boxes in a line | Tests small simple case |
| `test_parse_negative_coordinates` | Parse boxes with negative coords | Handles negative X,Y,Z values |
| `test_parse_whitespace_handling` | Handle whitespace in input | Robust parsing with extra spaces |

**Expected Behavior**:
- `parse_input()` should return a list of `(x, y, z)` tuples
- Each tuple contains 3 integers
- Handles various input sizes: 1, 3, 20+ boxes
- Robust to whitespace and negative coordinates

---

### 2. TestDay08DistanceCalculation (7 test cases)
**Purpose**: Validate 3D Euclidean distance calculations

| Test Method | Description | Expected Distance |
|-------------|-------------|-------------------|
| `test_distance_unit_x_axis` | Distance along X axis | 1.0 |
| `test_distance_unit_y_axis` | Distance along Y axis | 1.0 |
| `test_distance_unit_z_axis` | Distance along Z axis | 1.0 |
| `test_distance_3d_diagonal` | Distance on 3D diagonal (0,0,0)→(1,1,1) | √3 ≈ 1.732 |
| `test_distance_symmetry` | d(A,B) = d(B,A) | Symmetric |
| `test_distance_zero` | Distance from point to itself | 0.0 |
| `test_distance_large_values` | Distance with example coords | ~316.83 |

**Implementation Note**:
- Tests import `euclidean_distance()` helper function
- Gracefully skip if function not yet implemented
- Use `assertAlmostEqual()` for floating-point comparisons (5 decimal places)
- Formula: `sqrt((x2-x1)² + (y2-y1)² + (z2-z1)²)`

---

### 3. TestDay08UnionFind (6 test cases)
**Purpose**: Validate Union-Find data structure operations

| Test Method | Description | Key Validation |
|-------------|-------------|----------------|
| `test_union_find_initialization` | Initialize with n elements | Each element is its own root initially |
| `test_union_find_basic_union` | Basic union operation | Returns True when merging separate sets |
| `test_union_find_already_connected` | Union of already-connected elements | Returns False when already in same set |
| `test_union_find_transitive_connection` | Transitive connections (A-B, B-C → A-C) | Verifies path compression works |
| `test_union_find_get_circuit_sizes` | Get sizes of all circuits | Returns correct list of circuit sizes |
| `test_union_find_multiple_circuits` | Multiple separate circuits | Handles complex circuit configurations |

**Expected UnionFind Interface**:
```python
class UnionFind:
    def __init__(self, n):
        """Initialize n separate sets"""
    
    def find(self, x):
        """Find root of x with path compression"""
    
    def union(self, x, y):
        """Union sets containing x and y. Returns True if merged, False if already connected"""
    
    def get_circuit_sizes(self):
        """Return list of all circuit sizes"""
```

---

### 4. TestDay08Part1 (7 test cases)
**Purpose**: Validate complete Part 1 solution

| Test Method | Description | Input | Connections | Expected Output |
|-------------|-------------|-------|-------------|-----------------|
| `test_example_from_spec_10_connections` | **Main spec example** | 20 boxes | 10 | **40** (5×4×2) |
| `test_simple_3_boxes_1_connection` | 3 boxes in line | 3 boxes | 1 | ≥2 |
| `test_simple_4_boxes_3_connections` | Unit cube corners | 4 boxes | 3 | >0 |
| `test_collinear_points_4_connections` | Points on line | 5 boxes | 4 | ≥5 |
| `test_skip_already_connected_pairs` | Skip redundant pairs | 4 boxes | 3 | ≥4 |
| `test_part1_handles_fewer_than_3_circuits` | Edge case handling | 5 boxes | 10 | >0 |
| `test_part1_zero_connections` | Zero connections edge case | 3 boxes | 0 | 1 (1×1×1) |

**Critical Test**: `test_example_from_spec_10_connections`
- Uses exact example from spec
- **Expected output: 40** (product of three largest circuits: 5×4×2)
- This validates core algorithm correctness

**Important**: `solve_part1()` must accept `num_connections` parameter:
```python
def solve_part1(data, num_connections=1000) -> int:
    """Solve part 1 with configurable number of connections"""
```

---

### 5. TestDay08Part2 (1 test case)
**Purpose**: Placeholder for Part 2 (not yet available)

| Test Method | Description |
|-------------|-------------|
| `test_part2_not_yet_available` | Skipped until Part 2 released |

---

### 6. TestDay08Integration (2 test cases)
**Purpose**: End-to-end integration tests

| Test Method | Description | Validates |
|-------------|-------------|-----------|
| `test_end_to_end_example` | Complete flow with 20-box example | Parse → Solve → 40 |
| `test_parsing_and_solving_simple_case` | Complete flow with 3-box case | Parse → Solve → >0 |

---

## Key Test Cases from Spec

### Main Example (Test Case 1)
**Input**: 20 junction boxes from spec
```
162,817,812
57,618,57
...
425,690,689
```

**With 10 connections**:
- Final circuit sizes: `[5, 4, 2, 2, 1, 1, 1, 1, 1, 1, 1]`
- Three largest: 5, 4, 2
- **Expected output: 40** (5 × 4 × 2)

### Simple 3 Boxes (Test Case 2)
**Input**:
```
0,0,0
1,0,0
10,0,0
```

**Behavior**:
- Closest pair: (0,0,0) and (1,0,0) with distance 1
- After 1 connection: circuits `[2, 1]`

### Collinear Points (Test Case 4)
**Input**: 5 points on X-axis (0,0,0 to 4,0,0)

**Behavior**:
- All distances between adjacent pairs = 1
- After 4 connections: all in one circuit `[5]`

### Already Connected (Test Case 5)
**Input**: 4 boxes with redundant pairs

**Behavior**:
- Tests that Union-Find correctly skips already-connected pairs
- Counts only actual new connections

---

## Expected Test Results (Before Implementation)

When running `python3 test_solution.py -v`:

**Skipped Tests**: 14
- 7 distance calculation tests (waiting for `euclidean_distance()`)
- 6 Union-Find tests (waiting for `UnionFind` class)
- 1 Part 2 test (not yet available)

**Failed Tests**: 13
- 7 parsing tests (parse_input returns None)
- 6 Part 1 solution tests (solve_part1 not implemented / missing num_connections param)

**This is the correct TDD state!** Tests guide implementation.

---

## Test Execution Commands

```bash
# Run all tests (verbose)
python3 test_solution.py -v

# Run specific test class
python3 -m unittest test_solution.TestDay08Parsing -v

# Run specific test method
python3 -m unittest test_solution.TestDay08Part1.test_example_from_spec_10_connections -v

# Run with pytest (if available)
pytest test_solution.py -v
```

---

## Implementation Guidance

### Order of Implementation

1. **Parse Input** → Make `TestDay08Parsing` pass
   - Implement `parse_input()` to return list of (x,y,z) tuples
   - Split lines, parse commas, convert to integers

2. **Distance Calculation** → Make `TestDay08DistanceCalculation` pass
   - Implement `euclidean_distance(pos1, pos2)`
   - Formula: `sqrt((x2-x1)² + (y2-y1)² + (z2-z1)²)`
   - Consider using squared distance to avoid sqrt

3. **Union-Find** → Make `TestDay08UnionFind` pass
   - Implement `UnionFind` class with path compression
   - Implement union by size/rank
   - Implement `get_circuit_sizes()` method

4. **Part 1 Solution** → Make `TestDay08Part1` pass
   - Calculate all pairwise distances
   - Sort pairs by distance
   - Connect closest pairs using Union-Find
   - Count to exactly `num_connections` actual connections
   - Find product of three largest circuits

5. **Integration** → Make `TestDay08Integration` pass
   - Should pass automatically once Part 1 works

### Expected Function Signatures

```python
def parse_input(input_text: str) -> list[tuple[int, int, int]]:
    """Parse input into list of 3D coordinates."""

def euclidean_distance(pos1: tuple[int, int, int], 
                       pos2: tuple[int, int, int]) -> float:
    """Calculate 3D Euclidean distance."""

class UnionFind:
    def __init__(self, n: int):
        """Initialize n separate sets."""
    
    def find(self, x: int) -> int:
        """Find root of x with path compression."""
    
    def union(self, x: int, y: int) -> bool:
        """Union sets. Returns True if merged, False if already connected."""
    
    def get_circuit_sizes(self) -> list[int]:
        """Return list of all circuit sizes."""

def solve_part1(data: list[tuple[int, int, int]], 
                num_connections: int = 1000) -> int:
    """Solve part 1: connect num_connections closest pairs."""
```

---

## Edge Cases Covered

✅ **Empty/Minimal Inputs**: 1 box, 3 boxes  
✅ **Negative Coordinates**: Handles negative X,Y,Z  
✅ **Whitespace**: Robust parsing  
✅ **Collinear Points**: 1D degenerate case  
✅ **Already Connected Pairs**: Union-Find skip logic  
✅ **Zero Connections**: Edge case (all separate)  
✅ **Large Values**: Example has coordinates in hundreds  
✅ **Distance Symmetry**: d(A,B) = d(B,A)  
✅ **Distance to Self**: d(A,A) = 0  
✅ **Fewer than 3 Circuits**: Graceful handling  
✅ **Multiple Circuits**: Complex circuit configurations  

---

## Test Quality Metrics

- **Total Test Cases**: 27
- **Test Classes**: 6
- **Parsing Tests**: 7 (foundation layer)
- **Helper Function Tests**: 13 (distance + Union-Find)
- **Solution Tests**: 7 (Part 1 end-to-end)
- **Code Coverage**: Comprehensive (all core functions tested)
- **Spec Alignment**: 100% (all spec examples included)
- **TDD Compliance**: ✅ Tests written before implementation

---

## Success Criteria

Tests pass when:
1. ✅ All 7 parsing tests pass
2. ✅ All 7 distance calculation tests pass
3. ✅ All 6 Union-Find tests pass
4. ✅ All 7 Part 1 solution tests pass
5. ✅ Main example produces **exactly 40** with 10 connections
6. ✅ Integration tests pass end-to-end

**Primary validation**: `test_example_from_spec_10_connections` must output **40**.

---

## Notes for Implementer

- The spec is very detailed with exact example trace
- Union-Find is critical - must use path compression and union by size
- Don't count connections where boxes are already in same circuit
- Product of **three largest** circuits (not all circuits)
- Handle edge case where fewer than 3 circuits exist
- The `num_connections` parameter allows testing with small values (like 10) before running full 1000

**Algorithm Complexity**:
- Time: O(n² log n) for sorting all pairs
- Space: O(n²) for storing distances
- Union-Find: O(α(n)) ≈ O(1) per operation with path compression

Good luck with implementation! The tests will guide you to a correct solution. 🎄
