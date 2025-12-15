# Day 9: Movie Theater

## Problem Description

The challenge is to find the **largest rectangle** that can be formed using red tiles in a grid as **opposite corners**. Given a list of red tile coordinates, we need to find which pair of tiles creates the rectangle with the maximum area.

This is a **geometric computation and combinatorics problem** that requires:
1. Parsing coordinate pairs from the input
2. Testing all possible pairs of points as opposite corners
3. Calculating rectangle areas
4. Finding the maximum area

### Core Challenge

The key difficulty is efficiently checking all possible pairs of red tiles and calculating the resulting rectangle areas. With N red tiles, there are C(N, 2) = N×(N-1)/2 possible pairs to check.

### Important Constraint

The two tiles must be **opposite corners** of a rectangle - meaning they must be diagonally opposite (not adjacent sides). For tiles at (x1, y1) and (x2, y2) to form opposite corners:
- They must have different x-coordinates (x1 ≠ x2)
- They must have different y-coordinates (y1 ≠ y2)
- The rectangle area is |x2 - x1| × |y2 - y1|

### Example

Given red tiles at:
```
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
```

The largest rectangle has area **50**, formed between tiles at `(2,5)` and `(11,1)`:
- Width: |11 - 2| = 9
- Height: |5 - 1| = 4
- Area: 9 × 4 = 36... wait, let me recalculate

Actually:
- Width: |11 - 2| = 9
- Height: |5 - 1| = 4
- Area: 9 × 4 = 36

Hmm, the puzzle says area is 50. Let me reconsider...

Looking at the visual representation:
```
..............
..OOOOOOOOOO..  <- row 1 to row 5
..OOOOOOOOOO..
..OOOOOOOOOO..
..OOOOOOOOOO..
..OOOOOOOOOO..
..............
.........#.#..
..............
```

The rectangle spans from column 2 to column 11 (10 columns) and from row 1 to row 5 (5 rows).
- Width: 11 - 2 + 1 = 10 (inclusive counting)
- Height: 5 - 1 + 1 = 5 (inclusive counting)
- Area: 10 × 5 = 50 ✓

**Key Insight**: The area calculation is *inclusive* of both corner tiles:
- Area = (|x2 - x1| + 1) × (|y2 - y1| + 1)

Wait, that doesn't seem right either. Let me think about this differently.

Looking at the grid, if we have corners at (2,5) and (11,1):
- The rectangle includes columns from 2 to 11: that's positions 2,3,4,5,6,7,8,9,10,11 = 10 positions
- The rectangle includes rows from 1 to 5: that's positions 1,2,3,4,5 = 5 positions
- Area = 10 × 5 = 50 ✓

So the formula is:
- **Area = |x2 - x1| × |y2 - y1|** (using absolute differences, which gives the span excluding the starting point)

Actually, rethinking: if corners are at (2,5) and (11,1):
- x-span: from 2 to 11 = 11-2 = 9 units
- y-span: from 1 to 5 = 5-1 = 4 units
- But area shown is 50, not 36

The discrepancy suggests we're counting *tiles*, not units of distance. If we have 10 tiles horizontally and 5 tiles vertically, that's 50 tiles total.

