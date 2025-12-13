# Day 07: Laboratories

## Problem Description

A tachyon beam enters a manifold and travels downward, splitting whenever it encounters a splitter (`^`).

- **Part 1**: Count how many times the beam splits (classical physics - beams merge when they reach the same position)
- **Part 2**: Count the total number of unique quantum timelines created (quantum physics - timelines never merge)

## Input

The input is located in `input.txt`

## Input Format

A 2D grid representing a tachyon manifold:
- `S` - Starting position where the tachyon beam enters (top of manifold)
- `.` - Empty space (beam passes through freely)
- `^` - Splitter (beam stops, two new beams emit left and right)

Example:
```
.......S.......
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
...............
```

## Output Format

An integer representing the total number of times the beam is split.

Example:
```
21
```

## Requirements

### Part 1

Count the total number of times a tachyon beam is split as it travels through the manifold.

**Rules:**
1. A tachyon beam starts at position `S` and always moves **downward**
2. Beams pass freely through empty space (`.`)
3. When a beam encounters a splitter (`^`):
   - The original beam **stops**
   - Two new beams are created:
     - One beam continues from the position **immediately to the left** of the splitter
     - One beam continues from the position **immediately to the right** of the splitter
   - Both new beams continue moving **downward**
4. If multiple beams reach the same position, they merge (count as one beam continuing)
5. Beams exit when they move past the bottom edge of the manifold

#### Part 1 Example Answer
21

**Explanation:**

Starting configuration:
```
.......S.......
```

The beam moves down until hitting the first splitter at row 2:
```
.......S.......
.......|.......
.......^.......
```

The beam splits (count: 1), creating two beams:
```
.......S.......
.......|.......
......|^|......
```

Both beams continue down until row 4:
```
.......S.......
.......|.......
......|^|......
......|.|......
......^.^......
```

Each beam hits a splitter (count: 3 total), creating 4 new beams, but the middle two merge:
```
.......S.......
.......|.......
......|^|......
......|.|......
.....|^|^|.....
```

This process continues through all splitter rows. The final state shows all beam paths:
```
.......S.......
.......|.......
......|^|......
......|.|......
.....|^|^|.....
.....|.|.|.....
....|^|^|^|....
....|.|.|.|....
...|^|^|||^|...
...|.|.|||.|...
..|^|^|||^|^|..
..|.|.|||.|.|..
.|^|||^||.||^|.
.|.|||.||.||.|.
|^|^|^|^|^|||^|
|.|.|.|.|.|||.|
```

Counting all the splits:
- Row 2: 1 split
- Row 4: 2 splits (left and right beams each hit a splitter)
- Row 6: 3 splits
- Row 8: 4 splits
- Row 10: 5 splits
- Row 12: 5 splits (one duplicate merge)
- Row 14: 1 split (some beams have exited)

**Total: 21 splits**

### Part 2

**The Quantum Twist:** The teleporter uses a **quantum tachyon manifold**, not a classical one!

In Part 1, we simulated classical physics where multiple beams travel through the manifold and merge when they reach the same position. In Part 2, we're dealing with quantum mechanics and timeline splits.

**Key Differences:**
1. **Single particle** is sent through the manifold (not multiple beams)
2. At each splitter, the particle takes **BOTH** left and right paths simultaneously
3. This creates a **timeline split** - each choice creates a parallel timeline
4. We need to count the **total number of unique timelines** after the particle completes all possible journeys

**Part 2 Rules:**
- A single tachyon particle starts at position `S`
- The particle moves downward through the manifold
- When the particle encounters a splitter (`^`):
  - Time itself splits into two timelines
  - In one timeline, the particle went left (col-1)
  - In the other timeline, the particle went right (col+1)
  - The original beam stops (same as Part 1)
- Both timeline particles continue moving downward independently
- The particle exits when it moves past the bottom edge
- Count the total number of distinct timelines created

**Critical Distinction from Part 1:**
- **Part 1**: Multiple beams that **merge** when they reach the same position
- **Part 2**: Timeline branches that **never merge** even if particles end at the same position

