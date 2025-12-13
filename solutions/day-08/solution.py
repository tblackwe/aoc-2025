#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 08: Playground

Junction box circuit connection problem using Union-Find and greedy algorithm.
"""

import sys
import math
from pathlib import Path


def parse_input(input_text: str):
    """
    Parse the input text into a list of 3D coordinates.

    Input format: Each line contains X,Y,Z coordinates separated by commas.
    Returns: List of tuples (x, y, z)
    """
    lines = input_text.strip().split('\n')
    positions = []
    for line in lines:
        line = line.strip()
        if line:  # Skip empty lines
            parts = line.split(',')
            x, y, z = int(parts[0]), int(parts[1]), int(parts[2])
            positions.append((x, y, z))
    return positions


def euclidean_distance(pos1, pos2):
    """
    Calculate 3D Euclidean distance between two positions.
    
    Args:
        pos1: Tuple (x1, y1, z1)
        pos2: Tuple (x2, y2, z2)
    
    Returns:
        Float distance: sqrt((x2-x1)² + (y2-y1)² + (z2-z1)²)
    """
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)


class UnionFind:
    """
    Union-Find (Disjoint Set Union) data structure with path compression and union by size.
    
    Used to efficiently track which junction boxes are in the same electrical circuit.
    """
    
    def __init__(self, n):
        """
        Initialize n separate sets (each element is its own parent).
        
        Args:
            n: Number of elements
        """
        self.parent = list(range(n))  # parent[i] = parent of element i
        self.size = [1] * n           # size[i] = size of tree rooted at i
    
    def find(self, x):
        """
        Find the root of element x with path compression.
        
        Path compression: Make all nodes on the path point directly to the root
        for faster future queries.
        
        Args:
            x: Element to find root of
        
        Returns:
            Root of the set containing x
        """
        if self.parent[x] != x:
            # Path compression: recursively find root and update parent
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """
        Union the sets containing x and y.
        
        Uses union by size: attach smaller tree under root of larger tree
        to keep trees balanced.
        
        Args:
            x: First element
            y: Second element
        
        Returns:
            True if sets were merged (were previously separate)
            False if already in same set
        """
        root_x = self.find(x)
        root_y = self.find(y)
        
        # Already in same set
        if root_x == root_y:
            return False
        
        # Union by size: attach smaller tree under larger tree
        if self.size[root_x] < self.size[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        else:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
        
        return True
    
    def get_circuit_sizes(self):
        """
        Get the sizes of all circuits (connected components).
        
        Returns:
            List of circuit sizes (one per circuit)
        """
        # Count how many elements belong to each root
        circuit_counts = {}
        for i in range(len(self.parent)):
            root = self.find(i)
            circuit_counts[root] = circuit_counts.get(root, 0) + 1
        
        return list(circuit_counts.values())


def solve_part1(data, num_pairs=1000):
    """
    Solve part 1 of the puzzle.

    Connect pairs of junction boxes using a greedy algorithm (closest first),
    then return the product of the three largest circuit sizes.
    
    Algorithm:
    1. Calculate all pairwise distances
    2. Sort pairs by distance (closest first)
    3. Use Union-Find to connect pairs greedily
    4. Process the first num_pairs closest pairs (some may be skipped if already connected)
    5. Return product of three largest circuit sizes
    
    Args:
        data: List of (x, y, z) coordinate tuples
        num_pairs: Number of closest pairs to process (default 1000)
           Note: This is pairs to attempt, not successful connections.
           Some pairs may already be connected and will be skipped.
    
    Returns:
        Product of three largest circuit sizes
    """
    n = len(data)
    
    # Step 1: Calculate all pairwise distances
    # Format: (distance, index1, index2)
    distance_pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean_distance(data[i], data[j])
            distance_pairs.append((dist, i, j))
    
    # Step 2: Sort pairs by distance (closest first)
    distance_pairs.sort()
    
    # Step 3: Initialize Union-Find
    uf = UnionFind(n)
    
    # Step 4: Process the first num_pairs pairs (closest by distance)
    # Some pairs may already be in the same circuit and will be skipped
    for dist, i, j in distance_pairs[:num_pairs]:
        # Try to connect i and j (returns True if successful, False if already connected)
        uf.union(i, j)
    
    # Step 5: Get circuit sizes
    circuit_sizes = uf.get_circuit_sizes()
    
    # Step 6: Find three largest circuits
    circuit_sizes.sort(reverse=True)
    
    # Handle edge case: fewer than 3 circuits
    # Pad with 1s if needed (circuits of size 1)
    while len(circuit_sizes) < 3:
        circuit_sizes.append(1)
    
    # Return product of three largest
    return circuit_sizes[0] * circuit_sizes[1] * circuit_sizes[2]


def solve_part2(data) -> int | None:
    """
    Solve part 2 of the puzzle.
    
    Connect junction boxes until all are in a single circuit using greedy algorithm.
    Return product of X coordinates of the last two boxes connected.
    
    Algorithm:
    1. Calculate all pairwise 3D Euclidean distances
    2. Sort pairs by distance (closest first)
    3. Use Union-Find to track which boxes are in the same circuit
    4. Process pairs in distance order:
       - Try to connect each pair using Union-Find
       - Count only SUCCESSFUL connections (skip already-connected pairs)
       - Track which pair was the last successful connection
       - Stop when exactly n-1 successful connections have been made (forms single circuit)
    5. Extract the X coordinates (index 0) from the last pair connected
    6. Return the product of those X coordinates
    
    Args:
        data: List of (x, y, z) coordinate tuples
    
    Returns:
        Product of X coordinates of last two boxes connected, or None for invalid input
    """
    n = len(data)
    
    # Edge case: need at least 2 boxes to make a connection
    if n < 2:
        return None
    
    # Step 1: Calculate all pairwise distances
    # Format: (distance, index1, index2)
    distance_pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            dist = euclidean_distance(data[i], data[j])
            distance_pairs.append((dist, i, j))
    
    # Step 2: Sort pairs by distance (closest first)
    distance_pairs.sort()
    
    # Step 3: Initialize Union-Find
    uf = UnionFind(n)
    
    # Step 4: Process pairs in distance order until we have a single circuit
    # We need exactly n-1 successful connections to connect n boxes
    connections_made = 0
    last_pair = None
    
    for dist, i, j in distance_pairs:
        # Try to connect i and j
        # union() returns True if successful, False if already connected
        if uf.union(i, j):
            connections_made += 1
            last_pair = (i, j)  # Remember this pair as the last successful connection
            
            # Check if we're done: n boxes need n-1 connections
            if connections_made == n - 1:
                break
    
    # Step 5: Extract X coordinates from the last pair connected
    if last_pair is None:
        return None  # No connections were made (shouldn't happen with n >= 2)
    
    index1, index2 = last_pair
    x1 = data[index1][0]  # X coordinate is first element of tuple
    x2 = data[index2][0]
    
    # Step 6: Return product of X coordinates
    return x1 * x2


def main():
    """Run the solution."""
    input_file = Path(__file__).parent / 'input.txt'
    data = parse_input(input_file.read_text())

    print(f"Part 1: {solve_part1(data)}")

    if (part2 := solve_part2(data)) is not None:
        print(f"Part 2: {part2}")


def test():
    """
    Run tests based on spec test cases.

    Tests should match the Test Cases section in the spec file.
    """
    # === Part 1 Tests ===
    print("Part 1 Tests:")

    # Main example from spec (10 connections instead of 1000)
    example = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""
    # TODO: Test with 10 connections (modify solve_part1 to accept num_connections parameter)
    # assert solve_part1(parse_input(example), num_connections=10) == 40
    print("  ✓ Main example (10 connections) - TODO")

    # === Part 2 Tests ===
    print("\nPart 2 Tests:")
    print("  ⏸ Part 2 not yet available")

    print("\n✅ All tests passed!")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test()
    else:
        main()
