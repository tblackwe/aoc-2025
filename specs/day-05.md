# Day 5: Cafeteria - Specification

## Problem Description

The Elves have a new inventory management system that tracks ingredient freshness using ID ranges. The system needs to determine which available ingredients are fresh based on inclusive ID ranges.

### Example

```
3-5
10-14
16-20
12-18

1
5
8
11
17
32
```

**Fresh ID Ranges** (above blank line):
- `3-5` means IDs 3, 4, and 5 are fresh
- `10-14` means IDs 10, 11, 12, 13, and 14 are fresh
- `16-20` means IDs 16, 17, 18, 19, and 20 are fresh
- `12-18` means IDs 12, 13, 14, 15, 16, 17, and 18 are fresh

**Available Ingredient IDs** (below blank line):
- `1` - spoiled (not in any range)
- `5` - **fresh** (in range 3-5)
- `8` - spoiled (not in any range)
- `11` - **fresh** (in range 10-14)
- `17` - **fresh** (in ranges 12-18 and 16-20)
- `32` - spoiled (not in any range)

**Answer**: 3 fresh ingredients

## Input Format

The input consists of two sections separated by a blank line:

1. **Fresh ID Ranges Section**: Multiple lines, each containing a range in format `START-END`
   - START and END are integers
   - Ranges are inclusive (both START and END are included)
   - Ranges can overlap
   - Order is not guaranteed to be sorted

2. **Available Ingredient IDs Section**: Multiple lines, each containing a single integer
   - One ingredient ID per line
   - IDs can appear in any order

## Output Format

**Part 1**: A single integer representing the count of available ingredient IDs that are fresh (fall within at least one range).

**Part 2**: A single integer representing the total count of unique ingredient IDs that are considered fresh according to all fresh ID ranges (ignoring the available IDs section).

## Algorithm Analysis

### Approach 1: Naive Set Expansion
**Strategy**: Expand all ranges into a set of fresh IDs, then check each available ID.

**Steps**:
1. Parse fresh ID ranges
2. For each range, generate all IDs from START to END
3. Store all fresh IDs in a set (automatically handles overlaps)
4. For each available ID, check if it exists in the set
5. Count matches

**Time Complexity**: O(R × M + N) where R is number of ranges, M is average range size, N is number of available IDs
**Space Complexity**: O(T) where T is total number of unique fresh IDs across all ranges

**Pros**:
- Simple to implement
- Fast lookups (O(1) per ID)
- Easy to understand

**Cons**:
- Memory intensive if ranges are large (e.g., 1-1000000)
- Slow initialization if ranges are large
- Not suitable for very large range values

**Best for**: Small to medium range sizes (< 100,000 total IDs)

### Approach 2: Range Checking
**Strategy**: For each available ID, iterate through all ranges to check if it falls within any.

**Steps**:
1. Parse fresh ID ranges into a list of (start, end) tuples
2. For each available ID:
   - Iterate through all ranges
   - Check if START ≤ ID ≤ END for any range
   - If found, mark as fresh
3. Count fresh IDs

**Time Complexity**: O(N × R) where N is number of available IDs, R is number of ranges
**Space Complexity**: O(R) for storing ranges

**Pros**:
- Memory efficient
- Works with arbitrarily large range values
- No preprocessing needed

**Cons**:
- Slower for large numbers of ranges
- Redundant checks for overlapping ranges

**Best for**: Few ranges or large range values

### Approach 3: Interval Merging (Optimal)
**Strategy**: Merge overlapping ranges first, then check each ID against merged ranges.

**Steps**:
1. Parse fresh ID ranges
2. Sort ranges by start position
3. Merge overlapping/adjacent ranges:
   - If current range overlaps or touches previous, merge them
   - Otherwise, add as separate range
4. For each available ID, binary search or iterate through merged ranges
5. Count matches

