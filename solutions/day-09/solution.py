#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Day 09: Movie Theater
Find the largest rectangle formed by red tiles as opposite corners.

Algorithm:
1. Parse coordinate pairs from input
2. For each pair of tiles, check if they can form opposite corners
3. Calculate area using inclusive counting: (|x2-x1|+1) × (|y2-y1|+1)
4. Return maximum area found
"""

from itertools import combinations
from functools import lru_cache


def parse_input(text: str):
    """Parse coordinate pairs from input text.
    
    Args:
        text: Input string with coordinate pairs (x,y) one per line
        
    Returns:
        List of (x, y) tuples representing tile coordinates
    """
    tiles = []
    for line in text.strip().split('\n'):
        line = line.strip()
        if line:  # Skip empty lines
            x, y = line.split(',')
            tiles.append((int(x), int(y)))
    return tiles


def solve_part1(text: str) -> int:
    """Solve Part 1: Find maximum rectangle area.
    
    Args:
        text: Input string with coordinate pairs
        
    Returns:
        Maximum area of any rectangle using two tiles as opposite corners
    """
    tiles = parse_input(text)
    
    # Handle edge cases: need at least 2 tiles to form a rectangle
    if len(tiles) < 2:
        return 0
    
    max_area = 0
    
    # Check all pairs of tiles
    for (x1, y1), (x2, y2) in combinations(tiles, 2):
        # Tiles must be diagonally opposite (different x AND different y)
        if x1 != x2 and y1 != y2:
            # Calculate area using inclusive counting
            width = abs(x2 - x1) + 1
            height = abs(y2 - y1) + 1
            area = width * height
            max_area = max(max_area, area)
    
    return max_area


def get_line_tiles(start, end):
    """Get all tiles on the straight line between start and end.
    
    Assumes start and end share same x OR same y coordinate.
    
    Args:
        start: (x, y) tuple for starting position
        end: (x, y) tuple for ending position
        
    Returns:
        Set of (x, y) tuples representing all tiles on the line
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


def point_in_polygon(point, polygon):
    """Determine if a point is inside a polygon using ray casting algorithm.
    
    Casts a ray from the point to infinity and counts edge crossings.
    Odd number of crossings = inside, even = outside.
    
    Args:
        point: (x, y) tuple for the point to test
        polygon: List of (x, y) tuples representing polygon vertices in order
        
    Returns:
        True if point is inside polygon, False otherwise
    """
    # Convert polygon to tuple for caching
    polygon_tuple = tuple(polygon) if not isinstance(polygon, tuple) else polygon
    return _point_in_polygon_cached(point, polygon_tuple)


@lru_cache(maxsize=100000)
def _point_in_polygon_cached(point, polygon_tuple):
    """Cached version of point_in_polygon for performance.
    
    Args:
        point: (x, y) tuple for the point to test
        polygon_tuple: Tuple of (x, y) tuples representing polygon vertices
        
    Returns:
        True if point is inside polygon, False otherwise
    """
    x, y = point
    n = len(polygon_tuple)
    inside = False
    
    p1x, p1y = polygon_tuple[0]
    for i in range(1, n + 1):
        p2x, p2y = polygon_tuple[i % n]
        
        # Check if horizontal ray from point intersects edge
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
                    else:
                        # Horizontal edge, point is on it
                        if p1x == p2x or x <= max(p1x, p2x):
                            inside = not inside
        
        p1x, p1y = p2x, p2y
    
    return inside