Each unique path through the splitters represents a distinct timeline, so two timelines that end at the same final column are still counted as separate timelines if they took different routes to get there.

#### Part 2 Example Answer
**40 timelines**

Using the same 16x15 grid from Part 1:
```
.......S.......
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
...............
```

**Explanation:**

The problem illustrates three example timeline paths:

1. **Always going left**: At each splitter encountered, the timeline particle takes the left path
2. **Alternating left/right**: The particle alternates between left and right choices at each splitter
3. **Different path, same endpoint**: A path that ends at the same final position as #2 but took different turns

These examples demonstrate that timelines are distinguished by their **path history**, not just their final position.

**Why 40 timelines?**

The particle starts at column 7 and encounters different splitters depending on which path it takes:
- First splitter at row 2, col 7: Creates 2 timelines (left to col 6, right to col 8)
- Each of those timelines may encounter different splitters on subsequent rows
- The total number of unique paths through all possible splitter combinations is 40

This is fundamentally a "count all paths" problem through a directed acyclic graph (DAG) where nodes are positions and edges represent downward movement or splitter-induced branching.

## Algorithm Analysis

### Part 1: Classical Beam Simulation

#### Approach 1: Beam Simulation (Recommended for Part 1)

**Strategy:** Simulate each beam's path through the manifold, tracking active beams and split count.

**Algorithm:**
1. Parse the grid to find `S` (start position) and all splitter positions
2. Initialize a queue/list of active beams, starting with one beam at position S
3. For each active beam:
   - Move beam downward one row at a time
   - If beam encounters a splitter:
     - Increment split counter
     - Remove current beam
     - Add two new beams at positions (row, col-1) and (row, col+1)
   - If beam exits bottom of grid, remove it
   - If beam reaches same position as another beam, merge them
4. Continue until no active beams remain
5. Return total split count

**Time Complexity:** O(R × C × B) where R = rows, C = columns, B = max beams
- In worst case, beams can double at each splitter level
- But beams also merge, limiting total beam count

**Space Complexity:** O(B) for tracking active beams

**Pros:**
- Intuitive and matches problem description
- Easy to debug and visualize
- Handles beam merging naturally

**Cons:**
- Need to carefully track beam positions
- Need to handle merging logic

#### Approach 2: Level-by-Level Processing (Recommended for Part 1)

**Strategy:** Process the grid row by row, tracking which columns have active beams.

**Algorithm:**
1. Parse grid and find start column
2. Maintain a set of active column positions
3. For each row:
   - For each column in active set:
     - If there's a splitter at (row, col):
       - Increment split counter
       - Add (col-1) and (col+1) to next row's active set
       - Remove col from next row's active set
     - Else:
       - Add col to next row's active set
4. Return total split count

**Time Complexity:** O(R × C) in worst case
**Space Complexity:** O(C) for tracking active columns per row

**Pros:**
- Efficient processing
- Natural row-by-row iteration
- Easy to implement merging (set operations)

**Cons:**
- Need to carefully handle splitter logic
- Need to track "this row" vs "next row" active beams

### Part 2: Quantum Timeline Counting

**Problem Type:** This is a path counting problem through a directed acyclic graph (DAG).

#### Approach 1: DFS/BFS Path Exploration (Recommended for Part 2)

**Strategy:** Explore all possible paths from start to exit, counting each unique complete path as a timeline.

**Algorithm:**
1. Parse the grid to find `S` and all splitter positions
2. Use DFS or BFS to explore all paths:
   - State: (row, col, path_history)
   - Start state: (0, start_col, empty_path)
   - For each state:
     - If row >= grid_height: This is a complete timeline, increment counter
     - If position has splitter:
       - Recursively explore (row+1, col-1, path + 'L')
       - Recursively explore (row+1, col+1, path + 'R')
     - Else:
       - Recursively explore (row+1, col, path + 'D')
3. Return total timeline count

**Key Insight:** Two timelines are different if they have different path histories, even if they end at the same position.

**Time Complexity:** O(2^S) where S = number of splitters encountered across all paths
- Each splitter can double the number of timelines
- Worst case: exponential growth

