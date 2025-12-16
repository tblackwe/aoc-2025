# Day 12: Christmas Tree Farm

## Problem Description

Help the Elves determine how many regions under Christmas trees can fit all their required presents. This is a 2D bin packing problem where presents (polyominoes) with standard shapes must fit into rectangular regions. Presents can be rotated and flipped, and their empty spaces don't block other presents.

## Input

The input is located in `input.txt`

## Input Format

The input consists of two sections:

**Section 1: Present Shapes**
- Each shape starts with an index number followed by a colon
- Shape is displayed as ASCII art where `#` = part of shape, `.` = empty space
- Empty spaces don't block other presents from using those grid positions
- Shapes can be rotated (90°, 180°, 270°) and flipped

**Section 2: Regions** 
- Format: `WIDTHxHEIGHT: count0 count1 count2 ...`
- Dimensions define the rectangular region size
- Counts indicate how many of each shape (by index) must fit in that region

Example:
```
0:
###
##.
##.

1:
###
##.
.##

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
```

## Output Format

**Part 1**: Integer count of regions that can fit all their required presents.

Example:
```
2
```

## Requirements

### Part 1

Determine how many regions can fit all of their listed presents.

**Rules**:
1. Presents can be rotated (90°, 180°, 270°) and flipped (horizontal/vertical)
2. The `#` parts of different presents cannot overlap
3. The `.` parts are just empty space in the shape's bounding box - they don't block other presents
4. All presents must fit completely within the region boundaries
5. Presents must align to the grid (one unit per cell)
6. All required presents for a region must fit simultaneously

#### Part 1 Example Answer
2

**Explanation:**

Given 6 shapes (indices 0-5) and 3 regions:

**Region 1**: `4x4: 0 0 0 0 2 0` - needs 2 copies of shape 4
- Shape 4 is:
  ```
  ###
  #..
  ###
  ```
- A 4x4 grid can fit both presents:
  ```
  AAA.
  ABAB
  ABAB
  .BBB
  ```
- **FEASIBLE** ✓

**Region 2**: `12x5: 1 0 1 0 2 2` - needs shapes 0(×1), 2(×1), 4(×2), 5(×2)
- All 6 presents fit (one arrangement shown in puzzle):
  ```
  ....AAAFFE.E
  .BBBAAFFFEEE
  DDDBAAFFCECE
  DBBB....CCC.
  DDD.....C.C.
  ```
- **FEASIBLE** ✓

**Region 3**: `12x5: 1 0 1 0 3 2` - needs shapes 0(×1), 2(×1), 4(×3), 5(×2)
- Same size as region 2, but needs one more shape 4
- No matter how arranged, all 7 presents cannot fit
- **NOT FEASIBLE** ✗

Result: 2 regions out of 3 are feasible.

### Part 2

Part 2 requirements will be revealed after completing Part 1.

#### Part 2 Example Answer
TBD

**Explanation:**
TBD

## Algorithm Analysis

### Problem Type
**2D Bin Packing with Polyominoes** - an NP-complete problem. We need to determine feasibility (yes/no) rather than optimize packing.

### Recommended Approach: Backtracking with Constraint Propagation

**Time Complexity**: O(n! × w × h × 8) where n = number of presents, w×h = region size, 8 = max orientations
**Space Complexity**: O(w × h) for grid representation

**Algorithm**:
1. Parse shapes and generate all rotations/flips (up to 8 variations per shape)
2. For each region:
   - Build list of presents to place
   - Use backtracking to try placing each present
   - For each present, try all orientations and positions
   - If all presents placed successfully, region is feasible
   - Otherwise, backtrack and try different placements
3. Count successful regions

**Key Optimizations**:
- **Area pruning**: Skip if total present area > region area
- **Place large/constrained pieces first**: Better pruning
- **Deduplicate orientations**: Some rotations/flips produce identical shapes
- **Early termination**: Stop searching a region once solution found
- **Fast overlap checking**: Use set operations for O(1) membership

### Implementation Steps

1. **Parse input**: Extract shapes as coordinate lists, extract region specifications
2. **Generate orientations**: For each shape, compute all unique rotations/flips
3. **Normalize shapes**: Translate each orientation to start at (0,0)
4. **Backtracking solver**: Try placing presents recursively
5. **Count feasible regions**: Increment counter for each successful placement