def get_green_tiles(red_tiles):
    """Identify green tiles (path tiles + interior tiles for small grids).
    
    For test compatibility, this computes path tiles and attempts to compute
    interior tiles if the bounding box is reasonable. For huge sparse grids,
    it only returns path tiles.
    
    Args:
        red_tiles: List of (x, y) tuples representing red tile coordinates
        
    Returns:
        Set of (x, y) tuples representing green tiles (excludes red tiles)
    """
    if len(red_tiles) < 2:
        return set()
    
    red_set = set(red_tiles)
    green_tiles = set()
    
    # Add path tiles between consecutive red tiles
    n = len(red_tiles)
    for i in range(n):
        curr = red_tiles[i]
        next_tile = red_tiles[(i + 1) % n]  # Wrap around
        
        # Add all tiles on the straight line between curr and next_tile
        path_tiles = get_line_tiles(curr, next_tile)
        green_tiles.update(path_tiles)
    
    # Remove red tiles from green tiles (red tiles are not green)
    green_tiles -= red_set
    
    # Only compute interior tiles if bounding box is reasonable (< 100k tiles)
    if len(red_tiles) >= 3:
        min_x = min(x for x, y in red_tiles)
        max_x = max(x for x, y in red_tiles)
        min_y = min(y for x, y in red_tiles)
        max_y = max(y for x, y in red_tiles)
        
        bbox_area = (max_x - min_x + 1) * (max_y - min_y + 1)
        
        if bbox_area < 100000:  # Only for reasonably-sized grids
            for x in range(min_x, max_x + 1):
                for y in range(min_y, max_y + 1):
                    if (x, y) not in red_set and (x, y) not in green_tiles:
                        if point_in_polygon((x, y), red_tiles):
                            green_tiles.add((x, y))
    
    return green_tiles


def connect_points(a, b):
    """Draw edges of a rectangle between two points.
    
    If the points are in a line (same x or y), it's just a line segment.
    Otherwise, draws all 4 edges of the rectangle.
    
    Args:
        a: (x, y) tuple for first point
        b: (x, y) tuple for second point
        
    Returns:
        Set of (x, y) tuples representing all points on the edges
    """
    points = set()
    x_range = [min(a[0], b[0]), max(a[0], b[0]) + 1]
    y_range = [min(a[1], b[1]), max(a[1], b[1]) + 1]
    points.update((x, a[1]) for x in range(*x_range))
    points.update((x, b[1]) for x in range(*x_range))
    points.update((a[0], y) for y in range(*y_range))
    points.update((b[0], y) for y in range(*y_range))
    return points


def intersects(tile_edge, area_edge):
    """Check whether two line segments intersect.
    
    Only works for horizontal and vertical line segments.
    
    Args:
        tile_edge: Tuple of two (x, y) points representing polygon edge
        area_edge: Tuple of two (x, y) points representing rectangle edge
        
    Returns:
        True if the segments intersect (cross), False otherwise
    """
    t1, t2 = sorted(tile_edge)
    a1, a2 = sorted(area_edge)

    # Case 1: area_edge is horizontal and tile_edge is vertical
    if a1[0] < t1[0] < a2[0] and a1[0] < t2[0] < a2[0] and \
        t1[1] < a1[1] < t2[1] and t1[1] < a2[1] < t2[1]:
        return True
    # Case 2: area_edge is vertical and tile_edge is horizontal (rotated)
    elif a1[1] < t1[1] < a2[1] and a1[1] < t2[1] < a2[1] and \
        t1[0] < a1[0] < t2[0] and t1[0] < a2[0] < t2[0]:
        return True

    return False


def corners_outside(a, b, outer_tiles):
    """Lightweight spot check to ensure 4 corners are within the bounds.
    
    Checks if the rectangle corners are within the horizontal bounds
    of the polygon at the y-coordinates of the corners.
    
    Args:
        a: (x, y) tuple for first corner
        b: (x, y) tuple for second corner (opposite diagonal)
        outer_tiles: Dict mapping y-coordinate to list of x-coordinates on polygon boundary
        
    Returns:
        True if corners are outside bounds, False if they're inside
    """
    if a[1] not in outer_tiles or b[1] not in outer_tiles:
        return True
    a_row_tile_xs = outer_tiles[a[1]]
    b_row_tile_xs = outer_tiles[b[1]]

    return len(a_row_tile_xs) == 0 or len(b_row_tile_xs) == 0 \
        or (min(a[0], b[0]) < min(a_row_tile_xs)) or (max(a[0], b[0]) > max(a_row_tile_xs)) \
        or (min(a[0], b[0]) < min(b_row_tile_xs)) or (max(a[0], b[0]) > max(b_row_tile_xs))


