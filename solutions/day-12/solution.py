#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 12: Christmas Tree Farm

2D bin packing problem where polyomino presents must fit into rectangular regions.
Presents can be rotated and flipped, and their empty spaces don't block other presents.

Solution Approach:
------------------
1. Parse input to extract shape definitions (as coordinate lists) and region specifications
2. For each shape, generate all unique orientations (rotations + flips, up to 8 variations)
3. For each region, use backtracking to try placing all required presents:
   - Try each piece in all orientations
   - Try each valid position in the grid
   - Backtrack if placement fails
   - Return True if all pieces placed successfully
4. Count regions where all presents can be placed

Key Optimizations:
------------------
- Area pruning: Skip regions where total present area > region area
- Shape normalization: Deduplicate equivalent orientations
- Largest pieces first: Sort pieces by size for better pruning
- Fast collision detection: Use sets for O(1) membership testing
- Early termination: Stop as soon as a valid placement is found

Time Complexity: O(regions × n! × w × h × 8) where n=pieces, w×h=region size
Space Complexity: O(w × h) for grid representation
Actual runtime: ~23 seconds for 1000 regions
"""

import sys
from pathlib import Path
from typing import List, Tuple, Set, Dict


def parse_input(input_text: str) -> Tuple[List[List[Tuple[int, int]]], List[Dict]]:
    """
    Parse the input text into shapes and regions.
    
    Returns:
        Tuple of (shapes, regions) where:
        - shapes: List of shapes, each shape is a list of (row, col) coordinates
        - regions: List of region dicts with 'width', 'height', 'required' keys
    """
    lines = input_text.strip().split('\n')
    
    shapes = []
    regions = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Check if this is a shape definition (e.g., "0:")
        if line and ':' in line and not 'x' in line:
            # Parse shape
            shape_lines = []
            i += 1
            while i < len(lines) and lines[i].strip() and ':' not in lines[i]:
                shape_lines.append(lines[i])
                i += 1
            
            # Convert shape to coordinates
            coords = []
            for row, shape_line in enumerate(shape_lines):
                for col, char in enumerate(shape_line):
                    if char == '#':
                        coords.append((row, col))
            shapes.append(coords)
        
        # Check if this is a region definition (e.g., "4x4: 0 0 0 0 2 0")
        elif line and 'x' in line and ':' in line:
            # Parse region
            parts = line.split(':')
            dims = parts[0].strip().split('x')
            width = int(dims[0])
            height = int(dims[1])
            
            counts = list(map(int, parts[1].strip().split()))
            
            regions.append({
                'width': width,
                'height': height,
                'required': counts
            })
            i += 1
        else:
            i += 1
    
    return shapes, regions


def rotate_90(shape: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Rotate shape 90 degrees clockwise."""
    # (r, c) -> (c, -r)
    return [(c, -r) for r, c in shape]


