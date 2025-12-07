# Day 02: Gift Shop

## Problem Description

YOu are helping out in a gift shop, and the elves have miss-entered several product codes. You need to figure out the correct codes.


## Input

The input is located in `input.txt`

## Input Format

The input is a range of numbers, separated by commas. A range follows the format `start-end`, where `start` and `end` are both inclusive. IDs do not start with zero. 

Example:
```
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
1698522-1698528,446443-446449,38593856-38593862,565653-565659,
824824821-824824827,2121212118-2121212124
```

## Output Format

The solution is a single number

Example:
```
1227775554
```

## Requirements

### Part 1
An invalid product code is any ID which is made only of some sequence of digits repeated twice
Sum up all the invalid product codes
#### Part 1 Example Answer
1227775554

**Explanation:**
Your job is to find all of the invalid IDs that appear in the given ranges. In the above example:

    11-22 has two invalid IDs, 11 and 22.
    95-115 has one invalid ID, 99.
    998-1012 has one invalid ID, 1010.
    1188511880-1188511890 has one invalid ID, 1188511885.
    222220-222224 has one invalid ID, 222222.
    1698522-1698528 contains no invalid IDs.
    446443-446449 has one invalid ID, 446446.
    38593856-38593862 has one invalid ID, 38593859.
    The rest of the ranges contain no invalid IDs.


### Part 2

an invalid product code is whenever there is a set of 2 repeated sequences of numbers
#### Part 2 Example Answer
4174379265

**Explanation:**

    11-22 still has two invalid IDs, 11 and 22.
    95-115 now has two invalid IDs, 99 and 111.
    998-1012 now has two invalid IDs, 999 and 1010.
    1188511880-1188511890 still has one invalid ID, 1188511885.
    222220-222224 still has one invalid ID, 222222.
    1698522-1698528 still contains no invalid IDs.
    446443-446449 still has one invalid ID, 446446.
    38593856-38593862 still has one invalid ID, 38593859.
    565653-565659 now has one invalid ID, 565656.
    824824821-824824827 now has one invalid ID, 824824824.
    2121212118-2121212124 now has one invalid ID, 2121212121.


## Test Cases

### Part 1 Tests

| Input | Expected | Notes |
|-------|----------|-------|
| `11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124` | `1227775554` | Main example from problem |
| `11-11` | `11` | Smallest invalid code |
| `10-12` | `11` | Range containing one invalid |
| `12-15` | `0` | Range with no invalid codes |
| `99-99` | `99` | Single digit repeated twice |
| `1212-1212` | `1212` | 2-digit pattern repeated |
| `111-111` | `0` | Odd length - NOT invalid for Part 1 |
| `121212-121212` | `0` | 121≠212, not two equal halves |

### Part 2 Tests

| Input | Expected | Notes |
|-------|----------|-------|
| `11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124` | `4174379265` | Main example |
| `11-11` | `11` | Same as Part 1 |
| `111-111` | `111` | NEW: 1 repeated 3x |
| `999-999` | `999` | NEW: 9 repeated 3x |
| `121212-121212` | `121212` | NEW: 12 repeated 3x |
| `1000-1000` | `0` | Has "00" but not full repetition |
| `100100-100100` | `100100` | Pattern with leading zeros works |

### Key Distinctions

| Number | Part 1 | Part 2 | Why |
|--------|--------|--------|-----|
| `111` | ❌ | ✅ | Odd length fails Part 1; `1×3` passes Part 2 |
| `121212` | ❌ | ✅ | `121≠212`; but `12×3` passes Part 2 |
| `1000` | ❌ | ❌ | Neither rule applies |
| `9999` | ✅ | ✅ | Both: `99×2` and `9×4` |