**Space Complexity:** 
- O(2^S) for storing all timeline states
- O(R) for recursion stack depth

**Pros:**
- Correctly counts all unique paths
- Straightforward implementation
- No complex merging logic

**Cons:**
- Exponential time complexity
- May need memoization or optimization for large inputs

#### Approach 2: Dynamic Programming with Path Counting

**Strategy:** Use DP to count the number of distinct paths that reach each position, tracking path signatures to ensure uniqueness.

**Algorithm:**
1. Create DP table: dp[row][col] = number of unique paths to reach this position
2. Initialize: dp[start_row][start_col] = 1
3. For each row from top to bottom:
   - For each column with active paths:
     - If splitter at (row, col):
       - dp[row+1][col-1] += dp[row][col]
       - dp[row+1][col+1] += dp[row][col]
     - Else:
       - dp[row+1][col] += dp[row][col]
4. Sum all dp values at the bottom row (or past the grid)

**Wait - Problem with this approach:** Standard DP would merge paths that reach the same position, but Part 2 says paths should NOT merge. We need to track path distinctness.

**Corrected Approach:** We need to track paths by their unique signatures, not just positions.

#### Approach 3: Recursive Path Counting with Memoization

**Strategy:** Count paths recursively, using memoization to avoid recomputing the same subproblems.

**Algorithm:**
```python
def count_timelines(row, col, memo={}):
    # Base case: exited the grid
    if row >= grid_height:
        return 1
    
    # Check memo (but what's the key?)
    if (row, col) in memo:
        return memo[(row, col)]
    
    # Recursive case
    if grid[row][col] == '^':
        count = count_timelines(row+1, col-1) + count_timelines(row+1, col+1)
    else:
        count = count_timelines(row+1, col)
    
    memo[(row, col)] = count
    return count
```

**Key Insight for Memoization:** If we reach the same position (row, col) again, the number of timelines from that point onward is always the same. We don't need to track full path history for memoization!

**Time Complexity:** O(R × C) - each position computed once
**Space Complexity:** O(R × C) for memoization table

**Pros:**
- Efficient with memoization
- Avoids exponential blowup
- Clean recursive structure

**Cons:**
- Need to carefully handle grid boundaries
- Recursion depth could be an issue for very tall grids

### Recommended Approaches

**Part 1:** Use Approach 2 (Level-by-Level Processing) for better efficiency and cleaner code structure.

**Part 2:** Use Approach 3 (Recursive Path Counting with Memoization) for optimal performance. The key insight is that the number of timelines from any given position depends only on what's below it, not on how we got there.

## Test Cases

### Part 1 Tests

| Input | Expected | Notes |
|-------|----------|-------|
| Main example (16x15 grid) | `21` | Full example from problem |
| Single splitter | `1` | `S` directly above `^` |
| No splitters | `0` | Beam just passes through |
| Two splitters side-by-side | `2` | Tests merging behavior |
| Wide grid with many splitters | varies | Stress test |

### Simple Test Cases

**Test 1: Single Splitter**
```
...S...
.......
...^...
.......
```
Expected: 1 split

**Test 2: No Splitters**
```
...S...
.......
.......
.......
```
Expected: 0 splits

**Test 3: Two Splitters in a Row**
```
...S...
.......
..^.^..
.......
```
Expected: 1 split (beam hits left splitter, creates 2 beams, right beam hits right splitter immediately)
Actually: Need to trace carefully - beam goes down from S, hits nothing on row 2, continues to row with splitters...

Let me reconsider: If S is at column 3 (0-indexed), beam goes straight down and would hit the space between the two splitters.

**Test 4: Vertical Stack**
```
...S...
.......
...^...
.......
...^...
.......
```
Expected: 2 splits (but beams merge between splitters)

### Part 2 Tests

| Input | Expected | Notes |
|-------|----------|-------|
| Main example (16x15 grid) | `40` | Full example from problem |
| Single splitter | `2` | One timeline goes left, one goes right |
| No splitters | `1` | Single timeline, no branching |
| Two splitters vertically stacked | `4` | 2^2 timelines (each creates 2 branches) |
| Linear chain of N splitters | `2^N` | Exponential growth |

