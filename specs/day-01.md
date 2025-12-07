# Day 01: Figure out the Password

## Problem Description

There is a dial, pointing to 50. You are given a list of instructions. Each instruction is either a left turn (L) or a right turn (R) followed by a number. The number represents the number of steps to take in the direction the dial is pointing. The dial always points at the number it was pointing before the turn. The dial starts pointing to 50. The dial wraps around, so after 99 it goes back to 0. 

## Input
The input is located in input.txt

## Input Format

A series of instructions, one per line. Each instruction is either a left turn (L) or a right turn (R) followed by a number. 

Example:
```
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
```

## Output Format

The number of times the dial pointed to zero

Example:
```
3
```

## Requirements

### Part 1

Your goal is to find how many times the dial is pointing at zero. 

#### Part 1 Example Answer
3

**Explanation:**
Following these rotations would cause the dial to move as follows:

    The dial starts by pointing at 50.
    The dial is rotated L68 to point at 82.
    The dial is rotated L30 to point at 52.
    The dial is rotated R48 to point at 0.
    The dial is rotated L5 to point at 95.
    The dial is rotated R60 to point at 55.
    The dial is rotated L55 to point at 0.
    The dial is rotated L1 to point at 99.
    The dial is rotated L99 to point at 0.
    The dial is rotated R14 to point at 14.
    The dial is rotated L82 to point at 32.

Because the dial points at 0 a total of three times during this process, the password in this example is 3.

### Part 2 (if applicable)

Instead of counting the number of times it lands on 0, count the number of times it points at 0 during a rotation. 

#### Part 2 Example Answer
6

**Explanation:**
Following the same rotations as in the above example, the dial points at zero a few extra times during its rotations:

    The dial starts by pointing at 50.
    The dial is rotated L68 to point at 82; during this rotation, it points at 0 once.
    The dial is rotated L30 to point at 52.
    The dial is rotated R48 to point at 0.
    The dial is rotated L5 to point at 95.
    The dial is rotated R60 to point at 55; during this rotation, it points at 0 once.
    The dial is rotated L55 to point at 0.
    The dial is rotated L1 to point at 99.
    The dial is rotated L99 to point at 0.
    The dial is rotated R14 to point at 14.
    The dial is rotated L82 to point at 32; during this rotation, it points at 0 once.

In this example, the dial points at 0 three times at the end of a rotation, plus three more times during a rotation. So, in this example, the new password would be 6.

Be careful: if the dial were pointing at 50, a single rotation like R1000 would cause the dial to point at 0 ten times before returning back to 50!

## Test Cases

### Part 1 Tests

| Input | Expected | Notes |
|-------|----------|-------|
| `L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82` | `3` | Main example from problem |
| `R50` | `1` | Single move landing exactly on 0 |
| `L50` | `1` | Single move left landing exactly on 0 |
| `R49` | `0` | Single move, doesn't reach 0 |
| `L49` | `0` | Single move left, doesn't reach 0 |
| `R50\nL100` | `2` | Two moves, both land on 0 |

### Part 2 Tests

| Input | Expected | Notes |
|-------|----------|-------|
| `L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82` | `6` | Main example: 3 landings + 3 pass-throughs |
| `R1000` | `10` | Large rotation from 50, passes 0 ten times |
| `R50` | `1` | Lands exactly on 0, counts once |
| `R150` | `2` | Passes 0 at step 50 and 150 |
| `L50\nR100` | `2` | First lands on 0, second passes through 0 once |

### Step-by-Step Trace (for validation)

For the main example, verify intermediate positions:
```
Start: 50
L68 → 82
L30 → 52
R48 → 0   ← lands on 0
L5  → 95
R60 → 55
L55 → 0   ← lands on 0
L1  → 99
L99 → 0   ← lands on 0
R14 → 14
L82 → 32
```

Part 2 additional zero crossings during rotation:
- L68 (50→82): passes through 0 once
- R60 (95→55): passes through 0 once
- L82 (14→32): passes through 0 once