**Time Complexity**: O(R log R + N × log R) for sorting and binary search, or O(R log R + N × R') where R' is number of merged ranges
**Space Complexity**: O(R) for ranges

**Pros**:
- Reduces redundant range checks
- Efficient for many overlapping ranges
- Can use binary search for faster lookups
- Works with large range values

**Cons**:
- More complex implementation
- Sorting overhead
- May be overkill for small inputs

**Best for**: Many overlapping ranges or when both N and R are large

## Recommended Approach

**Start with Approach 2 (Range Checking)** for initial implementation:
- Simple and correct
- Works for all input sizes
- Easy to debug

**Optimize to Approach 3 (Interval Merging)** if performance is needed:
- Particularly if there are many overlapping ranges
- Provides better worst-case performance

**Avoid Approach 1** unless confirmed that range sizes are small (test with sample data first).

## Data Structures

### Core Data Structures

1. **Ranges**: `List[Tuple[int, int]]`
   - Store as list of (start, end) tuples
   - Simple and memory efficient

2. **Available IDs**: `List[int]`
   - Read and process sequentially
   - No need for special structure

3. **Fresh ID Set** (if using Approach 1): `Set[int]`
   - Fast O(1) membership testing
   - Use only if range expansion is feasible

### Utility Structures

- **Merged Ranges** (for Approach 3): `List[Tuple[int, int]]`
  - Sorted list of non-overlapping ranges
  - Enables binary search

## Test Plan

### Example Test Cases (from puzzle)

```python
# Example from puzzle
ranges = [(3, 5), (10, 14), (16, 20), (12, 18)]
available = [1, 5, 8, 11, 17, 32]
expected_fresh_count = 3
expected_fresh_ids = [5, 11, 17]
```

### Edge Cases

1. **Single ID Range**
   ```
   5-5
   
   5
   10
   ```
   Expected: 1 fresh (ID 5)

2. **Empty Available List**
   ```
   1-10
   
   ```
   Expected: 0 fresh

3. **No Ranges**
   ```
   
   1
   5
   10
   ```
   Expected: 0 fresh (all spoiled)

4. **All Available IDs Fresh**
   ```
   1-100
   
   5
   10
   50
   99
   ```
   Expected: 4 fresh

5. **All Available IDs Spoiled**
   ```
   10-20
   
   1
   5
   25
   30
   ```
   Expected: 0 fresh

6. **Boundary Testing**
   ```
   5-10
   
   4
   5
   10
   11
   ```
   Expected: 2 fresh (IDs 5 and 10, boundaries are inclusive)

7. **Completely Overlapping Ranges**
   ```
   5-20
   10-15
   
   7
   12
   18
   ```
   Expected: 3 fresh (all in outer range)

8. **Adjacent Non-Overlapping Ranges**
   ```
   1-5
   6-10
   
   5
   6
   ```
   Expected: 2 fresh (both at boundaries)

9. **Gap Between Ranges**
   ```
   1-5
   10-15
   
   7
   12
   ```
   Expected: 1 fresh (only 12)

10. **Large Range Values**
    ```
    1000000-1000010
    
    999999
    1000000
    1000005
    1000010
    1000011
    ```
    Expected: 3 fresh (1000000, 1000005, 1000010)

11. **Many Overlapping Ranges**
    ```
    1-10
    5-15
    10-20
    15-25
    
    1
    7
    13
    18
    30
    ```
    Expected: 4 fresh (1, 7, 13, 18)

### Unit Test Functions

Test the following functions independently:

1. **`parse_input(text: str) -> Tuple[List[Tuple[int, int]], List[int]]`**
   - Test parsing ranges correctly
   - Test parsing available IDs correctly
   - Test handling blank line separator
   - Test edge cases (empty sections, single line, etc.)

2. **`is_fresh(id: int, ranges: List[Tuple[int, int]]) -> bool`**
   - Test ID within single range
   - Test ID in overlapping ranges
   - Test ID outside all ranges
   - Test boundary values

3. **`count_fresh_ingredients(ranges: List[Tuple[int, int]], available: List[int]) -> int`**
   - Test with example input
   - Test with all edge cases above

4. **`merge_ranges(ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]`** (if implementing Approach 3)
   - Test merging overlapping ranges
   - Test merging adjacent ranges
   - Test non-overlapping ranges remain separate
   - Test sorting is correct

## Implementation Guidance

### Parsing Strategy

```python
def parse_input(text: str):
    sections = text.strip().split('\n\n')
    
    # Parse ranges
    range_lines = sections[0].strip().split('\n')
    ranges = []
    for line in range_lines:
        start, end = map(int, line.split('-'))
        ranges.append((start, end))
    
    # Parse available IDs
    id_lines = sections[1].strip().split('\n')
    available_ids = [int(line) for line in id_lines]
    
    return ranges, available_ids
```

### Core Logic (Approach 2 - Recommended)

```python
def is_fresh(ingredient_id: int, ranges: List[Tuple[int, int]]) -> bool:
    for start, end in ranges:
        if start <= ingredient_id <= end:
            return True
    return False

def count_fresh_ingredients(ranges: List[Tuple[int, int]], available: List[int]) -> int:
    count = 0
    for ingredient_id in available:
        if is_fresh(ingredient_id, ranges):
            count += 1
    return count
```

### Gotchas and Common Mistakes

1. **Inclusive Ranges**: Both START and END are included in the range. Don't use `start < id < end`.

2. **Overlapping Ranges**: An ID can fall into multiple ranges, but should only be counted once. Using Approach 2 naturally handles this since we check "is fresh" once per ID.

3. **Blank Line Separator**: Input has exactly one blank line between sections. Use `split('\n\n')` to separate sections.

4. **Range Format**: Ranges use hyphen `-` as separator, not other dash characters. Use `split('-')`.

5. **Empty Lines**: Watch for trailing newlines or empty lines in input. Use `strip()` appropriately.

6. **Integer Parsing**: All values are integers. Use `int()` for parsing.

7. **Order Independence**: Neither ranges nor available IDs are guaranteed to be sorted. Don't assume ordering.

8. **Performance**: If using set expansion (Approach 1), be aware that a range like `1-10000000` will consume significant memory. Check range sizes first.

## Part 2: Total Fresh Ingredient Count

### Problem Description

Instead of checking which *available* ingredients are fresh, Part 2 asks: **How many ingredient IDs in total are considered fresh according to all the fresh ingredient ID ranges?**

The key changes:
- The available ingredient IDs section (second section) is now **irrelevant**
- We need to count **all unique IDs** covered by the fresh ID ranges
- Overlapping ranges must be handled carefully to avoid double-counting

### Example Analysis

Using the same ranges from Part 1:
```
3-5
10-14
16-20
12-18
```

**All fresh IDs across all ranges**:
- Range `3-5`: IDs 3, 4, 5 (3 IDs)
- Range `10-14`: IDs 10, 11, 12, 13, 14 (5 IDs)
- Range `16-20`: IDs 16, 17, 18, 19, 20 (5 IDs)
- Range `12-18`: IDs 12, 13, 14, 15, 16, 17, 18 (7 IDs)

**Naive count**: 3 + 5 + 5 + 7 = 20 IDs ❌ (WRONG - double counts overlaps)

**Correct unique IDs**: 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20

**Answer**: **14 unique fresh IDs** ✓

### Why Overlaps Matter

Notice that ranges `10-14`, `16-20`, and `12-18` have overlaps:
- IDs 12, 13, 14 appear in both `10-14` and `12-18`
- IDs 16, 17, 18 appear in both `16-20` and `12-18`

If we merge `10-14` and `12-18`, we get `10-18` (9 IDs: 10, 11, 12, 13, 14, 15, 16, 17, 18).
Then add the non-overlapping part of `16-20`, which is `19-20` (2 IDs: 19, 20).
Plus `3-5` (3 IDs).
Total: 9 + 2 + 3 = 14 ✓

### Algorithm Analysis for Part 2

#### Approach 1: Set Expansion (Simple but Memory-Intensive)

**Strategy**: Expand all ranges into a set, which automatically handles duplicates.

**Steps**:
1. Parse fresh ID ranges
2. Create an empty set
3. For each range (start, end):
   - Add all IDs from start to end (inclusive) to the set
4. Return the size of the set

**Implementation**:
```python
def count_total_fresh_ids_set(ranges: List[Tuple[int, int]]) -> int:
    fresh_ids = set()
    for start, end in ranges:
        for id in range(start, end + 1):
            fresh_ids.add(id)
    return len(fresh_ids)
```

**Time Complexity**: O(T) where T is the total number of IDs across all ranges
- Worst case: sum of all range sizes
- Example: ranges 1-1000, 500-1500 = 1000 + 1001 = 2001 operations

**Space Complexity**: O(U) where U is the number of unique IDs
- Set stores only unique IDs
- Example: ranges 1-1000, 500-1500 = 1500 unique IDs stored

**Pros**:
- Very simple to implement
- Automatically handles all overlaps
- Easy to understand and debug
- Works well for small to medium range sizes

**Cons**:
- Memory intensive for large ranges
- Slow for large ranges (expanding 1-1000000 means 1 million operations)
- Time proportional to sum of range sizes, not number of ranges
- Not scalable for very large range values

**Best for**: 
- Total IDs < 1,000,000
- Quick implementation for Part 2
- When simplicity is preferred over optimization

#### Approach 2: Interval Merging (Optimal)

**Strategy**: Merge overlapping ranges into non-overlapping intervals, then sum their sizes.

**Steps**:
1. Sort ranges by start position
2. Merge overlapping or adjacent ranges:
   - Initialize with first range
   - For each subsequent range:
     - If it overlaps with previous merged range, extend the merged range
     - Otherwise, finalize previous range and start new one
3. Calculate the size of each merged range: (end - start + 1)
4. Return sum of all merged range sizes

**Implementation**:
```python
def merge_ranges(ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    if not ranges:
        return []
    
    # Sort by start position
    sorted_ranges = sorted(ranges)
    merged = [sorted_ranges[0]]
    
    for start, end in sorted_ranges[1:]:
        last_start, last_end = merged[-1]
        
        # Check if current range overlaps or touches previous
        if start <= last_end + 1:  # +1 for adjacent ranges
            # Merge by extending the end
            merged[-1] = (last_start, max(last_end, end))
        else:
            # Non-overlapping, add as separate range
            merged.append((start, end))
    
    return merged

def count_total_fresh_ids_merged(ranges: List[Tuple[int, int]]) -> int:
    merged = merge_ranges(ranges)
    total = 0
    for start, end in merged:
        total += (end - start + 1)
    return total
```

**Time Complexity**: O(R log R) where R is the number of ranges
- Sorting: O(R log R)
- Merging: O(R) single pass
- Counting: O(R') where R' ≤ R (number of merged ranges)
- Total: O(R log R)

**Space Complexity**: O(R) for storing merged ranges
- At most R ranges in merged list
- Usually fewer after merging

**Merging Logic Details**:

Consider ranges sorted by start:
- Range A: `[10, 14]`
- Range B: `[12, 18]`

Range B starts at 12, which is ≤ 14 (end of A), so they overlap.
Merged range: `[10, max(14, 18)]` = `[10, 18]`

Adjacent ranges example:
- Range A: `[10, 14]`
- Range B: `[15, 20]`

Range B starts at 15, which is 14+1, so they are adjacent (can be merged).
Merged range: `[10, 20]`

Non-overlapping example:
- Range A: `[10, 14]`
- Range B: `[20, 25]`

Range B starts at 20, which is > 14+1, so there's a gap. Keep as separate ranges.

**Pros**:
- Optimal time complexity
- Memory efficient
- Scalable to very large range values
- Handles all overlaps correctly
- Works for any input size

**Cons**:
- More complex to implement
- Requires careful handling of overlap/adjacency logic
- Need to handle edge cases (empty input, single range)

**Best for**:
- Production/optimal solution
- Large range values (e.g., 1-1000000)
- Many overlapping ranges
- When performance matters

#### Approach 3: Counting with Inclusion-Exclusion (Advanced)

**Strategy**: Use the mathematical principle of inclusion-exclusion for overlapping sets.

**Note**: This is theoretically interesting but impractical for this problem:
- Complexity grows exponentially with number of overlapping ranges
- Only mentioned for completeness
- **Not recommended** for implementation

### Recommended Approach for Part 2

**For initial implementation**: Use **Approach 1 (Set Expansion)** if you want to get Part 2 working quickly:
- Fast to code (5 lines)
- Handles all edge cases automatically
- Sufficient for most AoC inputs

**For optimal solution**: Use **Approach 2 (Interval Merging)**:
- Better time complexity
- Much better space complexity
- Scalable to any input size
- Industry-standard approach for interval problems

**Decision criteria**:
1. Check the actual input ranges:
   - If total IDs < 100,000: Either approach works fine
   - If total IDs > 1,000,000: Use interval merging
2. For learning: Implement both and compare performance
3. For speed: Start with set expansion, optimize later if needed

### Part 2 Test Cases

#### Example from Puzzle
```python
ranges = [(3, 5), (10, 14), (16, 20), (12, 18)]
expected_total_fresh = 14
# Fresh IDs: 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20
```

#### Edge Cases for Part 2

1. **Single Range**
   ```
   5-10
   ```
   Expected: 6 IDs (5, 6, 7, 8, 9, 10)

2. **Non-Overlapping Ranges**
   ```
   1-3
   10-12
   20-22
   ```
   Expected: 9 IDs (3 + 3 + 3)

3. **Completely Overlapping Ranges**
   ```
   5-20
   10-15
   12-18
   ```
   Expected: 16 IDs (all within 5-20)
   Merged: [(5, 20)] → 20 - 5 + 1 = 16

4. **Adjacent Ranges**
   ```
   1-5
   6-10
   11-15
   ```
   Expected: 15 IDs
   Merged: [(1, 15)] → 15 - 1 + 1 = 15

5. **Partially Overlapping Ranges**
   ```
   1-10
   5-15
   10-20
   ```
   Expected: 20 IDs (1 through 20)
   Merged: [(1, 20)] → 20 - 1 + 1 = 20

6. **Many Small Overlaps**
   ```
   1-5
   3-7
   5-9
   7-11
   ```
   Expected: 11 IDs (1 through 11)
   Merged: [(1, 11)] → 11 - 1 + 1 = 11

7. **Single ID Ranges**
   ```
   5-5
   10-10
   15-15
   ```
   Expected: 3 IDs

8. **Large Range Values**
   ```
   1000000-1000010
   1000005-1000015
   ```
   Expected: 16 IDs (1000000 through 1000015)
   Merged: [(1000000, 1000015)] → 16

9. **Empty Range List**
   ```
   (no ranges)
   ```
   Expected: 0 IDs

### Step-by-Step Trace for Example

**Input ranges**: `3-5`, `10-14`, `16-20`, `12-18`

**Approach 1 (Set Expansion)**:
1. Initialize empty set: `{}`
2. Process `3-5`: Add 3, 4, 5 → `{3, 4, 5}`
3. Process `10-14`: Add 10, 11, 12, 13, 14 → `{3, 4, 5, 10, 11, 12, 13, 14}`
4. Process `16-20`: Add 16, 17, 18, 19, 20 → `{3, 4, 5, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20}`
5. Process `12-18`: Add 12, 13, 14, 15, 16, 17, 18 (12-14, 16-18 already exist)
   → `{3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20}`
6. Count: 14 IDs ✓

**Approach 2 (Interval Merging)**:
1. Sort ranges by start: `[(3, 5), (10, 14), (12, 18), (16, 20)]`
2. Initialize merged: `[(3, 5)]`
3. Process `(10, 14)`:
   - Start 10 > 5+1, no overlap/adjacency
   - Add as separate: `[(3, 5), (10, 14)]`
4. Process `(12, 18)`:
   - Start 12 ≤ 14+1, overlaps with (10, 14)
   - Merge: `[(3, 5), (10, 18)]`
5. Process `(16, 20)`:
   - Start 16 ≤ 18+1, overlaps with (10, 18)
   - Merge: `[(3, 5), (10, 20)]`
6. Calculate sizes:
   - `(3, 5)`: 5 - 3 + 1 = 3 IDs
   - `(10, 20)`: 20 - 10 + 1 = 11 IDs
7. Total: 3 + 11 = 14 IDs ✓

### Implementation Guidance for Part 2

#### Key Differences from Part 1

1. **No Available IDs**: Don't parse or use the second section
2. **Count All IDs**: Count every ID in the ranges, not just specific ones
3. **Handle Overlaps**: Must properly handle overlapping ranges to avoid double-counting

#### Function Structure

```python
def solve_part2(text: str) -> int:
    # Only parse the ranges section
    sections = text.strip().split('\n\n')
    range_lines = sections[0].strip().split('\n')
    ranges = []
    for line in range_lines:
        start, end = map(int, line.split('-'))
        ranges.append((start, end))
    
    # Option 1: Set expansion (simple)
    return count_total_fresh_ids_set(ranges)
    
    # Option 2: Interval merging (optimal)
    return count_total_fresh_ids_merged(ranges)
```

#### Common Mistakes to Avoid

1. **Forgetting Inclusive Ranges**: Range `5-10` includes both 5 and 10
   - Correct size: `end - start + 1`
   - Wrong: `end - start`

2. **Not Handling Overlaps**: Simply summing all range sizes gives wrong answer
   - Example: `1-10` and `5-15` → wrong: 10 + 11 = 21, correct: 15

3. **Off-by-One in Adjacency**: Ranges `1-5` and `6-10` should merge to `1-10`
   - Check: `start <= last_end + 1`
   - Not: `start <= last_end` (misses adjacent ranges)

4. **Not Sorting Ranges**: Merge algorithm requires sorted input
   - Must sort by start position before merging

5. **Extending Wrong Range End**: When merging, take the maximum end
   - Correct: `max(last_end, end)`
   - Example: `(1, 10)` and `(5, 8)` → `(1, 10)`, not `(1, 8)`

#### Testing Strategy

1. **Start with Set Expansion**: Get correct answer first
2. **Implement Interval Merging**: Optimize for performance
3. **Compare Results**: Both should give same answer
4. **Verify Merge Logic**: Print merged ranges to debug
5. **Test Edge Cases**: Empty, single range, no overlaps, all overlapping

### Unit Test Functions for Part 2

```python
def test_merge_ranges():
    # Non-overlapping
    assert merge_ranges([(1, 5), (10, 15)]) == [(1, 5), (10, 15)]
    
    # Overlapping
    assert merge_ranges([(1, 10), (5, 15)]) == [(1, 15)]
    
    # Adjacent
    assert merge_ranges([(1, 5), (6, 10)]) == [(1, 10)]
    
    # Multiple overlaps
    assert merge_ranges([(1, 5), (3, 7), (6, 10)]) == [(1, 10)]
    
    # Unsorted input
    assert merge_ranges([(10, 15), (1, 5), (3, 8)]) == [(1, 15)]
    
    # Single range
    assert merge_ranges([(5, 10)]) == [(5, 10)]
    
    # Empty
    assert merge_ranges([]) == []

def test_count_total_fresh_ids():
    # Example from puzzle
    ranges = [(3, 5), (10, 14), (16, 20), (12, 18)]
    assert count_total_fresh_ids(ranges) == 14
    
    # Single range
    assert count_total_fresh_ids([(5, 10)]) == 6
    
    # Non-overlapping
    assert count_total_fresh_ids([(1, 3), (10, 12), (20, 22)]) == 9
    
    # Completely overlapping
    assert count_total_fresh_ids([(5, 20), (10, 15)]) == 16
    
    # Adjacent
    assert count_total_fresh_ids([(1, 5), (6, 10)]) == 10
```

### Complexity Analysis Summary for Part 2

| Approach | Time | Space | Notes |
|----------|------|-------|-------|
| Set Expansion | O(T) | O(U) | T = total IDs, U = unique IDs |
| Interval Merging | O(R log R) | O(R) | R = number of ranges |

**When T >> R**: Interval merging is much faster
**When T ≈ R**: Both approaches comparable
**When T < 1M**: Set expansion is fine

**Example comparison**:
- Input: 100 ranges, each size ~10,000
- Set expansion: ~1,000,000 operations
- Interval merging: ~664 operations (100 * log2(100) + 100)

## Complexity Summary

| Approach | Time | Space | Best Use Case |
|----------|------|-------|---------------|
| Set Expansion | O(R×M + N) | O(T) | Small ranges |
| Range Checking | O(N×R) | O(R) | General purpose |
| Interval Merging | O(R log R + N×log R) | O(R) | Many overlaps |

Where:
- R = number of ranges
- M = average range size
- N = number of available IDs
- T = total unique fresh IDs

## Implementation Checklist

### Part 1
- [ ] Parse input into ranges and available IDs
- [ ] Handle blank line separator correctly
- [ ] Implement range checking function
- [ ] Implement fresh ingredient counter
- [ ] Test with example input (expected: 3)
- [ ] Test boundary conditions (inclusive ranges)
- [ ] Test overlapping ranges
- [ ] Test spoiled IDs (outside all ranges)
- [ ] Handle edge cases (empty lists, single items)
- [ ] Verify performance with actual input

### Part 2
- [ ] Implement set expansion approach OR interval merging
- [ ] Handle overlapping ranges correctly (no double-counting)
- [ ] Test with example input (expected: 14)
- [ ] Verify inclusive range counting (end - start + 1)
- [ ] Test merge algorithm (if using interval merging):
  - [ ] Overlapping ranges merge correctly
  - [ ] Adjacent ranges merge correctly
  - [ ] Non-overlapping ranges stay separate
  - [ ] Sorting works for unsorted input
- [ ] Test edge cases:
  - [ ] Single range
  - [ ] No overlaps
  - [ ] All overlapping
  - [ ] Adjacent ranges
  - [ ] Empty range list
- [ ] Compare both approaches (if implemented both) for correctness
- [ ] Verify performance with actual input
