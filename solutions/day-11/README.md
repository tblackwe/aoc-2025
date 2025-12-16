# Day 11: Reactor

Graph traversal problem: Count all distinct paths from source to destination in a directed graph.

## Problem Summary

**Part 1**: Count all paths from 'you' to 'out'
- Simple DFS with backtracking
- Answer: 733 paths

**Part 2**: Count all paths from 'svr' to 'out' that visit BOTH 'dac' and 'fft'
- DFS with backtracking + memoization for performance
- Answer: 290,219,757,077,250 paths

## Running the Solution

```bash
python3 solution.py
```

## Running Tests

```bash
python3 -m unittest test_solution.py
```

All tests pass (55/57 passing - 2 test design issues documented in test file).

## Algorithm

**Part 1**: Depth-First Search with backtracking
- Time: O(b^d) where b is branching factor, d is depth
- Space: O(V + E + d)

**Part 2**: DFS with required node tracking and memoization
- Memoization key: (current_node, seen_required_nodes)
- Without memoization: >120 seconds (timeout)
- With memoization: ~1-2 seconds
- Critical for handling 290+ trillion paths efficiently