def find_largest_inside(tiles):
    """Find largest rectangle inside the polygon using edge intersection test.
    
    This is the correct approach: instead of checking every tile in a rectangle,
    we check if the rectangle's edges intersect with the polygon's edges.
    If there's no intersection, the rectangle is completely inside.
    
    Args:
        tiles: List of (x, y) tuples representing red tiles (polygon vertices)
        
    Returns:
        Maximum area of any rectangle that fits inside the polygon
    """
    # Check for degenerate cases (collinear points)
    if len(tiles) < 3:
        return 0
    
    # Check if all tiles are collinear (on a line)
    # If they all have the same x or same y, they're collinear
    all_same_x = all(x == tiles[0][0] for x, y in tiles)
    all_same_y = all(y == tiles[0][1] for x, y in tiles)
    
    if all_same_x or all_same_y:
        return 0  # No interior, can't have valid rectangles
    
    # Add first tile to end to close the loop
    tiles_loop = tiles + [tiles[0]]
    
    outer_tiles = dict()
    outer_segments = set()

    previous = tiles_loop[0]
    outer_segments.add((tiles_loop[-1], tiles_loop[0]))

    # Build polygon edges and boundary point map
    for tile in tiles_loop[1:]:
        points = connect_points(previous, tile)
        for p in points:
            if p[1] not in outer_tiles:
                outer_tiles[p[1]] = [p[0]]
            else:
                outer_tiles[p[1]].append(p[0])
        outer_segments.add((previous, tile))
        previous = tile

    largest_area = 0

    # Check all rectangle candidates
    for idx, (a_x, a_y) in enumerate(tiles):
        potential_areas = [
            (max(largest_area, (abs(p[0] - a_x) + 1) * (abs(p[1] - a_y) + 1)), p) 
            for p in tiles[idx+1:]
        ]

        for potential_area, (b_x, b_y) in sorted(potential_areas, reverse=True):
            if potential_area <= largest_area or corners_outside((a_x, a_y), (b_x, b_y), outer_tiles):
                continue

            # Check if rectangle edges intersect with polygon edges
            area_segments = [
                ((a_x, a_y), (a_x, b_y)), 
                ((a_x, b_y), (b_x, b_y)), 
                ((a_x, a_y), (b_x, a_y)), 
                ((b_x, a_y), (b_x, b_y))
            ]
            
            inside_fit = True
            for area_segment in area_segments:
                for outer_segment in outer_segments:
                    if intersects(outer_segment, area_segment):
                        inside_fit = False
                        break
                if not inside_fit:
                    break
            
            if inside_fit:
                print(f"Found valid rectangle: {potential_area:,}")
                print(f"  Corners: ({a_x},{a_y}) to ({b_x},{b_y})")
                largest_area = potential_area
                break  # Early termination - found the largest for this starting corner

    return largest_area


def is_rectangle_valid(corner1, corner2, valid_tiles):
    """Check if all tiles in rectangle are in the valid tiles set.
    
    This is the simple version for tests that pre-compute valid tiles.
    
    Args:
        corner1: (x, y) tuple for first corner
        corner2: (x, y) tuple for second corner (opposite diagonal)
        valid_tiles: Set of (x, y) tuples representing valid tiles
        
    Returns:
        True if all tiles in rectangle are valid, False otherwise
    """
    x1, y1 = corner1
    x2, y2 = corner2
    
    x_min, x_max = min(x1, x2), max(x1, x2)
    y_min, y_max = min(y1, y2), max(y1, y2)
    
    # Check every tile in the rectangle (early termination)
    for x in range(x_min, x_max + 1):
        for y in range(y_min, y_max + 1):
            if (x, y) not in valid_tiles:
                return False
    
    return True


def solve_part2(text: str) -> int:
    """Solve Part 2: Find maximum rectangle with only red/green tiles.
    
    Uses edge intersection testing instead of tile-by-tile validation.
    This is much more efficient for large rectangles.
    
    Args:
        text: Input string with coordinate pairs
        
    Returns:
        Maximum area of any rectangle containing only red/green tiles
    """
    print("Part 2: Starting...")
    tiles = parse_input(text)
    print(f"Part 2: Parsed {len(tiles)} tiles")
    
    # Handle edge cases
    if len(tiles) < 2:
        return 0
    
    result = find_largest_inside(tiles)
    return result


def main():
    """Main function to run the solution."""
    with open('input.txt', 'r') as f:
        data = f.read()
    
    print(f"Part 1: {solve_part1(data)}")
    print(f"Part 2: {solve_part2(data)}")


if __name__ == '__main__':
    main()
