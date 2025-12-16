#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 11: Reactor

Graph traversal problem: Count all distinct paths from 'you' to 'out' in a directed graph.
Uses DFS with backtracking to enumerate all possible paths.
"""

import sys
from pathlib import Path


def parse_input(input_text: str):
    """
    Parse the input text into an adjacency list representation of the directed graph.
    
    Input format: "device: output1 output2 output3 ..."
    Returns: dict mapping device name to list of output devices
    
    Example:
        "you: bbb ccc" -> {'you': ['bbb', 'ccc']}
    
    All nodes (including terminal nodes) will have entries in the graph,
    even if they have no outgoing edges (empty list).
    """
    graph = {}
    lines = input_text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Split on colon to separate device from outputs
        parts = line.split(':', 1)
        if len(parts) != 2:
            continue
            
        device = parts[0].strip()
        outputs_str = parts[1].strip()
        
        # Parse outputs (space-separated)
        if outputs_str:
            outputs = outputs_str.split()
        else:
            outputs = []
        
        # Add the device with its outputs
        graph[device] = outputs
        
        # Ensure all output nodes also have entries (even if empty)
        # This ensures terminal nodes like 'out' are in the graph
        for output in outputs:
            if output not in graph:
                graph[output] = []
    
    return graph


def count_paths_dfs(graph, current, target, visited):
    """
    Recursive DFS to count all paths from current node to target.
    
    Args:
        graph: adjacency list (dict)
        current: current node we're visiting
        target: destination node ('out')
        visited: set of nodes in current path (for cycle detection)
    
    Returns:
        Number of distinct paths from current to target
    """
    # Base case: reached the target
    if current == target:
        return 1
    
    # Cycle detection: if we've visited this node in current path, stop
    if current in visited:
        return 0
    
    # Mark current node as visited in this path
    visited.add(current)
    
    # Count paths through all neighbors
    total_paths = 0
    neighbors = graph.get(current, [])
    
    for neighbor in neighbors:
        total_paths += count_paths_dfs(graph, neighbor, target, visited)
    
    # Backtrack: remove current node from visited set
    # This allows other paths to visit this node
    visited.remove(current)
    
    return total_paths


def solve_part1(graph) -> int:
    """
    Solve part 1: Count all distinct paths from 'you' to 'out'.
    
    Uses DFS with backtracking to enumerate all possible paths.
    Handles cycles by tracking visited nodes in current path.
    
    Args:
        graph: adjacency list (dict) from parse_input
    
    Returns:
        Number of distinct paths from 'you' to 'out'
    """
    start = 'you'
    end = 'out'
    
    # Initialize empty visited set for path tracking
    visited = set()
    
    # Start DFS from 'you', count paths to 'out'
    return count_paths_dfs(graph, start, end, visited)


def count_paths_with_required_nodes_memo(graph, current, target, visited, required_nodes, seen_required, memo):
    """
    Recursive DFS with memoization to count all paths from current node to target 
    that visit all required nodes.
    
    Args:
        graph: adjacency list (dict)
        current: current node we're visiting
        target: destination node ('out')
        visited: set of nodes in current path (for cycle detection)
        required_nodes: frozenset of nodes that must be visited in the path
        seen_required: frozenset of required nodes seen so far in current path
        memo: dict mapping (node, seen_required_state) to path count
    
    Returns:
        Number of distinct paths from current to target that visit all required nodes
    """
    # Base case: reached the target
    if current == target:
        # Check if all required nodes have been seen in this path
        if seen_required == required_nodes:
            return 1
        else:
            return 0
    
    # Cycle detection: if we've visited this node in current path, stop
    if current in visited:
        return 0
    
    # Check memo - key is (current node, which required nodes we've seen)
    memo_key = (current, seen_required)
    if memo_key in memo:
        return memo[memo_key]
    
    # Mark current node as visited in this path
    visited.add(current)
    
    # Update seen_required if current is a required node
    new_seen_required = seen_required
    if current in required_nodes:
        new_seen_required = seen_required | {current}
    
    # Count paths through all neighbors
    total_paths = 0
    neighbors = graph.get(current, [])
    
    for neighbor in neighbors:
        total_paths += count_paths_with_required_nodes_memo(graph, neighbor, target, visited, required_nodes, new_seen_required, memo)
    
    # Backtrack: remove current node from visited set
    visited.remove(current)
    
    # Memoize the result
    memo[memo_key] = total_paths
    
    return total_paths


def solve_part2(graph) -> int:
    """
    Solve part 2: Count all distinct paths from 'svr' to 'out' that visit BOTH 'dac' and 'fft'.
    
    The paths can visit 'dac' and 'fft' in any order, but both must be visited.
    
    Args:
        graph: adjacency list (dict) from parse_input
    
    Returns:
        Number of distinct paths from 'svr' to 'out' that visit both required nodes
    """
    start = 'svr'
    end = 'out'
    required_nodes = frozenset({'dac', 'fft'})
    
    # Initialize empty visited set for path tracking
    visited = set()
    seen_required = frozenset()
    memo = {}
    
    # Start DFS from 'svr', count paths to 'out' that visit both 'dac' and 'fft'
    return count_paths_with_required_nodes_memo(graph, start, end, visited, required_nodes, seen_required, memo)


def main():
    """Run the solution."""
    input_file = Path(__file__).parent / 'input.txt'
    
    if not input_file.exists():
        print(f"Error: {input_file} not found")
        return
    
    input_text = input_file.read_text()
    graph = parse_input(input_text)

    result1 = solve_part1(graph)
    print(f"Part 1: {result1}")

    result2 = solve_part2(graph)
    print(f"Part 2: {result2}")


def test():
    """
    Run tests based on spec test cases.
    """
    # === Part 1 Tests ===
    print("Part 1 Tests:")

    # Main example from spec
    example = """aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out"""
    
    graph = parse_input(example)
    result = solve_part1(graph)
    assert result == 5, f"Expected 5 paths, got {result}"
    print("  ✓ Main example (5 paths)")

    # Simple test: direct connection
    simple = "you: out"
    graph = parse_input(simple)
    assert solve_part1(graph) == 1
    print("  ✓ Direct connection (1 path)")

    # Two independent paths
    two_paths = """you: a b
a: out
b: out"""
    graph = parse_input(two_paths)
    assert solve_part1(graph) == 2
    print("  ✓ Two independent paths (2 paths)")

    print("\n✅ All manual tests passed!")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test()
    else:
        main()