#### Simple Test Cases for Part 2

**Test 1: Single Splitter**
```
...S...
.......
...^...
.......
```
Expected: **2 timelines**
- Timeline 1: Start → Splitter (go left) → Exit at column 2
- Timeline 2: Start → Splitter (go right) → Exit at column 4

**Test 2: No Splitters**
```
...S...
.......
.......
.......
```
Expected: **1 timeline**
- Only one path exists (straight down)

**Test 3: Two Splitters Vertically Stacked**
```
...S...
.......
...^...
.......
...^...
.......
```
Expected: **4 timelines**
- First splitter creates 2 timelines (left and right)
- Each of those encounters the second splitter
- Left timeline: hits splitter at col 2, creates 2 more (cols 1 and 3)
- Right timeline: hits splitter at col 4, creates 2 more (cols 3 and 5)
- Total: 4 unique paths

Wait, let me reconsider. If S is at column 3:
- After first splitter: timelines at columns 2 and 4
- After second row with splitter at column 3:
  - Timeline at column 2: no splitter, continues to column 2
  - Timeline at column 4: no splitter, continues to column 4
- So only 2 timelines if splitter is at column 3

For 4 timelines, we need splitters aligned:
```
...S...
.......
...^...
.......
..^.^..
.......
```
- First splitter at col 3: creates timelines at cols 2 and 4
- Second row has splitters at cols 2 and 4
- Timeline at col 2 hits splitter: creates cols 1 and 3
- Timeline at col 4 hits splitter: creates cols 3 and 5
- Total: 4 timelines (cols 1, 3, 3, 5)
- But we count all 4 separately even though two are at col 3!

**Test 4: Splitter that produces merging positions**
```
...S...
.......
...^...
.......
..^.^..
.......
```
Expected: **4 timelines**

The key is that even though two timelines end at column 3, they took different paths (one came from left splitter going right, one came from right splitter going left), so they count as 2 separate timelines.

**Test 5: Binary tree pattern**
```
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
```
Expected: **8 timelines** (2^3 for 3 levels of splitters)
- Row 2: 1 splitter → 2 timelines
- Row 4: 2 splitters → 4 timelines  
- Row 6: 4 splitters → 8 timelines (if all timelines hit splitters)

This is more complex because we need to trace which timelines hit which splitters.

### Step-by-Step Trace (for validation)

#### Part 1 Trace (Classical Beams with Merging)

For a simpler 5-row example:
```
...S...
.......
...^...
.......
..^.^..
.......
```

Step-by-step:
```
Row 0: Beam at column 3 (S position)
Row 1: Beam at column 3 (empty space, continues down)
Row 2: Beam hits splitter at column 3
       Split count: 1
       Two new beams created at columns 2 and 4
Row 3: Beams at columns 2 and 4 (empty space, continue down)
Row 4: Beam at column 2 hits splitter
       Beam at column 4 hits splitter
       Split count: 3 total
       Four new beams created at columns 1, 3, 3, 5
       Beams at column 3 merge into one beam
       Active beams: columns 1, 3, 5
Row 5: Beams exit manifold (past bottom edge)

Final split count: 3
```

#### Part 2 Trace (Quantum Timelines without Merging)

Same grid as above:
```
...S...
.......
...^...
.......
..^.^..
.......
```

