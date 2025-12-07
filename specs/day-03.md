# Day 3: Lobby

## Problem Description

We are looking for the batteries we need to turn on to make the system work. 
## Input

The input is located in `input.txt`

## Input Format

Each line represents a bank of batteries. Each index represents 1 battery and the value is the voltage.
Example:
```
987654321111111
811111111111119
234234234234278
818181911112111
```

## Output Format

The solution is a single number


## Requirements

### Part 1

Look at each line, and find the largest number to represent the 10s digit, then the next largest number to reperesent the 1s digit. That represetns the two batteries you turn on. Add up all of the voltages of each bank and you have the answer.

#### Part 1 Example Answer
357

**Explanation:**

    In 987654321111111, you can make the largest joltage possible, 98, by turning on the first two batteries.
    In 811111111111119, you can make the largest joltage possible by turning on the batteries labeled 8 and 9, producing 89 jolts.
    In 234234234234278, you can make 78 by turning on the last two batteries (marked 7 and 8).
    In 818181911112111, the largest joltage you can produce is 92.


### Part 2

There needs joltage for each bank needs to be 12 digits, Update part 2 to find the 12 batteries to turn on to create the largest possible joltage. So the first number is the 100,000,000,000s digit, the second number is the 10,000,000,000s digit, and so on.

#### Part 2 Example Answer
3121910778619

**Explanation:**

    In 987654321111111, the largest joltage can be found by turning on everything except some 1s at the end to produce 987654321111.
    In the digit sequence 811111111111119, the largest joltage can be found by turning on everything except some 1s, producing 811111111119.
    In 234234234234278, the largest joltage can be found by turning on everything except a 2 battery, a 3 battery, and another 2 battery near the start to produce 434234234278.
    In 818181911112111, the joltage 888911112111 is produced by turning on everything except some 1s near the front.


## Test Cases

### Part 1 Tests

| Input | Expected | Notes |
|-------|----------|-------|
| `987654321111111\n811111111111119\n234234234234278\n818181911112111` | `357` | Main example from problem |
| `12` | `12` | Minimal two-battery bank |
| `21` | `21` | Two batteries, larger first |
| `5555` | `55` | All same digits |
| `123456789` | `89` | Ascending order - best pair at end |
| `987654321` | `98` | Descending order - best pair at start |
| `1119` | `19` | Max digit at end |
| `00` | `0` | All zeros |
| `09` | `9` | Zero as tens digit |
| `90` | `90` | Zero as ones digit |

### Part 2 Tests

| Input | Expected | Notes |
|-------|----------|-------|
| `987654321111111\n811111111111119\n234234234234278\n818181911112111` | `3121910778619` | Main example from problem |
| `123456789012` | `123456789012` | Exactly 12 digits - no choice |
| `1234567890123` | `234567890123` | 13 digits - skip the smallest (1) |
| `555555555555555` | `555555555555` | All same digits |
| `9876543210000` | `987654321000` | Descending with zeros |
| `12345` | `12345` | Fewer than 12 digits - use all |

### Step-by-Step Trace (for validation)

For bank `818181911112111` → `888911112111`:
```
Need 12 digits from 15 chars, must skip 3.
Digit 1: indices 0-3 (8,1,8,1) → pick '8' at idx 0
Digit 2: indices 1-4 (1,8,1,8) → pick '8' at idx 2
Digit 3: indices 3-5 (1,8,1) → pick '8' at idx 4
Digit 4: indices 5-6 (1,9) → pick '9' at idx 6
Digits 5-12: only one valid position each → 11112111
Result: 888911112111 ✓
```
