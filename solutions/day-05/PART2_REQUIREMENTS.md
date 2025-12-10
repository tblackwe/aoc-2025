# Day 5 Part 2: Implementation Requirements

## Overview
Part 2 tests have been successfully added to `test_solution.py`. These tests follow TDD principles and will guide the implementation of the Part 2 solution.

## Test Statistics
- **Total test methods in file**: 64
- **Part 2 test classes**: 3
- **Part 2 test methods**: 32
  - TestDay05Part2MergeRanges: 13 tests
  - TestDay05Part2CountTotalFresh: 16 tests
  - TestDay05Part2Integration: 3 tests

## Functions to Implement

### 1. `merge_ranges(ranges: List[Tuple[int, int]]) -> List[Tuple[int, int]]`

**Purpose**: Merge overlapping and adjacent ranges into non-overlapping intervals.

**Algorithm**:
1. Sort ranges by start position
2. Iterate through sorted ranges:
   - If current range overlaps or is adjacent to previous range (start <= last_end + 1):
     - Merge by extending the end: `merged[-1] = (last_start, max(last_end, end))`
   - Otherwise, add as separate range
3. Return merged list

**Test Coverage** (13 tests):
- Non-overlapping ranges remain separate
- Overlapping ranges merge correctly
- Adjacent ranges (touching boundaries) merge
- Multiple overlapping ranges merge into single range
- Completely contained ranges absorbed
- Unsorted input handled correctly
- Single range unchanged
- Empty list returns empty list
- Single-element ranges (X-X) merge when adjacent
- Three-way overlaps
- Multiple separate groups of overlapping ranges
- Identical/duplicate ranges merge
- Large value ranges

**Example**:
```python
merge_ranges([(10, 14), (12, 18), (16, 20), (3, 5)])
# Returns: [(3, 5), (10, 20)]
```

**Edge Cases to Handle**:
- Empty input: `[]` → `[]`
- Single range: `[(5, 10)]` → `[(5, 10)]`
- Adjacent ranges: `[(1, 5), (6, 10)]` → `[(1, 10)]`
- Check condition: `start <= last_end + 1` (the +1 handles adjacency)

---

### 2. `count_total_fresh_ids(ranges: List[Tuple[int, int]]) -> int`

**Purpose**: Count the total number of unique fresh IDs across all ranges (Part 2 solution).

**Algorithm Options**:

#### Option A: Set Expansion (Simple)
```python
def count_total_fresh_ids(ranges: List[Tuple[int, int]]) -> int:
    fresh_ids = set()
    for start, end in ranges:
        for id in range(start, end + 1):
            fresh_ids.add(id)
    return len(fresh_ids)
```
- **Pros**: Very simple, handles all overlaps automatically
- **Cons**: Memory intensive for large ranges
- **Use when**: Total IDs < 1,000,000

#### Option B: Interval Merging (Optimal - Recommended)
```python
def count_total_fresh_ids(ranges: List[Tuple[int, int]]) -> int:
    merged = merge_ranges(ranges)
    total = 0
    for start, end in merged:
        total += (end - start + 1)
    return total
```
- **Pros**: Optimal time/space complexity, scalable
- **Cons**: Slightly more complex
- **Use when**: Production/optimal solution needed

**Test Coverage** (16 tests):
- Example from spec: `[(3, 5), (10, 14), (16, 20), (12, 18)]` → 14
- Single range: `[(5, 10)]` → 6
- Non-overlapping ranges: sum correctly
- Completely overlapping: no double-counting
- Adjacent ranges: merge correctly
- Partially overlapping: handle correctly
- Many overlaps: merge all
- Large values: work correctly
- Empty list: return 0
- Complex mix of overlaps and gaps
- Single-element ranges
- Adjacent single elements
- Duplicate ranges: no double-counting
- One range contains many
- Boundary adjacency
- Heavy overlaps validation

**Critical Formula**:
```python
# Range size (INCLUSIVE on both ends)
size = end - start + 1

# Example: range 5-10
# IDs: 5, 6, 7, 8, 9, 10 = 6 IDs
# Formula: 10 - 5 + 1 = 6 ✓
```

---

## Test Cases from Specification

All 9 test cases from the spec are implemented:

1. **Single range**: `[(5, 10)]` → 6 IDs
2. **Non-overlapping**: `[(1, 3), (10, 12), (20, 22)]` → 9 IDs
3. **Completely overlapping**: `[(5, 20), (10, 15), (12, 18)]` → 16 IDs
4. **Adjacent**: `[(1, 5), (6, 10), (11, 15)]` → 15 IDs
5. **Partially overlapping**: `[(1, 10), (5, 15), (10, 20)]` → 20 IDs
6. **Many overlaps**: `[(1, 5), (3, 7), (5, 9), (7, 11)]` → 11 IDs
7. **Large values**: `[(1000000, 1000010), (1000005, 1000015)]` → 16 IDs
8. **Empty list**: `[]` → 0 IDs
9. **Complex mix**: `[(1, 5), (3, 7), (20, 25), (22, 30), (50, 55)]` → 24 IDs