So the correct interpretation is:
- **Number of columns spanned**: |x2 - x1| + 1 (but only if we're 0-indexed)

Actually, I think the simplest interpretation is that the coordinates represent discrete tile positions, and when we form a rectangle between (x1,y1) and (x2,y2), the area in tiles is:
- If x1 < x2 and y1 < y2: Area = (x2 - x1) × (y2 - y1)

For (2,5) and (11,1), we need to order them:
- x_min = 2, x_max = 11, dx = 9
- y_min = 1, y_max = 5, dy = 4
- Area = 9 × 4 = 36 ❌

This still doesn't match. Let me look at the visual grid more carefully.

The grid shows dots from column 0 to ~13 and rows 0 to ~8. The rectangle for (2,5) to (11,1):
```
Row 0: ..............
Row 1: ..OOOOOOOOOO..  <- y=1, from x=2 to x=11
Row 2: ..OOOOOOOOOO..
Row 3: ..OOOOOOOOOO..
Row 4: ..OOOOOOOOOO..
Row 5: ..OOOOOOOOOO..  <- y=5, from x=2 to x=11
Row 6: ..............
Row 7: .........#.#..
Row 8: ..............
```

Counting the 'O's:
- Horizontally: 10 O's per row (positions 2,3,4,5,6,7,8,9,10,11)
- Vertically: 5 rows (rows 1,2,3,4,5)
- Total: 10 × 5 = 50 ✓

So the formula must account for inclusive counting:
- **Width (inclusive)**: |x2 - x1| + 1
- **Height (inclusive)**: |y2 - y1| + 1
- **Area**: (|x2 - x1| + 1) × (|y2 - y1| + 1)

For corners (2,5) and (11,1):
- Width: |11 - 2| + 1 = 10
- Height: |5 - 1| + 1 = 5
- Area: 10 × 5 = 50 ✓

But wait - this assumes we're counting the number of tile positions, not the distance. Let me verify with another example.

Example: Rectangle between (7,1) and (11,7) should have area 35:
- Width: |11 - 7| + 1 = 5
- Height: |7 - 1| + 1 = 7
- Area: 5 × 7 = 35 ✓

Example: Rectangle between (7,3) and (2,3) should have area 6:
- Width: |7 - 2| + 1 = 6
- Height: |3 - 3| + 1 = 1
- Area: 6 × 1 = 6 ✓

Perfect! The formula is confirmed:
**Area = (|x2 - x1| + 1) × (|y2 - y1| + 1)**

This makes sense because we're counting discrete tile positions, not continuous distances.

## Input Format

The input consists of coordinate pairs, one per line, in the format `x,y`:

```
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
```

**Characteristics**:
- Each line contains two integers separated by a comma
- First number is x-coordinate (column)
- Second number is y-coordinate (row)
- All coordinates are non-negative integers
- Coordinates represent positions of red tiles in the grid

**Parsing Requirements**:
- Split each line by comma
- Convert both parts to integers
- Store as coordinate pairs (tuples or objects)

## Output Format

**Part 1**: A single integer representing the maximum area of any rectangle that can be formed using two red tiles as opposite corners.

Example: `50`

## Requirements

### Part 1

Find the largest rectangle that can be formed using any two red tiles as opposite corners.

**Rules**:
1. Choose any two red tiles from the input list
2. Use these tiles as **opposite corners** of a rectangle
   - The tiles must be diagonally opposite (different x AND different y coordinates)
   - Tiles at the same x or same y coordinate cannot form opposite corners
3. Calculate the area of the rectangle
   - Area = (|x2 - x1| + 1) × (|y2 - y1| + 1)
   - This counts the number of tile positions within the rectangle (inclusive)
4. Find the maximum area across all possible pairs

**Algorithm**:
1. Parse all red tile coordinates from input
2. For each pair of tiles (i, j) where i < j:
   - Check if they can form opposite corners (different x AND different y)
   - If yes, calculate area = (|x2 - x1| + 1) × (|y2 - y1| + 1)
   - Track maximum area seen
3. Return maximum area

#### Part 1 Example Answer

For the given example input with 8 red tiles, the maximum area is **50**.

**Validation**:
- Tiles at (2,5) and (11,1):
  - Width: |11 - 2| + 1 = 10
  - Height: |5 - 1| + 1 = 5
  - Area: 10 × 5 = 50

**Other rectangles tested**:
- (7,1) to (11,7): (5) × (7) = 35
- (2,5) to (9,7): (8) × (3) = 24
- (7,3) to (2,3): (6) × (1) = 6 (degenerate - horizontal line)

### Part 2: Green Tile Loop Constraint

**New Constraint**: Rectangles can now ONLY include tiles that are red or green. This dramatically changes the problem from Part 1.

#### The Green Tile System

**Key Insight**: The red tiles form a **closed polygon loop**, and green tiles consist of:
1. **Path tiles**: Straight-line segments connecting consecutive red tiles
2. **Interior tiles**: All tiles inside the polygon formed by red tiles

**Important Properties**:
- Red tiles are ordered in the input list
- Each red tile connects to the next red tile via a straight horizontal or vertical path of green tiles
- The last red tile connects back to the first red tile (the list wraps)
- Consecutive red tiles in the list are always on the same row OR same column
- All tiles inside the polygon loop are also green
- Tiles outside the loop are neither red nor green
- **Rectangles must have red tiles in opposite corners**
- **All other tiles in the rectangle must be red or green**

#### Example Analysis

Using the same 8 red tiles from Part 1:
```
7,1  → 11,1  (horizontal path)
11,1 → 11,7  (vertical path)
11,7 → 9,7   (horizontal path)
9,7  → 9,5   (vertical path)
9,5  → 2,5   (horizontal path)
2,5  → 2,3   (vertical path)
2,3  → 7,3   (horizontal path)
7,3  → 7,1   (vertical path, wraps to first)
```

**Part 1 Answer (INVALID for Part 2)**: Area 50
- Rectangle between (2,5) and (11,1)
- This rectangle includes tiles that are NOT red or green
- Therefore, it's rejected in Part 2

**Part 2 Answer**: Area 24
- Rectangle between (9,5) and (2,3)
- All tiles in this rectangle are either red or green
- This is the largest valid rectangle

**Other valid rectangles mentioned**:
- Area 15: between (7,3) and (11,1)
- Area 3: between (9,7) and (9,5)
- Area 24: between (9,5) and (2,3) ← maximum

#### Algorithm Requirements

**Phase 1: Identify All Green Tiles**

1. **Build the red tile path (loop)**:
   - Red tiles are given in order (wrapping)
   - Each consecutive pair forms a path segment

2. **Find path tiles** (connecting consecutive red tiles):
   - For each pair of consecutive red tiles (i, i+1):
     - If they share the same row: add all tiles between them horizontally
     - If they share the same column: add all tiles between them vertically
   - Don't forget to connect the last tile to the first (wraparound)

3. **Find interior tiles** (inside the polygon):
   - Use a polygon fill algorithm to determine which tiles are inside
   - Options:
     - **Ray casting**: For each candidate tile, count intersections with polygon edges
     - **Flood fill**: Fill from outside, everything not reached is inside
     - **Scanline algorithm**: Process row by row
     - **Shoelace formula + point-in-polygon**: Compute polygon area, test containment

**Phase 2: Filter Valid Rectangles**

For each pair of red tiles that could form opposite corners:
1. Calculate the rectangle bounds
2. Check EVERY tile in the rectangle
3. Verify that each tile is either:
   - A red tile (one of the input tiles)
   - A green tile (path or interior)
4. If all tiles are red/green, calculate area and track maximum
5. Return maximum valid area

#### Algorithm Analysis

**Approach 1: Explicit Green Tile Set + Validation (Recommended)**

**Strategy**: 
1. Build a complete set of all green tiles (path + interior)
2. For each potential rectangle, validate all tiles are in the red/green set
3. Track maximum valid area

**Algorithm**:
```python
def solve_part2(text: str) -> int:
    # Parse red tiles
    red_tiles = parse_input(text)
    red_set = set(red_tiles)
    
    # Build green tile set
    green_tiles = set()
    
    # Add path tiles between consecutive red tiles
    n = len(red_tiles)
    for i in range(n):
        curr = red_tiles[i]
        next_tile = red_tiles[(i + 1) % n]  # Wrap around
        
        # Add all tiles on the straight line between curr and next_tile
        path_tiles = get_line_tiles(curr, next_tile)
        green_tiles.update(path_tiles)
    
    # Add interior tiles using point-in-polygon test
    min_x = min(x for x, y in red_tiles)
    max_x = max(x for x, y in red_tiles)
    min_y = min(y for x, y in red_tiles)
    max_y = max(y for x, y in red_tiles)
    
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            if (x, y) not in red_set and point_in_polygon((x, y), red_tiles):
                green_tiles.add((x, y))
    
    # Valid tiles = red tiles ∪ green tiles
    valid_tiles = red_set | green_tiles
    
    # Find maximum rectangle with only valid tiles
    max_area = 0
    for i in range(len(red_tiles)):
        for j in range(i + 1, len(red_tiles)):
            x1, y1 = red_tiles[i]
            x2, y2 = red_tiles[j]
            
            # Must form opposite corners
            if x1 == x2 or y1 == y2:
                continue
            
            # Check if all tiles in rectangle are valid
            rect_valid = True
            x_min, x_max = min(x1, x2), max(x1, x2)
            y_min, y_max = min(y1, y2), max(y1, y2)
            
            for x in range(x_min, x_max + 1):
                for y in range(y_min, y_max + 1):
                    if (x, y) not in valid_tiles:
                        rect_valid = False
                        break
                if not rect_valid:
                    break
            
            if rect_valid:
                width = x_max - x_min + 1
                height = y_max - y_min + 1
                area = width * height
                max_area = max(max_area, area)
    
    return max_area
```

**Time Complexity**:
- Building path tiles: O(N × L) where L is average path length
- Finding interior tiles: O(W × H × N) for point-in-polygon checks (W×H is bounding box area)
- Rectangle validation: O(N² × R × N) where R is average rectangle area
- **Overall**: O(W × H × N + N² × R × N)
- For typical inputs: O(W × H × N) dominates

**Space Complexity**: O(W × H)
- Store all green tiles in a set
- Red tile set: O(N)
- Green tile set: O(W × H) in worst case

**Pros**:
- Clear separation of concerns
- Easy to debug (can visualize green tiles)
- Explicit validation logic

**Cons**:
- Potentially slow for large grids
- May build large green tile sets

**Approach 2: On-Demand Validation**

**Strategy**: For each rectangle, check tiles on-demand without building full green set

**Pros**:
- Potentially faster if few rectangles need checking
- Lower memory usage

**Cons**:
- Repeated polygon containment tests
- More complex logic per rectangle

**Recommended Approach**: Use Approach 1 (Explicit Green Tile Set)
- Clearer implementation
- Easier to test and debug
- One-time cost to build green tile set
- Fast rectangle validation with set lookups

#### Key Algorithmic Components

**1. Line Tile Enumeration**

```python
def get_line_tiles(start: Tuple[int, int], end: Tuple[int, int]) -> Set[Tuple[int, int]]:
    """
    Get all tiles on the straight line between start and end.
    Assumes start and end share same x OR same y coordinate.
    """
    x1, y1 = start
    x2, y2 = end
    tiles = set()
    
    if x1 == x2:  # Vertical line
        y_min, y_max = min(y1, y2), max(y1, y2)
        for y in range(y_min, y_max + 1):
            tiles.add((x1, y))
    else:  # Horizontal line (y1 == y2)
        x_min, x_max = min(x1, x2), max(x1, x2)
        for x in range(x_min, x_max + 1):
            tiles.add((x, y1))
    
    return tiles
```

**2. Point-in-Polygon Test (Ray Casting)**

```python
def point_in_polygon(point: Tuple[int, int], polygon: List[Tuple[int, int]]) -> bool:
    """
    Determine if a point is inside a polygon using ray casting algorithm.
    Casts a ray from the point to infinity and counts edge crossings.
    Odd number of crossings = inside, even = outside.
    """
    x, y = point
    n = len(polygon)
    inside = False
    
    p1x, p1y = polygon[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon[i % n]
        
        # Check if point is on a horizontal edge
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        
        p1x, p1y = p2x, p2y
    
    return inside
```

**Alternative: Shoelace Formula + Winding Number**

For closed polygons with vertices in order, we can:
1. Use shoelace formula to compute polygon area
2. Use winding number algorithm for point containment

**3. Rectangle Tile Enumeration**

```python
def get_rectangle_tiles(x1: int, y1: int, x2: int, y2: int) -> Set[Tuple[int, int]]:
    """Get all tiles within rectangle (inclusive)."""
    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y1, y2), max(y1, y2)
    
    tiles = set()
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            tiles.add((x, y))
    
    return tiles
```

#### Common Pitfalls

1. **Forgetting wraparound**: Last red tile must connect to first red tile
2. **Assuming only path tiles are green**: Interior tiles are also green!
3. **Including path endpoints**: Red tiles themselves are red, not green
4. **Off-by-one in line generation**: Must include both endpoints
5. **Not handling edge tiles**: Tiles on polygon boundary may need special handling
6. **Integer coordinates in point-in-polygon**: Ensure algorithm works with discrete grid
7. **Large coordinate ranges**: If input has huge coordinates, memory may be an issue

#### Testing Strategy for Part 2

**Test Cases**:

1. **Main Example**: 8 red tiles → area 24
   - Verify green tiles are correctly identified
   - Confirm Part 1's answer (50) is rejected
   - Validate specific rectangles:
     - (7,3) to (11,1): area 15 ✓
     - (9,7) to (9,5): area 3 ✓
     - (9,5) to (2,3): area 24 ✓ (maximum)

2. **Simple Loop**: 4 red tiles forming a square
   - All interior tiles should be green
   - Any rectangle within the square should be valid

3. **Narrow Loop**: Red tiles forming a thin rectangle
   - Minimal interior area
   - Test edge cases with path-only green tiles

4. **Complex Polygon**: Non-rectangular loop
   - Test point-in-polygon algorithm correctness
   - Verify interior detection

**Validation Points**:
- Count green tiles manually for small example
- Visualize the loop and interior
- Check that Part 2 answer ≤ Part 1 answer (more constraints)
- Verify all tiles in answer rectangle are red/green

#### Performance Considerations

**For large inputs**:
- **Sparse grid representation**: Use sets instead of 2D arrays
- **Bounding box optimization**: Only check tiles within polygon bounds
- **Early rectangle rejection**: If corner tiles aren't red, skip immediately
- **Incremental validation**: Stop checking rectangle tiles on first invalid tile

**Memory optimization**:
- Don't materialize all rectangle tiles if just counting
- Use generator expressions for tile enumeration
- Cache point-in-polygon results if testing many points

#### Edge Cases

1. **Collinear red tiles**: All red tiles in a line
   - No interior area
   - Only path tiles are green
   - Valid rectangles are very limited

2. **Self-intersecting polygon**: Red tiles that create crossing paths
   - Point-in-polygon may behave unexpectedly
   - May need to handle specially

3. **Duplicate red tiles**: Same coordinate appears twice
   - Should handle gracefully

4. **Very sparse grid**: Huge coordinate ranges with few tiles
   - Set-based approach is critical
   - Don't try to materialize full grid

5. **All red tiles at same point**: Degenerate polygon
   - No valid rectangles

#### Comparison to Part 1

| Aspect | Part 1 | Part 2 |
|--------|--------|--------|
| **Constraint** | Red tiles as corners | Red/green tiles only |
| **Algorithm** | Simple pair enumeration | Polygon + validation |
| **Complexity** | O(N²) | O(W×H×N + N²×R×N) |
| **Answer** | 50 (unrestricted) | 24 (restricted) |
| **Key Challenge** | Area calculation | Green tile identification |

**Why Part 1 answer fails**: Rectangle (2,5)-(11,1) includes tiles outside the red/green loop, which are invalid in Part 2.

## Algorithm Analysis

### Problem Classification

This is a **combinatorial geometry problem** with elements of:
- **Exhaustive pair enumeration**: Check all C(N,2) pairs
- **Geometric calculation**: Compute rectangle areas
- **Optimization**: Find maximum value
- **Constraint checking**: Validate that pairs form valid rectangles

### Approach 1: Brute Force Pair Enumeration (Recommended)

**Strategy**: Check every possible pair of red tiles and calculate the area of the rectangle they form.

**Algorithm**:
```python
def find_max_rectangle_area(tiles):
    max_area = 0
    n = len(tiles)
    
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = tiles[i]
            x2, y2 = tiles[j]
            
            # Check if they form opposite corners (different x AND y)
            if x1 != x2 and y1 != y2:
                # Calculate area (inclusive counting)
                width = abs(x2 - x1) + 1
                height = abs(y2 - y1) + 1
                area = width * height
                max_area = max(max_area, area)
    
    return max_area
```

**Time Complexity**: O(N²)
- N red tiles in input
- C(N,2) = N×(N-1)/2 pairs to check
- Each pair requires O(1) calculation
- Total: O(N²)

**Space Complexity**: O(N)
- Store N coordinate pairs
- No additional data structures needed
- O(1) for tracking max area

**Pros**:
- Simple and straightforward
- Guaranteed to find optimal solution
- Easy to implement and debug
- No complex data structures needed

**Cons**:
- O(N²) may be slow for very large N (e.g., N > 10,000)
- Checks every pair even if many are invalid

**Optimizations**:
- Skip pairs with same x or same y coordinate early
- Use itertools.combinations for cleaner pair generation
- Could sort tiles by x or y first (but doesn't improve worst case)

### Approach 2: Spatial Indexing with Optimization

**Strategy**: Use spatial data structures to reduce the number of pairs checked.

**Potential optimizations**:
1. **Sort tiles by x-coordinate**: Process in order to establish bounds
2. **Grid bucketing**: Group tiles into regions, only check cross-region pairs
3. **Pruning**: If current max area > max possible with remaining tiles, stop early

**Algorithm sketch**:
```python
def find_max_rectangle_optimized(tiles):
    # Sort by x-coordinate
    tiles.sort()
    
    max_area = 0
    n = len(tiles)
    
    for i in range(n):
        x1, y1 = tiles[i]
        
        # Early termination: if max remaining x-distance can't beat current max
        max_possible_width = max(t[0] for t in tiles[i+1:]) - x1 + 1
        if max_possible_width * (max_y_span + 1) <= max_area:
            continue
        
        for j in range(i + 1, n):
            x2, y2 = tiles[j]
            
            if y1 != y2:
                width = x2 - x1 + 1
                height = abs(y2 - y1) + 1
                area = width * height
                max_area = max(max_area, area)
    
    return max_area
```

**Time Complexity**: O(N² log N) worst case (due to sorting)
- Average case may be better with pruning
- Best case: O(N log N) if many pairs can be skipped

**Space Complexity**: O(N)

**Pros**:
- Can be faster in practice with good pruning
- Sorting provides structure for optimizations

**Cons**:
- More complex implementation
- Pruning logic can be error-prone
- May not significantly improve on worst-case inputs
- Overhead of sorting may not be worth it for small N

### Approach 3: Mathematical Analysis (Not Applicable)

For some geometric problems, there are mathematical properties that allow direct computation without enumeration. However, for this problem:
- No clear pattern for which tiles form maximum rectangles
- Position of tiles is arbitrary
- Need to check actual combinations

**Conclusion**: Mathematical shortcuts don't apply here.

### Recommended Approach

**Use Approach 1 (Brute Force Enumeration)** because:
1. **Simplicity**: Clean, easy to implement correctly
2. **Sufficient performance**: O(N²) is acceptable for typical AoC inputs (N < 1000)
3. **Guaranteed correctness**: No complex logic to debug
4. **Clear code**: Readable and maintainable

**When to consider Approach 2**:
- If Part 2 requires processing millions of tiles
- If actual puzzle input has N > 10,000
- If execution time becomes a bottleneck

**Implementation priority**:
1. Get Approach 1 working correctly
2. Test thoroughly with examples
3. Submit Part 1
4. Only optimize if needed for Part 2

## Data Structures

### Primary Structures

**Tiles List**: `List[Tuple[int, int]]`
- Store all red tile coordinates
- Each element is (x, y) tuple
- Can use list of tuples or list of custom Point objects

**Example**:
```python
tiles = [
    (7, 1),
    (11, 1),
    (11, 7),
    (9, 7),
    (9, 5),
    (2, 5),
    (2, 3),
    (7, 3),
]
```

**Alternative**: Use a `@dataclass` for clarity:
```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int
```

### Helper Variables

- `max_area`: Integer tracking the maximum area found so far
- `n`: Number of tiles (for loop bounds)
- `width`, `height`, `area`: Temporary variables for calculations

**Why simple structures work**:
- No need for spatial indexing (2D tree, quadtree) for small inputs
- No need for adjacency graphs
- Direct pair iteration is sufficient
- Memory overhead is minimal

## Implementation Guidance

### Step-by-Step Implementation

#### Step 1: Parse Input

```python
def parse_input(text: str) -> List[Tuple[int, int]]:
    """Parse coordinate pairs from input text."""
    tiles = []
    for line in text.strip().split('\n'):
        if line:
            x, y = line.split(',')
            tiles.append((int(x), int(y)))
    return tiles
```

**Key points**:
- Strip whitespace from input
- Split by newlines
- Split each line by comma
- Convert to integers
- Return list of tuples

#### Step 2: Calculate Rectangle Area

```python
def calculate_area(x1: int, y1: int, x2: int, y2: int) -> int:
    """
    Calculate the area of a rectangle with opposite corners at (x1,y1) and (x2,y2).
    Returns 0 if the points don't form a valid rectangle (same x or same y).
    """
    if x1 == x2 or y1 == y2:
        return 0  # Not opposite corners (degenerate rectangle)
    
    width = abs(x2 - x1) + 1
    height = abs(y2 - y1) + 1
    return width * height
```

**Key points**:
- Check for degenerate cases (same x or y)
- Use absolute value for difference (works regardless of point order)
- Add 1 for inclusive counting
- Return area as integer

#### Step 3: Find Maximum Area

```python
def find_max_rectangle_area(tiles: List[Tuple[int, int]]) -> int:
    """
    Find the maximum area of any rectangle formed by two tiles as opposite corners.
    """
    max_area = 0
    n = len(tiles)
    
    for i in range(n):
        for j in range(i + 1, n):
            x1, y1 = tiles[i]
            x2, y2 = tiles[j]
            
            area = calculate_area(x1, y1, x2, y2)
            max_area = max(max_area, area)
    
    return max_area
```

**Key points**:
- Initialize max_area to 0
- Use nested loops to check all pairs
- Inner loop starts at i+1 to avoid duplicates
- Track maximum area seen

#### Step 4: Main Solution

```python
def solve_part1(text: str) -> int:
    """Solve Part 1: Find maximum rectangle area."""
    tiles = parse_input(text)
    return find_max_rectangle_area(tiles)
```

**Alternative with itertools**:
```python
from itertools import combinations

def find_max_rectangle_area(tiles: List[Tuple[int, int]]) -> int:
    """Find maximum rectangle area using itertools.combinations."""
    max_area = 0
    
    for (x1, y1), (x2, y2) in combinations(tiles, 2):
        if x1 != x2 and y1 != y2:
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height
            max_area = max(max_area, area)
    
    return max_area
```

**Pros of itertools approach**:
- More Pythonic and concise
- Clearer intent (we want combinations)
- Less indexing logic

**Cons**:
- Slightly less control over iteration
- May be marginally slower (negligible)

### Common Pitfalls

1. **Off-by-one errors in area calculation**
   - Forgetting to add 1 for inclusive counting
   - Using `abs(x2 - x1)` instead of `abs(x2 - x1) + 1`
   - Test: (0,0) to (1,1) should be 2×2 = 4, not 1×1 = 1

2. **Not checking for degenerate rectangles**
   - Tiles at (5,3) and (5,7) have same x → area should be 0 (or skip)
   - Tiles at (2,4) and (8,4) have same y → area should be 0 (or skip)
   - Can handle by checking `if x1 != x2 and y1 != y2`

3. **Checking pairs twice**
   - Using `for i in range(n): for j in range(n)` checks each pair twice
   - Correct: `for j in range(i+1, n)` to check each pair once

4. **Integer overflow** (unlikely in Python)
   - Python handles arbitrary precision integers
   - Not a concern for this problem

5. **Empty input**
   - What if there are 0 or 1 tiles?
   - With 0 tiles: no rectangles → area = 0
   - With 1 tile: no pairs → area = 0
   - Handle: return 0 if `len(tiles) < 2`

6. **Parsing errors**
   - Lines with extra whitespace
   - Lines with missing comma
   - Non-integer values
   - Negative coordinates (probably valid, treat normally)

### Edge Cases to Handle

1. **Minimum input**: 2 tiles (exactly 1 rectangle)
2. **All tiles in a line**: Same x or same y for all tiles → area = 0
3. **All tiles at same point**: Duplicate coordinates → area = 0
4. **Large coordinates**: x, y > 1000 → should still work (Python handles large ints)
5. **Negative coordinates**: Valid tile positions (treat normally)
6. **Maximum area ties**: Multiple pairs with same max area → return the max value (don't need to track which pair)
7. **Single tile**: No pairs → area = 0
8. **Zero tiles**: Empty input → area = 0

### Testing Strategy

Test in order of increasing complexity:
1. **Simple cases**: 2-3 tiles, easy to verify
2. **Main example**: 8 tiles, expected area 50
3. **Edge cases**: Degenerate rectangles, collinear points
4. **Large inputs**: Performance testing with many tiles

## Test Plan

### Part 2 Tests

#### Main Example (from puzzle)

**Input** (same 8 red tiles as Part 1):
```
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
```

**Expected Output**: `24`

**Green Tile Identification**:
1. **Path tiles** (connecting consecutive red tiles):
   - (7,1) → (11,1): tiles at (8,1), (9,1), (10,1)
   - (11,1) → (11,7): tiles at (11,2), (11,3), (11,4), (11,5), (11,6)
   - (11,7) → (9,7): tile at (10,7)
   - (9,7) → (9,5): tile at (9,6)
   - (9,5) → (2,5): tiles at (8,5), (7,5), (6,5), (5,5), (4,5), (3,5)
   - (2,5) → (2,3): tile at (2,4)
   - (2,3) → (7,3): tiles at (3,3), (4,3), (5,3), (6,3)
   - (7,3) → (7,1): tile at (7,2)

2. **Interior tiles** (inside the polygon loop):
   - All tiles inside the closed loop formed by red tiles
   - Use point-in-polygon test to identify

**Valid Rectangles** (examples from puzzle):
- Between (7,3) and (11,1): area = 5 × 3 = 15 ✓
- Between (9,7) and (9,5): area = 1 × 3 = 3 ✓
- Between (9,5) and (2,3): area = 8 × 3 = 24 ✓ (maximum)

**Invalid Rectangle** (from Part 1):
- Between (2,5) and (11,1): area would be 50, but contains non-green tiles ✗

**Verification**:
- Part 2 answer (24) < Part 1 answer (50)
- All tiles in the 24-area rectangle must be red or green

#### Simple Test Cases

**Test 1: Small Square Loop**

**Input**:
```
0,0
10,0
10,10
0,10
```

**Expected Green Tiles**:
- Path: All tiles on edges (0-10 on each side)
- Interior: All tiles inside the 11×11 square

**Expected Output**: `121`
- Largest rectangle is the entire square: (0,0) to (10,10)
- Area: 11 × 11 = 121
- All tiles are red (corners) or green (edges + interior)

**Test 2: Minimal Loop (No Interior)**

**Input**:
```
0,0
2,0
2,1
0,1
```

**Expected Green Tiles**:
- Path only: (1,0), (2,0), (0,1), (1,1)
- No interior (the loop is too thin)

**Expected Output**: `6`
- Rectangle from (0,0) to (2,1)
- Area: 3 × 2 = 6

**Test 3: Line (Degenerate Polygon)**

**Input**:
```
0,0
5,0
10,0
```

**Expected Green Tiles**:
- Path: (1,0), (2,0), (3,0), (4,0), (6,0), (7,0), (8,0), (9,0)
- No interior (not a polygon)

**Expected Output**: `0`
- No valid rectangles (all tiles same y-coordinate)

**Test 4: L-Shape Loop**

**Input**:
```
0,0
5,0
5,5
0,5
```

**Expected Green Tiles**:
- Path: Tiles on perimeter of 6×6 square
- Interior: All tiles inside the square

**Expected Output**: `36`
- Full square: (0,0) to (5,5)
- Area: 6 × 6 = 36

#### Edge Cases for Part 2

**Edge 1: Rectangle Outside Loop**

**Input**: 8 red tiles forming a small loop + 2 red tiles far away

**Expected**: Only rectangles within the loop are valid

**Edge 2: Partial Overlap with Loop**

**Expected**: Rectangles that partially overlap the green area are invalid

**Edge 3: Rectangle Exactly Matching Loop Boundary**

**Expected**: Valid if all boundary tiles are path tiles

**Edge 4: Very Large Coordinates with Small Loop**

**Input**: Red tiles at (0,0), (1,0), (1,1), (0,1) but with offset 1000000

**Expected**: Algorithm should handle sparse representation efficiently

**Edge 5: Complex Concave Polygon**

**Input**: Red tiles forming a concave (non-convex) polygon

**Expected**: Point-in-polygon algorithm correctly identifies interior

#### Validation Trace for Part 2 Main Example

**Step 1: Parse Red Tiles**
```
red_tiles = [(7,1), (11,1), (11,7), (9,7), (9,5), (2,5), (2,3), (7,3)]
```

**Step 2: Build Path Tiles**
- Connect (7,1) → (11,1): add (8,1), (9,1), (10,1)
- Connect (11,1) → (11,7): add (11,2), (11,3), (11,4), (11,5), (11,6)
- Connect (11,7) → (9,7): add (10,7)
- Connect (9,7) → (9,5): add (9,6)
- Connect (9,5) → (2,5): add (8,5), (7,5), (6,5), (5,5), (4,5), (3,5)
- Connect (2,5) → (2,3): add (2,4)
- Connect (2,3) → (7,3): add (3,3), (4,3), (5,3), (6,3)
- Connect (7,3) → (7,1): add (7,2)

**Step 3: Find Interior Tiles**
- Bounding box: x ∈ [2,11], y ∈ [1,7]
- For each tile in bounding box:
  - If not red and not path: test if inside polygon
  - If inside: add to green_tiles

**Step 4: Build Valid Tile Set**
```
valid_tiles = red_set ∪ green_tiles
```

**Step 5: Test Rectangles**

| Corners | Valid? | Area | Reason |
|---------|--------|------|--------|
| (7,1)-(11,7) | Yes | 35 | All tiles red/green |
| (11,1)-(2,5) | **No** | 50 | Contains non-green tiles |
| (9,7)-(9,5) | Yes | 3 | All tiles red/green |
| (9,5)-(2,3) | Yes | 24 | All tiles red/green ← MAX |
| (7,3)-(11,1) | Yes | 15 | All tiles red/green |

**Step 6: Return Maximum**
- Maximum valid area: **24**

#### Test Cases for Green Tile Algorithms

**Test: Line Tile Generation**

Input: `get_line_tiles((0,0), (5,0))`
Expected: `{(0,0), (1,0), (2,0), (3,0), (4,0), (5,0)}`

Input: `get_line_tiles((3,2), (3,7))`
Expected: `{(3,2), (3,3), (3,4), (3,5), (3,6), (3,7)}`

**Test: Point-in-Polygon**

Polygon: `[(0,0), (10,0), (10,10), (0,10)]` (square)

| Point | Expected | Reason |
|-------|----------|--------|
| (5,5) | True | Inside |
| (0,0) | False | On boundary (vertex) |
| (5,0) | False | On boundary (edge) |
| (15,5) | False | Outside |
| (-1,5) | False | Outside |

**Test: Rectangle Validation**

Red tiles: `[(0,0), (10,0), (10,10), (0,10)]`
Green tiles: All tiles inside + edges

| Rectangle | Expected | Reason |
|-----------|----------|--------|
| (0,0)-(10,10) | Valid | All tiles red/green |
| (2,2)-(8,8) | Valid | Subset of green tiles |
| (0,0)-(15,10) | Invalid | Contains tiles outside loop |
| (5,5)-(6,6) | Valid | Small interior rectangle |

### Part 1 Tests

#### Main Example (from puzzle)

**Input**:
```
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
```

**Expected Output**: `50`

**Verification**:
- Tiles at (2,5) and (11,1):
  - Width: |11-2|+1 = 10
  - Height: |5-1|+1 = 5
  - Area: 50 ✓

### Simple Test Cases

#### Test 1: Two Tiles (Minimum Valid Input)

**Input**:
```
0,0
5,3
```

**Expected**: `24`
- Width: |5-0|+1 = 6
- Height: |3-0|+1 = 4
- Area: 6 × 4 = 24

#### Test 2: Square Rectangle

**Input**:
```
0,0
4,4
```

**Expected**: `25`
- Width: 5
- Height: 5
- Area: 5 × 5 = 25

#### Test 3: Three Tiles (Multiple Pairs)

**Input**:
```
0,0
3,2
6,5
```

**Expected**: `36`
- (0,0) to (3,2): 4 × 3 = 12
- (0,0) to (6,5): 7 × 6 = 42 ← maximum
- (3,2) to (6,5): 4 × 4 = 16

Wait, let me recalculate:
- (0,0) to (6,5): (6-0+1) × (5-0+1) = 7 × 6 = 42 ✓

**Corrected Expected**: `42`

#### Test 4: Unit Rectangle

**Input**:
```
0,0
1,1
```

**Expected**: `4`
- Width: 2
- Height: 2
- Area: 2 × 2 = 4

#### Test 5: Horizontal Line (Degenerate)

**Input**:
```
0,5
5,5
10,5
```

**Expected**: `0`
- All tiles have same y-coordinate
- No valid rectangles can be formed
- Area: 0

#### Test 6: Vertical Line (Degenerate)

**Input**:
```
3,0
3,5
3,10
```

**Expected**: `0`
- All tiles have same x-coordinate
- No valid rectangles can be formed
- Area: 0

#### Test 7: Mixed Valid and Invalid Pairs

**Input**:
```
0,0
0,5
5,0
5,5
```

**Expected**: `36`
- (0,0) to (0,5): invalid (same x)
- (0,0) to (5,0): invalid (same y)
- (0,0) to (5,5): 6 × 6 = 36 ✓
- (0,5) to (5,0): 6 × 6 = 36 ✓
- (0,5) to (5,5): invalid (same y)
- (5,0) to (5,5): invalid (same x)
- Maximum: 36

### Edge Cases

#### Edge 1: Single Tile

**Input**:
```
5,5
```

**Expected**: `0`
- No pairs to form rectangles
- Area: 0

#### Edge 2: Empty Input

**Input**:
```
(empty)
```

**Expected**: `0`
- No tiles
- Area: 0

#### Edge 3: Duplicate Coordinates

**Input**:
```
2,3
2,3
5,7
```

**Expected**: `0`
- (2,3) to (2,3): same point, area = 0
- (2,3) to (5,7): 4 × 5 = 20... wait

Actually:
- First (2,3) to second (2,3): same point, invalid
- First (2,3) to (5,7): (5-2+1) × (7-3+1) = 4 × 5 = 20 ✓
- Second (2,3) to (5,7): same as above, 20 ✓

**Corrected Expected**: `20`

#### Edge 4: Large Coordinates

**Input**:
```
0,0
1000,1000
```

**Expected**: `1002001`
- Width: 1001
- Height: 1001
- Area: 1001 × 1001 = 1,002,001

#### Edge 5: Negative Coordinates

**Input**:
```
-5,-5
5,5
```

**Expected**: `121`
- Width: |5-(-5)|+1 = 11
- Height: |5-(-5)|+1 = 11
- Area: 11 × 11 = 121

#### Edge 6: Zero-Width or Zero-Height

This is actually the same as the degenerate line cases (Test 5 and 6).

**Input**:
```
0,0
0,10
```

**Expected**: `0` (same x-coordinate)

### Validation Trace for Main Example

**Input** (8 tiles):
```
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
```

**Step 1: Parse Input**
- tiles = [(7,1), (11,1), (11,7), (9,7), (9,5), (2,5), (2,3), (7,3)]
- n = 8

**Step 2: Enumerate Pairs and Calculate Areas**

| Pair | Tile 1 | Tile 2 | Valid? | Width | Height | Area |
|------|--------|--------|--------|-------|--------|------|
| 0,1  | (7,1)  | (11,1) | No (same y) | - | - | 0 |
| 0,2  | (7,1)  | (11,7) | Yes | 5 | 7 | 35 |
| 0,3  | (7,1)  | (9,7)  | Yes | 3 | 7 | 21 |
| 0,4  | (7,1)  | (9,5)  | Yes | 3 | 5 | 15 |
| 0,5  | (7,1)  | (2,5)  | Yes | 6 | 5 | 30 |
| 0,6  | (7,1)  | (2,3)  | Yes | 6 | 3 | 18 |
| 0,7  | (7,1)  | (7,3)  | No (same x) | - | - | 0 |
| 1,2  | (11,1) | (11,7) | No (same x) | - | - | 0 |
| 1,3  | (11,1) | (9,7)  | Yes | 3 | 7 | 21 |
| 1,4  | (11,1) | (9,5)  | Yes | 3 | 5 | 15 |
| 1,5  | (11,1) | (2,5)  | Yes | 10 | 5 | 50 | ← max |
| 1,6  | (11,1) | (2,3)  | Yes | 10 | 3 | 30 |
| 1,7  | (11,1) | (7,3)  | Yes | 5 | 3 | 15 |
| 2,3  | (11,7) | (9,7)  | No (same y) | - | - | 0 |
| 2,4  | (11,7) | (9,5)  | Yes | 3 | 3 | 9 |
| 2,5  | (11,7) | (2,5)  | Yes | 10 | 3 | 30 |
| 2,6  | (11,7) | (2,3)  | Yes | 10 | 5 | 50 | ← max |
| 2,7  | (11,7) | (7,3)  | Yes | 5 | 5 | 25 |
| 3,4  | (9,7)  | (9,5)  | No (same x) | - | - | 0 |
| 3,5  | (9,7)  | (2,5)  | Yes | 8 | 3 | 24 |
| 3,6  | (9,7)  | (2,3)  | Yes | 8 | 5 | 40 |
| 3,7  | (9,7)  | (7,3)  | Yes | 3 | 5 | 15 |
| 4,5  | (9,5)  | (2,5)  | No (same y) | - | - | 0 |
| 4,6  | (9,5)  | (2,3)  | Yes | 8 | 3 | 24 |
| 4,7  | (9,5)  | (7,3)  | Yes | 3 | 3 | 9 |
| 5,6  | (2,5)  | (2,3)  | No (same x) | - | - | 0 |
| 5,7  | (2,5)  | (7,3)  | Yes | 6 | 3 | 18 |
| 6,7  | (2,3)  | (7,3)  | No (same y) | - | - | 0 |

**Step 3: Find Maximum**
- Valid areas: 35, 21, 15, 30, 18, 21, 15, 50, 30, 15, 9, 30, 50, 25, 24, 40, 15, 24, 9, 18
- Maximum: **50**

**Verification**: Two pairs produce area 50:
1. (11,1) to (2,5): width=10, height=5, area=50 ✓
2. (11,7) to (2,3): width=10, height=5, area=50 ✓

Both are valid and produce the maximum area.

## Complexity Analysis

### Time Complexity

**Parsing**: O(N)
- Read N lines
- Split and convert each line: O(1)
- Total: O(N)

**Pair Enumeration**: O(N²)
- C(N,2) = N×(N-1)/2 pairs
- Each pair: O(1) area calculation
- Total: O(N²)

**Overall**: **O(N²)**

### Space Complexity

**Storage**: O(N)
- Store N coordinate pairs
- Each pair: 2 integers
- Total: O(N)

**Auxiliary Space**: O(1)
- max_area: 1 integer
- Loop variables: constant
- No additional data structures

**Overall**: **O(N)**

### Performance Characteristics

**Best Case**: O(N²)
- Must check all pairs (no early termination possible)
- Cannot be better than O(N²) for this problem

**Average Case**: O(N²)
- Always check all pairs

**Worst Case**: O(N²)
- Same as average case

**Scalability**:
- N = 10: 45 pairs → instant
- N = 100: 4,950 pairs → ~milliseconds
- N = 1,000: 499,500 pairs → ~seconds
- N = 10,000: 49,995,000 pairs → may need optimization

**Expected Input Size**:
- Typical AoC puzzle: N < 1,000
- Performance should be acceptable

**If optimization needed**:
- Spatial indexing (quadtree, R-tree)
- Pruning based on max area bounds
- Parallel processing of pairs
- But likely not necessary for Part 1

## Implementation Checklist

### Part 1
- [x] Parse input into list of (x, y) tuples
  - [x] Handle comma separation
  - [x] Convert to integers
  - [x] Handle empty lines
- [x] Implement area calculation function
  - [x] Check for valid opposite corners (x1≠x2 and y1≠y2)
  - [x] Calculate width = |x2-x1|+1
  - [x] Calculate height = |y2-y1|+1
  - [x] Return area = width × height
- [x] Implement pair enumeration
  - [x] Nested loops or itertools.combinations
  - [x] Avoid checking pairs twice
- [x] Track maximum area
  - [x] Initialize to 0
  - [x] Update with each valid rectangle
- [x] Test with main example (expected: 50)
- [x] Test with simple cases
- [x] Test edge cases (collinear points, single tile, empty)
- [x] Handle degenerate rectangles (same x or y)
- [x] Verify with actual puzzle input

### Part 2
- [ ] Implement green tile identification
  - [ ] Build path tiles between consecutive red tiles
    - [ ] Handle wraparound (last → first)
    - [ ] Generate line tiles for horizontal/vertical paths
  - [ ] Build interior tiles using point-in-polygon
    - [ ] Implement ray casting or winding number algorithm
    - [ ] Test with small polygon examples
    - [ ] Handle edge cases (on boundary, vertex)
  - [ ] Create valid_tiles set (red ∪ green)
- [ ] Implement helper functions
  - [ ] `get_line_tiles(start, end)`: Generate tiles on straight line
  - [ ] `point_in_polygon(point, polygon)`: Test if point is inside
  - [ ] `is_rectangle_valid(rect_corners, valid_tiles)`: Check all tiles
- [ ] Adapt rectangle enumeration
  - [ ] Keep pair enumeration from Part 1
  - [ ] Add validation: check all rectangle tiles are in valid_tiles
  - [ ] Use early termination on first invalid tile
- [ ] Test with Part 2 examples
  - [ ] Main example: expect 24 (not 50)
  - [ ] Verify specific rectangles:
    - [ ] (7,3)-(11,1): area 15 ✓
    - [ ] (9,7)-(9,5): area 3 ✓
    - [ ] (9,5)-(2,3): area 24 ✓ (maximum)
    - [ ] (2,5)-(11,1): invalid ✗
- [ ] Test green tile algorithms separately
  - [ ] Line generation for horizontal/vertical lines
  - [ ] Point-in-polygon for square, complex polygons
  - [ ] Wraparound connection (last → first tile)
- [ ] Optimize for performance
  - [ ] Use sets for O(1) containment checks
  - [ ] Early rectangle rejection
  - [ ] Sparse representation for large coordinates
- [ ] Edge cases
  - [ ] Collinear red tiles (no interior)
  - [ ] Small loops (minimal interior)
  - [ ] Concave polygons
  - [ ] Large coordinate ranges
- [ ] Verify Part 2 answer ≤ Part 1 answer
- [ ] Submit Part 2 solution

## Algorithm Patterns Used

1. **Exhaustive Enumeration**: Check all possible pairs
2. **Combinatorics**: C(N,2) pair selection
3. **Geometric Calculation**: Rectangle area from corner points
4. **Optimization**: Find maximum value
5. **Filtering**: Skip invalid pairs (degenerate rectangles)

## Common AoC Patterns

This problem demonstrates:
- **Brute force sufficiency**: Sometimes O(N²) is good enough
- **Geometric primitives**: Basic rectangle calculations
- **Input parsing**: Simple coordinate pair format
- **Maximum finding**: Track best value during iteration

**Part 2 speculation** (common AoC twists):
- Count rectangles with area ≥ threshold
- Find rectangles that don't overlap certain regions
- Add third dimension (cuboids)
- Find minimum perimeter at maximum area
- Constrain rectangles to contain/avoid specific tiles
- Dynamic tile placement (tiles appear/disappear)

## Summary

This is a two-part geometric problem with escalating complexity:

### Part 1: Maximum Rectangle with Red Corners
A straightforward combinatorial geometry problem requiring:
1. **Parse** coordinate pairs from input
2. **Enumerate** all C(N,2) pairs of tiles
3. **Calculate** rectangle areas using inclusive counting
4. **Find** maximum area

**Key Formula**: Area = (|x2 - x1| + 1) × (|y2 - y1| + 1)

**Key Insight**: With typical input sizes (N < 1000), brute force O(N²) enumeration is sufficient.

### Part 2: Rectangle with Red/Green Tile Constraint
A polygon geometry and validation problem requiring:
1. **Identify** the closed polygon loop formed by red tiles
2. **Generate** green tiles (path + interior):
   - Path tiles: connecting consecutive red tiles
   - Interior tiles: inside the polygon (point-in-polygon test)
3. **Validate** rectangles contain only red/green tiles
4. **Find** maximum valid area

**Key Algorithms**:
- **Line generation**: Enumerate tiles between consecutive red tiles
- **Point-in-polygon**: Ray casting or winding number algorithm
- **Rectangle validation**: Check every tile in rectangle is red/green

**Key Challenge**: The shift from simple area calculation to polygon containment testing

**Success Factors**:

**Part 1**:
- Correct area formula (inclusive counting with +1)
- Proper handling of degenerate cases (same x or y)
- Clean pair enumeration (avoid duplicates)

**Part 2**:
- Correct green tile identification (path + interior)
- Efficient point-in-polygon algorithm
- Wraparound handling (last tile → first tile)
- Set-based validation for O(1) lookups
- Understanding that Part 2 answer ≤ Part 1 answer

**Implementation Priority**:
1. ✅ Solve Part 1 with simple enumeration
2. ✅ Test thoroughly with provided examples
3. ✅ Submit Part 1
4. **Part 2**: Implement green tile identification
5. **Part 2**: Add rectangle validation logic
6. **Part 2**: Test with examples (expected: 24, not 50)
7. **Part 2**: Submit and verify

**Complexity Comparison**:

| Aspect | Part 1 | Part 2 |
|--------|--------|--------|
| **Time** | O(N²) | O(W×H×N + N²×R×N) |
| **Space** | O(N) | O(W×H) |
| **Core** | Area calculation | Polygon + validation |
| **Answer** | 50 | 24 |