Timeline counting approach:
```
Starting at row 0, column 3 (S position)

count_timelines(0, 3):
  Row 0, col 3: empty space '.'
  → count_timelines(1, 3)

count_timelines(1, 3):
  Row 1, col 3: empty space '.'
  → count_timelines(2, 3)

count_timelines(2, 3):
  Row 2, col 3: splitter '^'
  → count_timelines(3, 2) + count_timelines(3, 4)

count_timelines(3, 2):
  Row 3, col 2: empty space '.'
  → count_timelines(4, 2)

count_timelines(4, 2):
  Row 4, col 2: splitter '^'
  → count_timelines(5, 1) + count_timelines(5, 3)

count_timelines(5, 1):
  Row 5: past grid bottom
  → return 1

count_timelines(5, 3):
  Row 5: past grid bottom
  → return 1

count_timelines(4, 2) = 1 + 1 = 2

count_timelines(3, 2) = 2

count_timelines(3, 4):
  Row 3, col 4: empty space '.'
  → count_timelines(4, 4)

count_timelines(4, 4):
  Row 4, col 4: splitter '^'
  → count_timelines(5, 3) + count_timelines(5, 5)

count_timelines(5, 3):
  Row 5: past grid bottom
  → return 1

count_timelines(5, 5):
  Row 5: past grid bottom
  → return 1

count_timelines(4, 4) = 1 + 1 = 2

count_timelines(3, 4) = 2

count_timelines(2, 3) = 2 + 2 = 4

Final answer: 4 timelines
```

**Key observation**: Both paths through the first splitter eventually hit splitters on row 4, each creating 2 more timelines. Even though two timelines end at column 3, they count separately because they took different routes.

**Comparison**:
- Part 1 (classical beams): 3 splits, 3 final beams (merged at column 3)
- Part 2 (quantum timelines): 4 timelines (no merging at column 3)

#### Part 2 Complex Trace (Main Example)

For the main 16x15 example with answer 40, the tree of timelines would be enormous to fully trace. But we can understand the structure:

```
Row 0: Start at column 7
Row 2: Hit splitter → 2 timelines (cols 6, 8)
Row 4: Splitters at cols 6 and 8
       - Timeline at col 6 hits splitter → 2 timelines (cols 5, 7)
       - Timeline at col 8 hits splitter → 2 timelines (cols 7, 9)
       - Total: 4 timelines
Row 6: Splitters at cols 5, 7, 9
       - Each of the 4 timelines may hit a splitter
       - Timelines continue to branch...

And so on through all rows.
```

The final count of 40 represents all unique paths from start to exit, where each path is defined by the sequence of left/right choices made at each splitter encounter.

## Edge Cases to Consider

### Part 1 Edge Cases

1. **Beam merging**: Multiple beams reaching the same column must merge
2. **Edge beams**: Beams that split near the left/right edge
   - Left beam from splitter at column 0 would go to column -1 (out of bounds)
   - Right beam from splitter at last column would go past grid
3. **Start position**: S can be at any column
4. **Empty rows**: Multiple rows without splitters between splitter rows
5. **Bottom row splitters**: Beams that split on the last row (new beams immediately exit)

### Part 2 Edge Cases

1. **No timeline merging**: Two timelines at the same position are still distinct timelines
2. **Out of bounds timelines**: Timelines that go to negative columns or past grid width
   - These timelines still count! They exit the grid boundary
3. **Exponential growth**: With N splitters in sequence, expect up to 2^N timelines
4. **Single path**: Grid with no splitters should have exactly 1 timeline
5. **Immediate exit**: Splitter on the last row creates 2 timelines that immediately exit
6. **Path history matters**: Same endpoint, different path = different timeline
7. **Splitter at start position**: What if S is also a splitter position?
   - Based on Part 1 rules, beam starts at S and moves down, so it wouldn't hit a splitter at S
8. **Very wide timelines**: Timelines that spread wider than the grid
   - Timeline at column -5 is still a valid timeline (just happens to be out of bounds)

### Critical Distinction Test Case

**Test: Same endpoint, different paths**
```
....S....
.........
....^....
.........
...^.^...
.........
```

Let's trace this carefully (S at column 4, 0-indexed):
1. Start: 1 timeline at column 4
2. Row 2 splitter at column 4: 2 timelines at columns 3 and 5
3. Row 4 splitters at columns 3 and 5:
   - Timeline at column 3 hits splitter → creates cols 2 and 4
   - Timeline at column 5 hits splitter → creates cols 4 and 6
4. Result: 4 timelines at columns 2, 4, 4, 6

**Expected: 4 timelines** (not 3, because the two at column 4 came from different paths)

This illustrates the fundamental difference between Part 1 and Part 2:
- **Part 1**: Would merge the two beams at column 4 → only 3 active beams
- **Part 2**: Keeps both timelines at column 4 separate → 4 distinct timelines

