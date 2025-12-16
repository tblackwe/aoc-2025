# Day 11: Reactor

## Problem Description

**Core Mechanic**: Graph traversal - find all distinct paths from a starting node to an ending node in a directed graph.

This puzzle involves analyzing a network of devices where each device has outputs connected to other devices. We need to count all possible paths that data can take from the `you` device to the `out` device, where data flows only forward through outputs (no backtracking).

**What makes this challenging**: This is an all-paths problem (not just shortest path), which requires exhaustive search. We must enumerate every possible route through the graph while handling potential cycles and multiple edges between nodes.

## Input Format

The input consists of lines defining a directed graph where each line specifies a device and its output connections.

**Format**: `device_name: output1 output2 output3 ...`
- Device names are alphanumeric strings (e.g., `you`, `bbb`, `out`)
- Colon separates the device name from its outputs
- Outputs are space-separated device names
- A device can have 0 or more outputs
- Multiple devices can have edges to the same target

**Example Input**:
```
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
```

**Parsing Notes**:
- Each line creates one or more directed edges in the graph
- The first device on each line is the source
- All subsequent devices are targets (destinations)
- The graph may have cycles (though paths to `out` likely won't revisit nodes)
- Not all devices may be reachable from `you`
- Some devices may not lead to `out`

## Output Format

A single integer representing the total count of distinct paths from the device `you` to the device `out`.

**Example Output**:
```
5
```

## Requirements

### Part 1

**Objective**: Count all distinct paths from the device labeled `you` to the device labeled `out`.

**Definition of a Path**:
- A path is a sequence of device connections: `you → device1 → device2 → ... → out`
- Data flows only through outputs (forward direction only)
- A path is complete when it reaches `out`
- Different sequences of devices count as different paths, even if they visit some of the same nodes

**Key Constraints**:
- Paths start at `you` (source node)
- Paths end at `out` (target node)
- Paths follow directed edges only
- No backtracking allowed (data flows forward)

#### Part 1 Example Answer

For the example input above: **5 paths**

**Explanation - All Paths Enumerated**:

Starting from `you`, which connects to `bbb` and `ccc`:

**Paths through `bbb`**:
1. `you → bbb → ddd → ggg → out`
   - Go to `bbb`, then `ddd`, then `ggg`, then reach `out`
2. `you → bbb → eee → out`
   - Go to `bbb`, then `eee`, directly to `out`

**Paths through `ccc`**:
3. `you → ccc → ddd → ggg → out`
   - Go to `ccc`, then `ddd`, then `ggg`, then reach `out`
4. `you → ccc → eee → out`
   - Go to `ccc`, then `eee`, directly to `out`
5. `you → ccc → fff → out`
   - Go to `ccc`, then `fff`, directly to `out`

**Total**: 5 distinct paths

**Why other devices don't create additional paths**:
- `aaa` connects to `you` and `hhh`, but since we must *start* at `you`, we never traverse from `aaa`
- `hhh` and `iii` are only reachable from `aaa`, which isn't on any path from `you` to `out`

### Part 2

**Objective**: Count all distinct paths from the device labeled `svr` (server rack) to the device labeled `out`, where the paths must visit BOTH `dac` (digital-to-analog converter) AND `fft` (fast Fourier transform) devices.

**Key Changes from Part 1**:
1. **Different source node**: Start at `svr` instead of `you`
2. **Required intermediate nodes**: Path MUST visit both `dac` AND `fft` (in any order)
3. **Constraint validation**: Only count paths that satisfy both visitation requirements

**Definition of a Valid Path**:
- A path is a sequence of device connections: `svr → device1 → device2 → ... → out`
- The path must pass through `dac` at some point
- The path must pass through `fft` at some point
- The order of visiting `dac` and `fft` doesn't matter
- A path is complete and valid only when it:
  1. Reaches `out`
  2. Has visited both `dac` and `fft` along the way

#### Part 2 Example

**Input**:
```
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
```

**All 8 Paths from `svr` to `out`**:

1. `svr → aaa → fft → ccc → ddd → hub → fff → ggg → out`
   - Visits: fft ✓, dac ✗ → **INVALID**

2. `svr → aaa → fft → ccc → ddd → hub → fff → hhh → out`
   - Visits: fft ✓, dac ✗ → **INVALID**

3. `svr → aaa → fft → ccc → eee → dac → fff → ggg → out`
   - Visits: fft ✓, dac ✓ → **VALID** ✓

4. `svr → aaa → fft → ccc → eee → dac → fff → hhh → out`
   - Visits: fft ✓, dac ✓ → **VALID** ✓

5. `svr → bbb → tty → ccc → ddd → hub → fff → ggg → out`
   - Visits: fft ✗, dac ✗ → **INVALID**

6. `svr → bbb → tty → ccc → ddd → hub → fff → hhh → out`
   - Visits: fft ✗, dac ✗ → **INVALID**

7. `svr → bbb → tty → ccc → eee → dac → fff → ggg → out`
   - Visits: fft ✗, dac ✓ → **INVALID**

8. `svr → bbb → tty → ccc → eee → dac → fff → hhh → out`
   - Visits: fft ✗, dac ✓ → **INVALID**

**Expected Answer**: **2 paths** (paths #3 and #4)

**Why Only 2 Are Valid**:
- Paths 1-4 go through `aaa → fft`, so they visit `fft`
  - Paths 1-2 go through `ddd → hub → fff`, skipping `dac` → INVALID
  - Paths 3-4 go through `eee → dac → fff`, visiting both → VALID ✓
- Paths 5-8 go through `bbb → tty`, which bypasses `fft` entirely
  - Even though paths 7-8 visit `dac`, they miss `fft` → INVALID

**Key Insight**: The constraint requires BOTH nodes to be visited. Paths that visit only one or neither don't count.

#### Algorithm Modifications for Part 2

The core DFS algorithm needs to be enhanced to track which required nodes have been visited:

**Modified Approach**: DFS with Required Nodes Tracking

```python
def count_paths_with_requirements(graph, current, target, visited, required_nodes):
    """
    Count paths that visit all required nodes.
    
    Args:
        graph: Adjacency list
        current: Current node
        target: Destination node
        visited: Set of nodes in current path (for cycle detection)
        required_nodes: Set of nodes that must be visited
    
    Returns:
        Number of valid paths from current to target that visit all required nodes
    """
    if current == target:
        # Only count this path if all required nodes were visited
        return 1 if len(required_nodes) == 0 else 0
    
    if current in visited:
        return 0  # Cycle detected
    
    visited.add(current)
    
    # Update required nodes if we just visited one
    new_required = required_nodes.copy()
    if current in new_required:
        new_required.remove(current)
    
    total_paths = 0
    for neighbor in graph.get(current, []):
        total_paths += count_paths_with_requirements(
            graph, neighbor, target, visited, new_required
        )
    
    visited.remove(current)  # Backtrack
    return total_paths

# Initial call:
# count_paths_with_requirements(graph, 'svr', 'out', set(), {'dac', 'fft'})
```

**Alternative Implementation - Track Visited Flags**:

```python
def count_paths_part2(graph, current, target, visited, seen_dac, seen_fft):
    """
    Track required nodes with boolean flags.
    """
    if current == target:
        return 1 if (seen_dac and seen_fft) else 0
    
    if current in visited:
        return 0
    
    visited.add(current)
    
    # Update flags if we're at a required node
    if current == 'dac':
        seen_dac = True
    if current == 'fft':
        seen_fft = True
    
    total_paths = 0
    for neighbor in graph.get(current, []):
        total_paths += count_paths_part2(
            graph, neighbor, target, visited, seen_dac, seen_fft
        )
    
    visited.remove(current)
    return total_paths
```

**Time Complexity Analysis**:
- **Worst case**: Still O(n!) for complete graphs
- **Practical**: O(b^d) where b is branching factor, d is depth
- **Additional overhead**: Minimal - just tracking 2 boolean flags or a set
- **Pruning opportunity**: Could terminate early if path reaches `out` without visiting required nodes (already handled by checking at target)

**Space Complexity Analysis**:
- **Call stack**: O(d) - maximum path depth
- **Visited set**: O(d) - current path nodes
- **Required nodes tracking**: O(1) - only 2 nodes to track
- **Total**: O(V + E + d) - same as Part 1

**Key Differences in Implementation**:
1. Change source from `you` to `svr`
2. Add parameter to track required nodes (`dac` and `fft`)
3. Update tracking as we visit nodes
4. Only count paths that have seen ALL required nodes when reaching `out`
5. No need to change cycle detection or backtracking logic

#### Part 2 Test Cases

**Main Example**:
```
Input: (as shown above with svr, dac, fft, etc.)
Expected: 2
Notes: Tests basic required node constraint with multiple paths
```

**Simple Cases**:

| Input | Expected | Notes |
|-------|----------|-------|
| `svr: dac\ndac: fft\nfft: out` | 1 | Linear path visiting both in order |
| `svr: fft\nfft: dac\ndac: out` | 1 | Linear path visiting both in reverse order |
| `svr: out` | 0 | Direct path misses both required nodes |
| `svr: dac\ndac: out` | 0 | Path visits dac but not fft |
| `svr: fft\nfft: out` | 0 | Path visits fft but not dac |

**Edge Cases**:

| Input | Expected | Notes |
|-------|----------|-------|
| `svr: a b\na: dac\nb: fft\ndac: out\nfft: out` | 0 | Two paths but each visits only one required node |
| `svr: a\na: dac fft\ndac: out\nfft: out` | 0 | Parallel paths after required nodes, but can't visit both |
| `svr: a\na: dac\ndac: fft\nfft: out` | 1 | Must visit in specific order due to graph structure |
| `svr: dac\ndac: svr` | 0 | Cycle with required node but no path to out |

**Corner Cases**:

| Input | Expected | Notes |
|-------|----------|-------|
| `svr: a b\na: dac\nb: dac\ndac: fft\nfft: out` | 2 | Both paths converge and visit both nodes |
| `svr: a\na: dac\ndac: b c\nb: fft\nc: fft\nfft: out` | 2 | After first required node, split then converge at second |
| `svr: dac fft\ndac: fft\nfft: dac out\ndac: out` | 3 | Multiple ways to visit both nodes with cycles |
| `svr: a\na: b c\nb: dac\nc: fft\ndac: fft\nfft: out` | 2 | Diamond pattern where both branches visit one required node, then merge |

#### Part 2 Implementation Notes

**Common Pitfalls**:
1. **Forgetting order independence**: Both `svr → dac → fft → out` and `svr → fft → dac → out` are valid
2. **Checking requirements too early**: Don't filter paths until they reach `out`
3. **Mutable state bug**: If using sets for required nodes, must copy when passing to recursive calls
4. **Flag propagation**: Must pass updated boolean flags down the recursion tree
5. **Double-counting**: Each complete path should only be counted once, even if it visits required nodes multiple times

**Optimization Opportunities**:
1. **Early termination**: If a node can't reach `out`, don't explore it (requires preprocessing)
2. **Memoization limitation**: Can't easily cache because path validity depends on visited history
3. **Graph preprocessing**: Identify nodes that can't reach both required nodes + `out`

**Edge Cases Specific to Part 2**:
1. **Required nodes same as source/target**: What if `svr == dac`? (Probably not in actual input)
2. **Required nodes unreachable**: If graph doesn't contain `dac` or `fft`, answer is 0
3. **Required nodes disconnected**: If no path exists through both, answer is 0
4. **Multiple visits**: Visiting a required node twice still counts (path only needs one visit)
5. **Out node is a required node**: If `out == dac`, handled by flag checking at end

## Algorithm Analysis

### Problem Classification

**Primary Pattern**: Graph - All Paths Enumeration
- **Subtype**: Directed acyclic graph (DAG) path counting
- **Related Patterns**: 
  - Tree traversal (if graph is tree-like)
  - Depth-first search with path tracking
  - Backtracking

### Recommended Approach: Depth-First Search (DFS) with Backtracking

**Algorithm Description**:
1. Build an adjacency list representation of the directed graph
2. Use DFS to explore all paths from `you` to `out`
3. Track current path to detect cycles (avoid infinite loops)
4. Count each time we reach `out`
5. Backtrack to explore alternative branches

**Why This Approach**:
- DFS naturally explores all possible paths
- Backtracking allows us to try all branches from each node
- Path tracking prevents infinite loops in case of cycles
- Simple to implement and understand
- Works well for moderate-sized graphs

**Pseudocode**:
```python
def count_paths(graph, current, target, visited):
    if current == target:
        return 1  # Found a complete path
    
    if current in visited:
        return 0  # Cycle detected, avoid infinite loop
    
    visited.add(current)
    total_paths = 0
    
    for neighbor in graph.get(current, []):
        total_paths += count_paths(graph, neighbor, target, visited)
    
    visited.remove(current)  # Backtrack
    return total_paths
```

**Time Complexity**: 
- **Worst case**: O(n!) where n is number of nodes
  - In a complete graph, we could explore every permutation
  - For most AoC inputs: O(b^d) where b is branching factor and d is depth
- **Best case**: O(n) for a simple linear path
- **Expected**: O(n * m) where m is average number of paths, likely manageable for Part 1

**Space Complexity**:
- **Call stack**: O(d) where d is maximum depth of any path
- **Visited set**: O(d) to track current path
- **Graph storage**: O(V + E) where V is vertices and E is edges
- **Total**: O(V + E + d)

**Data Structures**:

1. **Adjacency List (dict of lists)**
   - Purpose: Store graph structure
   - Format: `{device: [output1, output2, ...]}`
   - Why: O(1) lookup of neighbors, efficient iteration
   - Trade-off: More memory than adjacency matrix, but sparse graphs benefit

2. **Visited Set**
   - Purpose: Track current path to detect cycles
   - Why: O(1) membership testing
   - Important: Must backtrack (remove from set) when unwinding recursion

3. **Path Counter (integer)**
   - Purpose: Accumulate total path count
   - Alternative: Could collect actual paths if needed for debugging

### Alternative Approaches

#### Approach 2: Breadth-First Search (BFS) with Path Storage

**Description**: Use BFS but store the entire path in queue along with current node.

**Pros**:
- Can track path length easily
- Iterative (no stack overflow risk)
- Natural for shortest-path problems

**Cons**:
- Memory intensive - stores full paths in queue
- Doesn't leverage call stack for backtracking
- More complex path tracking

**Complexity**:
- Time: O(b^d) similar to DFS
- Space: O(b^d) - much worse, stores all partial paths

**When to use**: If we need path lengths or want iterative solution

#### Approach 3: Dynamic Programming with Memoization

**Description**: Cache the number of paths from each node to target.

**Pros**:
- Avoids recomputing paths from same node
- Optimal for graphs with significant overlap
- Time complexity can be reduced to O(V + E)

**Cons**:
- Only works for DAGs (no cycles)
- More complex implementation
- May not be necessary for Part 1

**Implementation**:
```python
def count_paths_dp(graph, current, target, memo):
    if current == target:
        return 1
    if current in memo:
        return memo[current]
    
    total = 0
    for neighbor in graph.get(current, []):
        total += count_paths_dp(graph, neighbor, target, memo)
    
    memo[current] = total
    return total
```

**When to use**: If Part 2 requires handling very large graphs or many repeated queries

#### Approach 4: Topological Sort + Dynamic Programming

**Description**: 
1. Verify graph is a DAG
2. Perform topological sort
3. Process nodes in reverse topological order
4. For each node, sum paths from all its successors

**Pros**:
- Most efficient for large DAGs: O(V + E)
- No recursion needed
- Clean iterative solution

**Cons**:
- Requires DAG (fails if cycles exist)
- More complex initial setup
- Overkill for small graphs

**When to use**: If Part 2 scales significantly or requires multiple queries

### Recommended Implementation Strategy

**For Part 1**: Use **DFS with backtracking** (Approach 1)
- Simple and correct
- Fast enough for expected input size
- Easy to debug
- Naturally handles the all-paths requirement

**For Part 2 considerations**: 
- If scaling is required, switch to **DP with memoization** (Approach 3)
- If graph has cycles, stick with DFS but add cycle detection
- If counting isn't enough (need actual paths), adapt DFS to collect paths

## Implementation Guidance

### Helper Functions to Create

1. **`parse_input(filename) -> dict`**
   - Read input file
   - Build adjacency list representation
   - Return: `{device_name: [list_of_outputs]}`

2. **`count_all_paths(graph, start, end) -> int`**
   - Main DFS function
   - Initialize visited set
   - Call recursive helper
   - Return total path count

3. **`dfs_count_paths(graph, current, target, visited) -> int`**
   - Recursive path counting
   - Base case: current == target → return 1
   - Cycle check: current in visited → return 0
   - Recursive case: sum paths through all neighbors

4. **`solve_part1(filename) -> int`** (Optional)
   - Convenience function combining parse + count
   - Use for main solution

### Common Pitfalls to Avoid

1. **Cycle Handling**: 
   - MUST track visited nodes in current path
   - MUST backtrack (remove from visited) after exploring each branch
   - Without this: infinite recursion on cycles

2. **Graph Direction**:
   - Data flows from device → its outputs (forward only)
   - Don't build reverse edges
   - The graph is directed, not undirected

3. **Base Case Ordering**:
   - Check if at target BEFORE checking visited
   - Otherwise, reaching `out` might be blocked if visited

4. **Parsing Edge Cases**:
   - Devices with no outputs (terminal nodes other than `out`)
   - Devices not mentioned on left side (only as outputs)
   - Empty lines or whitespace

5. **Missing Nodes**:
   - `you` might not exist in input → handle gracefully
   - `out` might not be reachable → result is 0 paths
   - Some devices may have no path to `out`

### Edge Cases to Handle

1. **No path exists**: `you` and `out` are disconnected → return 0
2. **Direct connection**: `you: out` → return 1
3. **Single path**: Only one route exists → return 1
4. **Cycles in graph**: Must not cause infinite loop
5. **Isolated target**: `out` has no incoming edges → check reachability
6. **Source has no outputs**: `you` leads nowhere → return 0
7. **Large branching factor**: Many outputs per device → ensure all explored
8. **Deep paths**: Very long chains → watch for stack overflow (unlikely in AoC)

### Optimization Opportunities

1. **Early termination**: If DFS finds no path to `out` from a node, cache that result
2. **Memoization**: Cache path counts from each node to target
3. **Graph validation**: Check if `you` and `out` exist before starting
4. **Pruning**: Don't explore nodes that can't reach `out` (requires preprocessing)

## Test Plan

### Test Case Design

#### Main Example Test
```
Input:
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out

Expected: 5
Notes: Primary example from puzzle, tests multiple paths and convergence
```

#### Simple Cases

| Input | Expected | Notes |
|-------|----------|-------|
| `you: out` | 1 | Direct connection, simplest path |
| `you: a\na: out` | 1 | Single intermediate node |
| `you: a b\na: out\nb: out` | 2 | Two independent paths of length 2 |
| `you: a\na: b\nb: out` | 1 | Linear chain |

#### Edge Cases

| Input | Expected | Notes |
|-------|----------|-------|
| `you: a\na: you` | 0 | Cycle with no path to `out` |
| `you: a` | 0 | Dead end, `out` not reachable |
| `out: a` | 0 | Target has outputs but no incoming from `you` |
| `you: a\na: b c\nb: out\nc: out` | 2 | Diamond pattern - tests path independence |

#### Corner Cases

| Input | Expected | Notes |
|-------|----------|-------|
| `you: a b\na: c\nb: c\nc: out` | 2 | Paths converge then continue together |
| `you: a\na: b c\nb: out\nc: b` | 2 | One path direct, one through intermediate convergence |
| `you: a\na: a` | 0 | Self-loop with no exit |
| `you: a a` | 0 | Duplicate edges, no path to `out` |

### Step-by-Step Trace (Main Example Validation)

**Initial State**: Start at `you`

```
Graph structure:
  aaa → [you, hhh]
  you → [bbb, ccc]
  bbb → [ddd, eee]
  ccc → [ddd, eee, fff]
  ddd → [ggg]
  eee → [out]
  fff → [out]
  ggg → [out]
  hhh → [ccc, fff, iii]
  iii → [out]

Starting DFS from 'you':
  visited = {you}
  neighbors = [bbb, ccc]
  
  Branch 1: Explore you → bbb
    visited = {you, bbb}
    neighbors of bbb = [ddd, eee]
    
    Branch 1.1: Explore bbb → ddd
      visited = {you, bbb, ddd}
      neighbors of ddd = [ggg]
      
      Branch 1.1.1: Explore ddd → ggg
        visited = {you, bbb, ddd, ggg}
        neighbors of ggg = [out]
        
        Branch 1.1.1.1: Explore ggg → out
          ✓ PATH FOUND #1: you → bbb → ddd → ggg → out
          return 1
        
        return 1 from ggg
      return 1 from ddd
    
    Branch 1.2: Explore bbb → eee
      visited = {you, bbb, eee}
      neighbors of eee = [out]
      
      Branch 1.2.1: Explore eee → out
        ✓ PATH FOUND #2: you → bbb → eee → out
        return 1
      
      return 1 from eee
    
    return 2 from bbb
  
  Branch 2: Explore you → ccc
    visited = {you, ccc}
    neighbors of ccc = [ddd, eee, fff]
    
    Branch 2.1: Explore ccc → ddd
      visited = {you, ccc, ddd}
      neighbors of ddd = [ggg]
      
      Branch 2.1.1: Explore ddd → ggg
        visited = {you, ccc, ddd, ggg}
        neighbors of ggg = [out]
        
        Branch 2.1.1.1: Explore ggg → out
          ✓ PATH FOUND #3: you → ccc → ddd → ggg → out
          return 1
        
        return 1 from ggg
      return 1 from ddd
    
    Branch 2.2: Explore ccc → eee
      visited = {you, ccc, eee}
      neighbors of eee = [out]
      
      Branch 2.2.1: Explore eee → out
        ✓ PATH FOUND #4: you → ccc → eee → out
        return 1
      
      return 1 from eee
    
    Branch 2.3: Explore ccc → fff
      visited = {you, ccc, fff}
      neighbors of fff = [out]
      
      Branch 2.3.1: Explore fff → out
        ✓ PATH FOUND #5: you → ccc → fff → out
        return 1
      
      return 1 from fff
    
    return 3 from ccc
  
  Total: 2 + 3 = 5 paths
```

**Final Answer**: 5 paths from `you` to `out`

### Validation Checklist

Before submitting solution, verify:

- [ ] Parser correctly builds adjacency list from input
- [ ] Graph is directed (edges only go from device to its outputs)
- [ ] DFS correctly tracks visited nodes for current path
- [ ] DFS correctly backtracks (removes from visited) after exploring branches
- [ ] Base case returns 1 when reaching `out`
- [ ] Cycle detection prevents infinite recursion
- [ ] All test cases pass (main example returns 5)
- [ ] Edge cases handled (no path → 0, direct connection → 1)
- [ ] Works with devices not reachable from `you`
- [ ] Works with devices that don't lead to `out`

## Common AoC Patterns Present

1. **Graph Traversal**: Core pattern - exploring connected nodes
2. **All Paths Problem**: Unlike typical "shortest path", we need ALL paths
3. **Backtracking**: Essential for exploring all branches without missing any
4. **Depth-First Search**: Natural fit for exhaustive path enumeration
5. **Cycle Detection**: Using visited set to avoid infinite loops
6. **Parsing Structured Input**: Building graph from text specification

**Similar AoC Problems**:
- Finding all routes between locations
- Counting valid sequences through state machines
- Tree/graph path enumeration
- Network flow analysis (simpler version)
