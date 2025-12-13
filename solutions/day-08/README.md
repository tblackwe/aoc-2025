# Day 08 Solution

This solution is generated based on the specification in `specs/day-08.md`.

## Problem Summary

Connect junction boxes in 3D space by creating circuits. Connect the 1000 closest pairs of junction boxes and calculate the product of the three largest resulting circuit sizes.

## Algorithm

- **Union-Find (Disjoint Set Union)** for tracking circuits
- **Greedy connection strategy** (similar to Kruskal's MST algorithm)
- **3D Euclidean distance** calculation
- Time complexity: O(n² log n) for sorting all pairs
- Space complexity: O(n²) for storing all pairs

## Running the Solution

```bash
python3 solution.py
```

## Running Tests

```bash
python3 -m unittest test_solution.py
```

Or use the built-in test function:

```bash
python3 solution.py test
```

## Input

Place your puzzle input in `input.txt` (not committed to git).

## Notes

### Key Implementation Details

1. **Parse 3D coordinates** from comma-separated values
2. **Calculate all pairwise distances** between junction boxes
3. **Sort pairs** by distance (ascending)
4. **Use Union-Find** to track which boxes are in same circuit
5. **Connect 1000 pairs** (skip if already in same circuit)
6. **Count circuit sizes** by grouping boxes by their root
7. **Find product** of three largest circuit sizes

### Union-Find Optimizations

- Path compression in `find()` operation
- Union by size (attach smaller tree to larger)
- These optimizations give nearly O(1) amortized time per operation