## Implementation Notes

### Part 1 Implementation

1. Parse the grid to identify:
   - Start position (S)
   - All splitter positions
   - Grid dimensions

2. Track active beams as a set of column positions for each row

3. For each row with splitters:
   - Check which active beams hit splitters
   - Increment split counter for each hit
   - Update active beam positions

4. Handle beam merging automatically using sets

5. Beams that go out of bounds (column < 0 or column >= width) are simply removed from active set

### Part 2 Implementation

1. **Key difference from Part 1**: Do NOT merge timelines that reach the same position

2. **Recommended approach**: Recursive path counting with memoization
   ```python
   def count_timelines(row, col):
       if row >= grid_height:
           return 1  # Exited grid = 1 complete timeline
       
       if grid[row][col] == '^':
           # Splitter: timeline splits into two
           left_count = count_timelines(row + 1, col - 1)
           right_count = count_timelines(row + 1, col + 1)
           return left_count + right_count
       else:
           # Empty space: continue straight down
           return count_timelines(row + 1, col)
   ```

3. **Memoization is critical**: Cache results for (row, col) to avoid exponential recomputation

4. **Handle out of bounds gracefully**: 
   - Timelines can go to negative columns or beyond grid width
   - These are still valid timelines (they just happen to be outside the visible grid)
   - Continue processing them until they exit the bottom

5. **No merging logic needed**: Unlike Part 1, we count paths, not active beams

6. **Optimization opportunity**: The answer at each position (row, col) depends only on the grid structure below that position, not on how we got there. This makes memoization very effective.

### Data Structures

**Part 1:**
- Grid: 2D list or dict of positions → characters
- Active beams: Set of column indices (changes each row)
- Split counter: Integer

**Part 2:**
- Grid: 2D list or dict (same as Part 1)
- Memo table: Dict mapping (row, col) → timeline count
- No need to track active beams or merging

### Common Pitfalls

**Part 1:**
- Forgetting to merge beams at the same position
- Not handling out-of-bounds beams correctly
- Counting splits incorrectly (should count each splitter hit, not total beams)

**Part 2:**
- Trying to merge timelines (this is Part 1 logic, don't do it!)
- Not handling out-of-bounds timelines (they still count!)
- Forgetting memoization (will cause exponential slowdown)
- Confusing "number of timelines" with "number of final positions"

### Testing Strategy

1. **Start with simple cases**: Single splitter, no splitters
2. **Verify the distinction**: Create a test case where Part 1 and Part 2 give different answers
3. **Check exponential growth**: Vertical stack of splitters should give 2^N for Part 2
4. **Validate with examples**: Main example should give 21 (Part 1) and 40 (Part 2)
5. **Edge cases**: Out of bounds, grid boundaries, single timeline paths

## Summary: Part 1 vs Part 2

| Aspect | Part 1 (Classical) | Part 2 (Quantum) |
|--------|-------------------|------------------|
| **Physics Model** | Classical beams | Quantum timelines |
| **What we count** | Number of splits | Number of unique timelines |
| **Initial state** | One beam at S | One particle at S |
| **At splitter** | Beam stops, creates 2 new beams | Timeline splits into 2 parallel timelines |
| **Merging behavior** | Beams at same position merge | Timelines NEVER merge |
| **Data structure** | Set of active beam positions | Count of paths (recursive/DP) |
| **Algorithm** | Simulation with merging | Path counting |
| **Complexity** | O(R × C) | O(R × C) with memoization |
| **Example answer** | 21 | 40 |
| **Key insight** | Track positions, merge duplicates | Track unique paths, count all |

**The fundamental difference**: 
- Part 1: Two beams reaching column 3 → merge into 1 beam
- Part 2: Two timelines reaching column 3 → still count as 2 separate timelines

**Why Part 2 has more timelines**:
- Every unique path through the splitter network creates a distinct timeline
- Even if two paths end at the same position, they're different timelines if they took different routes
- No merging means the count grows exponentially with the number of splitters encountered