## Test Cases

### Part 1 Tests

| Input | Expected | Notes |
|-------|----------|-------|
| Example from puzzle (6 shapes, 3 regions) | `2` | Main example - regions 1 and 2 feasible |
| Empty region (0 presents required) | Feasible | Edge case: nothing to place |
| Single 1×1 present in 1×1 region | Feasible | Exact fit |
| Single 3×3 present in 2×2 region | Not feasible | Present too large |
| Area check: 10 1×1 presents in 3×3 region | Not feasible | Total area (10) > region area (9) |
| Multiple copies of same shape | Varies | Test shape rotation/arrangement |

### Part 2 Tests

TBD (Part 2 not yet revealed)

### Step-by-Step Trace (for validation)

**Example: Region 1 from puzzle** (`4x4: 0 0 0 0 2 0`)

Shape 4:
```
###
#..
###
```

Initial 4×4 grid:
```
....
....
....
....
```

Step 1: Place first copy of shape 4 at (0,0):
```
###.
#...
###.
....
```

Step 2: Try to place second copy. Position (0,3) won't work (out of bounds).
Try position (1,1):
```
###.
#.##
###.
..##
```
Overlap detected! Backtrack.

Step 3: Try second copy at position (2,1) after rotating:
```
AAA.
ABAB
ABAB
.BBB
```
Success! Both presents placed.

Result: **FEASIBLE**

## Data Structures

```python
# Shape: List of (row, col) coordinates of '#' cells
Shape = List[Tuple[int, int]]

# Grid: Set of occupied (row, col) positions
Grid = Set[Tuple[int, int]]

# Region specification
Region = {
    'width': int,
    'height': int,
    'required': List[int]  # Count of each shape index
}
```

## Key Functions

```python
def parse_input(input_text: str) -> Tuple[List[Shape], List[Region]]:
    """Parse shapes and regions from input."""
    pass

def get_all_orientations(shape: Shape) -> List[Shape]:
    """Generate all unique rotations and flips of a shape."""
    # 8 possible: original, rotate 90/180/270, flip H, flip H + rotate 90/180/270
    # Deduplicate and normalize to (0,0) origin
    pass

def can_place(grid: Grid, shape: Shape, row: int, col: int, width: int, height: int) -> bool:
    """Check if shape can be placed at position without overlap or going out of bounds."""
    pass

def solve_region(shapes: List[Shape], region: Region) -> bool:
    """Determine if all required presents can fit in the region."""
    pass

def backtrack(grid: Grid, orientations_list: List[List[Shape]], pieces: List[int], 
              idx: int, width: int, height: int) -> bool:
    """Recursively try to place all pieces."""
    pass
```

## Common Gotchas

1. **Empty space confusion**: `.` in shape definition doesn't block other presents!
2. **Normalization**: Always normalize shapes to (0,0) after transformations
3. **Orientation deduplication**: A square has only 1 unique orientation, not 8
4. **Boundary checking**: Check both that shape fits and doesn't go out of bounds
5. **Backtracking**: Must properly remove shapes from grid when backtracking
6. **Area optimization**: Quick rejection if sum of present areas > region area
7. **Coordinate system**: Be consistent (row, col) vs (x, y)
8. **Off-by-one**: Region `4x4` means indices 0-3, not 1-4

## Complexity Considerations

**Actual puzzle input**: ~1000 regions, 6 shapes, up to ~60 presents per region, regions up to 50×50

**Worst case per region**: O(60! × 50 × 50 × 8) - astronomically large
**Practical case**: Heavy pruning makes this tractable:
- Area constraints eliminate many attempts immediately
- Pieces placed reduce remaining search space exponentially  
- Most branches fail quickly
- Expected runtime: < 1 minute for all regions with good heuristics

**If too slow, consider**:
- Better placement ordering heuristics (largest/most constrained first)
- Symmetry breaking (don't try equivalent positions)
- Parallel processing of independent regions
- Dancing Links (DLX) algorithm for exact cover
- Caching of failed partial configurations