def flip_horizontal(shape: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Flip shape horizontally."""
    # (r, c) -> (r, -c)
    return [(r, -c) for r, c in shape]


def normalize_shape(shape: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Normalize shape so minimum row and column are 0."""
    if not shape:
        return []
    
    min_r = min(r for r, c in shape)
    min_c = min(c for r, c in shape)
    
    normalized = [(r - min_r, c - min_c) for r, c in shape]
    # Sort for consistency in deduplication
    return sorted(normalized)


def get_all_orientations(shape: List[Tuple[int, int]]) -> List[List[Tuple[int, int]]]:
    """Generate all unique rotations and flips of a shape."""
    orientations = set()
    
    current = shape
    for _ in range(4):  # 4 rotations
        normalized = tuple(normalize_shape(current))
        orientations.add(normalized)
        current = rotate_90(current)
    
    # Flip and rotate
    current = flip_horizontal(shape)
    for _ in range(4):  # 4 rotations of flipped shape
        normalized = tuple(normalize_shape(current))
        orientations.add(normalized)
        current = rotate_90(current)
    
    return [list(o) for o in orientations]


def can_place_shape(grid: Set[Tuple[int, int]], shape: List[Tuple[int, int]], 
                    row: int, col: int, width: int, height: int) -> bool:
    """Check if shape can be placed at position without overlap or going out of bounds."""
    for dr, dc in shape:
        r, c = row + dr, col + dc
        # Check bounds
        if r < 0 or r >= height or c < 0 or c >= width:
            return False
        # Check overlap
        if (r, c) in grid:
            return False
    return True


# Alias for compatibility
can_place = can_place_shape


def place_shape(grid: Set[Tuple[int, int]], shape: List[Tuple[int, int]], 
                row: int, col: int) -> None:
    """Place shape on grid at given position."""
    for dr, dc in shape:
        grid.add((row + dr, col + dc))


def remove_shape(grid: Set[Tuple[int, int]], shape: List[Tuple[int, int]], 
                 row: int, col: int) -> None:
    """Remove shape from grid at given position."""
    for dr, dc in shape:
        grid.discard((row + dr, col + dc))


def backtrack(grid: Set[Tuple[int, int]], pieces_to_place: List[List[List[Tuple[int, int]]]], 
              idx: int, width: int, height: int) -> bool:
    """
    Recursively try to place all pieces.
    
    Args:
        grid: Current set of occupied positions
        pieces_to_place: List of pieces, each piece is a list of possible orientations
        idx: Index of current piece to place
        width, height: Region dimensions
    
    Returns:
        True if all pieces can be placed, False otherwise
    """
    # Base case: all pieces placed successfully
    if idx >= len(pieces_to_place):
        return True
    
    piece_orientations = pieces_to_place[idx]
    
    # Try each orientation
    for orientation in piece_orientations:
        # Try each position in the grid
        # Optimization: start from top-left and go row by row
        for row in range(height):
            for col in range(width):
                if can_place_shape(grid, orientation, row, col, width, height):
                    # Place the piece
                    place_shape(grid, orientation, row, col)
                    
                    # Recursively try to place remaining pieces
                    if backtrack(grid, pieces_to_place, idx + 1, width, height):
                        return True
                    
                    # Backtrack: remove the piece
                    remove_shape(grid, orientation, row, col)
    
    return False


def solve_region(shapes: List[List[Tuple[int, int]]], region: Dict) -> bool:
    """Determine if all required presents can fit in the region."""
    width = region['width']
    height = region['height']
    required = region['required']
    
    # Build list of pieces to place
    pieces_to_place = []
    for shape_idx, count in enumerate(required):
        for _ in range(count):
            # Get all orientations for this shape
            orientations = get_all_orientations(shapes[shape_idx])
            pieces_to_place.append(orientations)
    
    # Quick area check: if total area of all pieces > region area, impossible
    total_area = sum(len(shapes[shape_idx]) for shape_idx, count in enumerate(required) for _ in range(count))
    region_area = width * height
    if total_area > region_area:
        return False
    
    # If no pieces to place, it's trivially feasible
    if not pieces_to_place:
        return True
    
    # Sort pieces by size (largest first) for better pruning
    pieces_to_place.sort(key=lambda orientations: -len(orientations[0]))
    
    # Use backtracking to try to place all pieces
    grid = set()
    return backtrack(grid, pieces_to_place, 0, width, height)


def solve_part1(data) -> int:
    """
    Solve part 1 of the puzzle.
    
    Count how many regions can fit all their required presents.
    """
    shapes, regions = data
    
    count = 0
    for region in regions:
        if solve_region(shapes, region):
            count += 1
    
    return count


def solve_part2(data) -> int | None:
    """
    Solve part 2 of the puzzle.
    
    Part 2 requirements will be revealed after completing Part 1.
    """
    # TODO: implement part 2
    return None


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

    # Edge case: Empty region (0 presents required)
    empty_region_test = """0:
###

1x1: 0"""
    result = solve_part1(parse_input(empty_region_test))
    assert result == 1, f"Expected 1 (empty region should be feasible), got {result}"
    print("  ✓ Empty region test")

    # Edge case: Single 1x1 present in 1x1 region
    single_cell_test = """0:
#

1x1: 1"""
    result = solve_part1(parse_input(single_cell_test))
    assert result == 1, f"Expected 1 (exact fit), got {result}"
    print("  ✓ Single cell exact fit")

    # Edge case: Present too large for region
    too_large_test = """0:
###
###
###

2x2: 1"""
    result = solve_part1(parse_input(too_large_test))
    assert result == 0, f"Expected 0 (present too large), got {result}"
    print("  ✓ Present too large test")
    
    # Test with multiple pieces that can fit
    two_pieces_test = """0:
##

1:
##

2x2: 1 1"""
    result = solve_part1(parse_input(two_pieces_test))
    assert result == 1, f"Expected 1 (two 2-cell pieces in 2x2), got {result}"
    print("  ✓ Two pieces fit test")

    print("\n✅ All tests passed!")


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        test()
    else:
        main()