## Key Part 2 Example (from spec)

**Input Ranges**:
```
3-5
10-14
16-20
12-18
```

**Step-by-Step Trace**:
1. Parse: `[(3, 5), (10, 14), (16, 20), (12, 18)]`
2. Sort: `[(3, 5), (10, 14), (12, 18), (16, 20)]`
3. Merge:
   - Start with `[(3, 5)]`
   - `(10, 14)`: doesn't overlap with `(3, 5)`, add separately → `[(3, 5), (10, 14)]`
   - `(12, 18)`: overlaps with `(10, 14)` (12 ≤ 14+1), merge → `[(3, 5), (10, 18)]`
   - `(16, 20)`: overlaps with `(10, 18)` (16 ≤ 18+1), merge → `[(3, 5), (10, 20)]`
4. Count:
   - `(3, 5)`: 5 - 3 + 1 = 3 IDs
   - `(10, 20)`: 20 - 10 + 1 = 11 IDs
   - Total: 3 + 11 = **14 IDs** ✓

**Fresh IDs**: 3, 4, 5, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20

---

## Common Mistakes to Avoid

1. **Off-by-one in range size**: Must use `end - start + 1`, not `end - start`
2. **Forgetting adjacency**: Check `start <= last_end + 1`, not `start <= last_end`
3. **Not sorting**: Merge algorithm requires sorted input
4. **Wrong merge end**: Use `max(last_end, end)` when merging
5. **Double-counting overlaps**: Don't sum individual range sizes

---

## Running the Tests

```bash
# Run all tests
python3 test_solution.py

# Run only Part 2 tests
python3 test_solution.py TestDay05Part2MergeRanges
python3 test_solution.py TestDay05Part2CountTotalFresh
python3 test_solution.py TestDay05Part2Integration

# Run with verbose output
python3 test_solution.py -v
```

**Expected Behavior** (TDD):
- ❌ All Part 2 tests SHOULD FAIL initially (functions don't exist)
- ✅ After implementing `merge_ranges` and `count_total_fresh_ids`, all tests should pass

---

## Implementation Checklist

### Phase 1: Implement `merge_ranges`
- [ ] Handle empty input
- [ ] Sort ranges by start position
- [ ] Implement merge logic with adjacency check (`start <= last_end + 1`)
- [ ] Use `max(last_end, end)` when merging
- [ ] Run `TestDay05Part2MergeRanges` tests
- [ ] All 13 merge tests should pass

### Phase 2: Implement `count_total_fresh_ids`
- [ ] Call `merge_ranges` to get non-overlapping ranges
- [ ] Calculate size for each range: `end - start + 1`
- [ ] Sum all range sizes
- [ ] Run `TestDay05Part2CountTotalFresh` tests
- [ ] All 16 count tests should pass

### Phase 3: Integration
- [ ] Update `main()` to call Part 2 solution
- [ ] Parse ranges from input (ignore available IDs section for Part 2)
- [ ] Run `TestDay05Part2Integration` tests
- [ ] All 3 integration tests should pass

### Phase 4: Verification
- [ ] Run all 64 tests: `python3 test_solution.py`
- [ ] Verify Part 1 still works (no regressions)
- [ ] Verify Part 2 produces correct answer for example (14)
- [ ] Test with actual puzzle input

---

## Complexity Analysis

| Approach | Time | Space | Best Use Case |
|----------|------|-------|---------------|
| Set Expansion | O(T) | O(U) | Small ranges (T < 1M) |
| Interval Merging | O(R log R) | O(R) | Production/optimal |

Where:
- T = total IDs across all ranges (sum of range sizes)
- U = unique IDs
- R = number of ranges

**Recommendation**: Use interval merging approach (Option B) for optimal solution.

---

## Next Steps

1. ✅ **Tests created** (this step is complete)
2. ⏭️ **Implement `merge_ranges` function** in `solution.py`
3. ⏭️ **Implement `count_total_fresh_ids` function** in `solution.py`
4. ⏭️ **Update `main()` to solve Part 2**
5. ⏭️ **Run all tests to verify correctness**
6. ⏭️ **Solve actual puzzle input**

---

## Test-Driven Development Verification

**Current Status**: ✅ Tests are ready and failing as expected

```bash
$ python3 test_solution.py
ImportError: cannot import name 'merge_ranges' from 'solution'
```

This is **correct TDD behavior** - tests fail because functions don't exist yet!

After implementation, all 64 tests should pass.
