# Day 4: Printing Department

## Problem Description

The input grid represents locations of rolls of paper that a forklift needs to access. A roll can be accessed if one of the 8 spots around it does not contain another role

## Input

The input is located in `input.txt`

## Input Format

Each line represents the row of a grid. A `@` on the grid represents a roll of paper. A `.` represents an empty space.

Example:

```
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
```

## Output Format

an integer representing the number of rolls of toilet paper the forklift can access.

Example:

```
13
```

## Requirements

### Part 1

A roll is accessible if it has fewer than 4 rolls of paper in the eight adjacent positions
For each coordinate, check the 8 locations around it for the existence of a roll. If there are 4 roles or more around it, then do not count the roll

#### Part 1 Example Answer

13

**Explanation:**
This grid shows the 13 rolls that are accessible in the original grid, marked by an `x`

```
..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.
```

| Coordinate | Accessible? | Why?                                                                                                  |
| ---------- | ----------- | ----------------------------------------------------------------------------------------------------- |
| [0,2]      | Y           | only 3 Rolls around it, at [1,1], [1,2], and [0,3]                                                    |
| [0,7       | N           | Columns 6 and 8 contain rolls, as does [7,1]. [7,-1] has a negative coordinate, so it is inaccessible |

### Part 2

Since we have a forklift, we can remove rolls of paper to make them more accessible. Setup a loop to count how many rolls of paper can be removed. For each iteration, you remove the rolls that can be accessed and iterate over the updated grid. Figure out how many rolls can be removed

#### Part 2 Example Answer

43

**Explanation:**
```
Initial state:
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.

Remove 13 rolls of paper:
..xx.xx@x.
x@@.@.@.@@
@@@@@.x.@@
@.@@@@..@.
x@.@@@@.@x
.@@@@@@@.@
.@.@.@.@@@
x.@@@.@@@@
.@@@@@@@@.
x.x.@@@.x.

Remove 12 rolls of paper:
.......x..
.@@.x.x.@x
x@@@@...@@
x.@@@@..x.
.@.@@@@.x.
.x@@@@@@.x
.x.@.@.@@@
..@@@.@@@@
.x@@@@@@@.
....@@@...

Remove 7 rolls of paper:
..........
.x@.....x.
.@@@@...xx
..@@@@....
.x.@@@@...
..@@@@@@..
...@.@.@@x
..@@@.@@@@
..x@@@@@@.
....@@@...

Remove 5 rolls of paper:
..........
..x.......
.x@@@.....
..@@@@....
...@@@@...
..x@@@@@..
...@.@.@@.
..x@@.@@@x
...@@@@@@.
....@@@...

Remove 2 rolls of paper:
..........
..........
..x@@.....
..@@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@x.
....@@@...

Remove 1 roll of paper:
..........
..........
...@@.....
..x@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
...x@.....
...@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
....x.....
...@@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...

Remove 1 roll of paper:
..........
..........
..........
...x@@....
...@@@@...
...@@@@@..
...@.@.@@.
...@@.@@@.
...@@@@@..
....@@@...
```

## Test Cases

Distinct test cases should be documented here. Do not write additional tests without them being documented here in the spec. If a test doesn't exist and should be created, suggest that test to the user.

### Part 1 Tests

| Input            | Expected   | Notes                       |
| ---------------- | ---------- | --------------------------- |
| `[main example]` | `[answer]` | Main example from problem   |
| `[simple case]`  | `[answer]` | [why this case matters]     |
| `[edge case]`    | `[answer]` | [boundary condition tested] |

### Part 2 Tests

| Input            | Expected   | Notes             |
| ---------------- | ---------- | ----------------- |
| `[main example]` | `[answer]` | Main example      |
| `[edge case]`    | `[answer]` | [what this tests] |

### Step-by-Step Trace (for validation)

For the main example, verify intermediate states:

```
[Initial state]
[Step 1] → [result]
[Step 2] → [result]  ← [notable event]
...
```
