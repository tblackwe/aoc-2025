# Day 10: Factory

## Problem Description

This is a **linear algebra over GF(2)** (Galois Field 2) problem disguised as a machine initialization puzzle. Each machine has indicator lights that must be set to specific states by pressing buttons that toggle groups of lights. The goal is to find the minimum number of button presses required to configure all lights correctly.

### Core Challenge

The fundamental mechanic is:
- **State**: Each indicator light is either on (`#`) or off (`.`)
- **Operations**: Buttons toggle specific sets of lights (on→off, off→on)
- **Goal**: Transform all lights from initial state (all off) to target state
- **Optimization**: Find the minimum total button presses across all machines

This is equivalent to solving a **system of linear equations over GF(2)** where:
- Variables are the number of times each button is pressed (0 or 1 in optimal solution)
- Equations represent the final state of each light
- Operations are XOR (toggle) rather than addition

### What Makes This Challenging

1. **Mathematical foundation**: Recognizing this as a linear algebra problem
2. **Modular arithmetic**: Working in GF(2) where 1 + 1 = 0 (toggle twice = no change)
3. **Optimal solution**: Multiple button combinations may work, need minimum presses
4. **Gaussian elimination**: Solving the system efficiently
5. **Edge cases**: Unsolvable systems, redundant buttons, no-solution machines

### Example

Given machine:
```
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
```

- **Target state**: `.##.` (4 lights: off, on, on, off)
- **Buttons available**:
  - `(3)`: toggles light 3
  - `(1,3)`: toggles lights 1 and 3
  - `(2)`: toggles light 2
  - `(2,3)`: toggles lights 2 and 3
  - `(0,2)`: toggles lights 0 and 2
  - `(0,1)`: toggles lights 0 and 1
- **Joltage**: `{3,5,4,7}` (ignore - not relevant)

**Optimal solution**: Press buttons `(0,2)` and `(0,1)` once each = **2 presses**

**Why this works**:
- Start: `....` (all off)
- Press `(0,2)`: toggles lights 0,2 → `#.#.`
- Press `(0,1)`: toggles lights 0,1 → `.##.` ✓

## Input Format

Each line represents one machine with three components:

```
[indicator_diagram] (button1) (button2) ... (buttonN) {joltage_values}
```

### Components

1. **Indicator Light Diagram**: `[...]`
   - Shows target state for lights
   - `.` = off (0)
   - `#` = on (1)
   - Number of characters = number of lights
   - Lights are indexed from 0 (leftmost)

2. **Button Wiring Schematics**: `(...)`
   - Each `(...)` is one button
   - Contains comma-separated light indices that the button toggles
   - Indices are 0-based
   - Example: `(0,3,4)` toggles lights 0, 3, and 4

3. **Joltage Requirements**: `{...}`
   - Comma-separated numbers
   - **Can be safely ignored** (machines are offline)

### Example Input

```
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
```

### Parsing Requirements

For each line:
1. Extract indicator diagram between `[` and `]`
2. Extract all button patterns between `(` and `)`
3. Parse each button as comma-separated integers
4. Ignore joltage values in `{}`

**Parsing gotchas**:
- Multiple spaces between components
- Buttons may toggle 1 to many lights
- Light indices must be < number of lights
- Empty button list would be invalid (but unlikely in input)

## Output Format

**Part 1**: A single integer representing the minimum total button presses required to configure all machines' indicator lights.

Example: `7` (sum of minimum presses across 3 machines: 2 + 3 + 2)

**Part 2**: A single integer representing the minimum total button presses required to configure all machines' joltage level counters.

Example: `33` (sum of minimum presses across 3 machines: 10 + 12 + 11)

## Requirements

### Part 1: Minimum Button Presses (Indicator Light Configuration)

For each machine:
1. **Initial state**: All lights are OFF (0)
2. **Target state**: Pattern shown in indicator diagram
3. **Operations**: Press buttons to toggle lights
4. **Constraint**: Each button must be pressed an integer number of times (0, 1, 2, ...)
5. **Goal**: Find minimum number of button presses to reach target state
6. **Mode**: Indicator light configuration (button wiring shows which lights toggle)

Sum the minimum presses across all machines.

**Key insight**: Since toggling a light twice returns it to original state, optimal solutions only press each button 0 or 1 times. This reduces to solving a system of linear equations over GF(2).

### Part 2: Minimum Button Presses (Joltage Counter Configuration)

**IMPORTANT**: Part 2 uses a completely different interpretation of the machine specifications!

For each machine:
1. **Initial state**: All counters are at 0
2. **Target state**: Joltage requirements `{...}` (previously ignored!)
3. **Operations**: Press buttons to increment specific counters
4. **Constraint**: Each button can be pressed multiple times (0, 1, 2, ..., N)
5. **Goal**: Find minimum number of button presses to reach target joltage levels
6. **Mode**: Joltage counter configuration (button wiring shows which counters to increment)

Sum the minimum presses across all machines.

#### Key Differences from Part 1

| Aspect | Part 1 (Indicator Lights) | Part 2 (Joltage Counters) |
|--------|---------------------------|---------------------------|
| **State** | Binary (on/off) | Integer (0 to target) |
| **Operation** | Toggle (XOR) | Increment (+1) |
| **Target** | Indicator diagram `[.##.]` | Joltage requirements `{3,5,4,7}` |
| **Button effect** | Toggles lights on↔off | Increments counters by 1 |
| **Arithmetic** | GF(2) (mod 2) | Regular integers |
| **Button presses** | 0 or 1 times optimal | 0 to N times |
| **Problem type** | Linear algebra over GF(2) | Integer Linear Programming |
| **Wiring meaning** | Which lights toggle | Which counters increment |

#### Example Explanation

Machine: `[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}`

**Part 1 interpretation**:
- Ignore `{3,5,4,7}` (joltage)
- Use `[.##.]` as target (lights 1,2 on)
- Button `(3)` toggles light 3
- Solve using toggle logic → **2 presses**

**Part 2 interpretation**:
- Ignore `[.##.]` (indicator diagram)
- Use `{3,5,4,7}` as target (counters at [3,5,4,7])
- Button `(3)` increments counter 3
- Solve using increment logic → **10 presses**

#### Mathematical Formulation

For Part 2, we need to solve:

**System of equations**:
```
For each counter i: Σ(x_j where button j affects counter i) = target[i]
```

**In matrix form**:
```
A × x = b
```

Where:
- **A**: Matrix where A[i][j] = 1 if button j increments counter i, 0 otherwise
- **x**: Vector of button press counts (how many times each button is pressed)
- **b**: Vector of target joltage levels

**Constraints**:
- x ≥ 0 (all components non-negative)
- x ∈ ℤⁿ (integer vector)

**Objective**:
```
minimize ||x||₁ = Σ x_j (total button presses)
```

This is an **Integer Linear Programming (ILP)** problem.

#### Step-by-Step Algorithm for Part 2

Unlike Part 1 where we could use Gaussian elimination over GF(2), Part 2 requires a different approach:

1. **Parse machine specification**:
   - Extract joltage requirements as target vector
   - Extract button patterns (which counters each button affects)
   
2. **Build the system**:
   - Create matrix A where A[i][j] = 1 if button j increments counter i
   - Create vector b = target joltage levels
   - Need to solve: Ax = b, x ≥ 0, minimize sum(x)

3. **Solve the ILP problem**:
   - **Option 1**: Use linear programming relaxation + rounding (may not be optimal)
   - **Option 2**: Use simplex/dual simplex for integer solutions
   - **Option 3**: Greedy heuristic with verification
   - **Option 4**: Constraint satisfaction with optimization

4. **Sum across all machines**

#### Example Walkthrough: Machine 1

**Specification**: `[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}`

**Part 2 Setup**:
- **Target joltage**: `{3,5,4,7}` → counters must reach [3, 5, 4, 7]
- **Counters**: 4 counters (indices 0-3)
- **Buttons**: 6 buttons
  - Button 0: `(3)` → increments counter 3
  - Button 1: `(1,3)` → increments counters 1 and 3
  - Button 2: `(2)` → increments counter 2
  - Button 3: `(2,3)` → increments counters 2 and 3
  - Button 4: `(0,2)` → increments counters 0 and 2
  - Button 5: `(0,1)` → increments counters 0 and 1

**Matrix form** (Ax = b):
```
Counter 0: x₄ + x₅ = 3
Counter 1: x₁ + x₅ = 5
Counter 2: x₂ + x₃ + x₄ = 4
Counter 3: x₀ + x₁ + x₃ = 7
```

**One valid solution** (from puzzle):
- Press button `(3)` once: x₀ = 1
- Press button `(1,3)` three times: x₁ = 3
- Press button `(2,3)` three times: x₃ = 3
- Press button `(0,2)` once: x₄ = 1
- Press button `(0,1)` twice: x₅ = 2
- Button `(2)` not pressed: x₂ = 0

**Verification**:
```
Counter 0: x₄ + x₅ = 1 + 2 = 3 ✓
Counter 1: x₁ + x₅ = 3 + 2 = 5 ✓
Counter 2: x₂ + x₃ + x₄ = 0 + 3 + 1 = 4 ✓
Counter 3: x₀ + x₁ + x₃ = 1 + 3 + 3 = 7 ✓
```

**Total presses**: 1 + 3 + 0 + 3 + 1 + 2 = **10 presses**

#### Critical Differences in Solution Space

**Part 1**: Binary solution space
- Each button pressed 0 or 1 times only
- Pressing twice = no effect (toggle back)
- 2ⁿ possible combinations for n buttons
- Small search space even with many buttons

**Part 2**: Unbounded integer solution space
- Each button can be pressed 0, 1, 2, ..., ∞ times
- Multiple presses accumulate
- Infinite solution space (must find bounds)
- Need optimization techniques, not just enumeration

#### Example Walkthrough

**Machine 1**: `[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1)`

**Setup**:
- Target: `[0, 1, 1, 0]`
- Buttons: 6 buttons
  - Button 0: `(3)` → toggles light 3
  - Button 1: `(1,3)` → toggles lights 1, 3
  - Button 2: `(2)` → toggles light 2
  - Button 3: `(2,3)` → toggles lights 2, 3
  - Button 4: `(0,2)` → toggles lights 0, 2
  - Button 5: `(0,1)` → toggles lights 0, 1

**Matrix form** (A × x = b mod 2):
```
Light 0: b4 + b5 = 0
Light 1: b1 + b5 = 1
Light 2: b2 + b3 + b4 = 1
Light 3: b0 + b1 + b3 = 0
```

**Solution**: One valid solution is `b4=1, b5=1, others=0` → **2 presses**

**Verification**:
- Initial: `[0,0,0,0]`
- Press button 4 (0,2): toggles lights 0,2 → `[1,0,1,0]`
- Press button 5 (0,1): toggles lights 0,1 → `[0,1,1,0]` ✓

**Other valid solutions**:
- Press buttons 0,1,2 (3 presses)
- Press buttons 1,2,3,5 (4 presses)
- Press all except button 1 (5 presses)

**Minimum**: 2 presses

## Algorithm Analysis

### Problem Classification

**Part 1** is a **linear algebra problem over GF(2)** with characteristics:
- **System of linear equations**: One equation per light
- **Binary domain (GF(2))**: All operations modulo 2
- **Optimization**: Find minimum weight solution
- **Tractable**: Solvable via Gaussian elimination + enumeration

**Part 2** is an **Integer Linear Programming (ILP)** problem with characteristics:
- **System of linear equations**: One equation per counter
- **Integer domain**: Regular integer arithmetic
- **Optimization**: Minimize L1 norm subject to Ax = b, x ≥ 0
- **NP-hard in general**: But often solvable for small instances

### Part 1 Approaches

#### Approach 1: Gaussian Elimination over GF(2) (Recommended for Part 1)

**Strategy**: Solve the linear system using Gaussian elimination, then find minimum solution from the solution space.

**Algorithm**:

```python
def solve_machine_minimum_presses(target, buttons):
    """
    Solve for minimum button presses using Gaussian elimination over GF(2).
    
    Args:
        target: List of target states [0 or 1 for each light]
        buttons: List of lists, each inner list contains light indices toggled
    
    Returns:
        Minimum number of button presses, or infinity if unsolvable
    """
    num_lights = len(target)
    num_buttons = len(buttons)
    
    # Build augmented matrix [A | b]
    # A[i][j] = 1 if button j toggles light i
    matrix = []
    for i in range(num_lights):
        row = [0] * (num_buttons + 1)
        for j, button in enumerate(buttons):
            if i in button:
                row[j] = 1
        row[num_buttons] = target[i]  # Augment with target
        matrix.append(row)
    
    # Gaussian elimination (forward elimination)
    pivot_row = 0
    pivot_cols = []
    
    for col in range(num_buttons):
        # Find pivot
        found_pivot = False
        for row in range(pivot_row, num_lights):
            if matrix[row][col] == 1:
                # Swap rows
                matrix[pivot_row], matrix[row] = matrix[row], matrix[pivot_row]
                found_pivot = True
                break
        
        if not found_pivot:
            continue  # This column has no pivot, it's a free variable
        
        pivot_cols.append(col)
        
        # Eliminate below
        for row in range(pivot_row + 1, num_lights):
            if matrix[row][col] == 1:
                # XOR rows (mod 2 addition)
                for c in range(num_buttons + 1):
                    matrix[row][c] ^= matrix[pivot_row][c]
        
        pivot_row += 1
    
    # Back substitution to check consistency
    for row in range(pivot_row, num_lights):
        if matrix[row][num_buttons] == 1:
            # Inconsistent: 0 = 1
            return float('inf')  # No solution
    
    # Identify free variables and basic variables
    free_vars = [i for i in range(num_buttons) if i not in pivot_cols]
    
    # If no free variables, unique solution
    if not free_vars:
        # Count how many buttons need to be pressed
        solution = [0] * num_buttons
        for i in range(len(pivot_cols) - 1, -1, -1):
            col = pivot_cols[i]
            val = matrix[i][num_buttons]
            for j in range(col + 1, num_buttons):
                val ^= matrix[i][j] * solution[j]
            solution[col] = val
        return sum(solution)
    
    # Multiple solutions exist, enumerate to find minimum
    # 2^k possibilities where k = number of free variables
    min_presses = float('inf')
    
    for mask in range(1 << len(free_vars)):
        solution = [0] * num_buttons
        
        # Set free variables according to mask
        for i, var in enumerate(free_vars):
            solution[var] = (mask >> i) & 1
        
        # Back substitution for basic variables
        for i in range(len(pivot_cols) - 1, -1, -1):
            col = pivot_cols[i]
            val = matrix[i][num_buttons]
            for j in range(col + 1, num_buttons):
                val ^= matrix[i][j] * solution[j]
            solution[col] = val
        
        # Count total presses
        presses = sum(solution)
        min_presses = min(min_presses, presses)
    
    return min_presses
```

**Time Complexity**:
- Gaussian elimination: O(L × B²) where L = lights, B = buttons
- Enumeration: O(2^F × B) where F = free variables
- Typical case: F is small (0-5), so O(2^F) is manageable
- **Overall**: O(L × B² + 2^F × B)

**Space Complexity**: O(L × B) for the matrix

**Pros**:
- Mathematically rigorous
- Guaranteed to find optimal solution
- Handles all cases (unique, multiple, no solution)
- Efficient for small F

**Cons**:
- Complex implementation
- Exponential in number of free variables (but typically small)
- Requires understanding of GF(2) arithmetic

#### Approach 2: Brute Force Enumeration (Part 1 Only)

**Strategy**: Try all possible combinations of button presses (each 0 or 1).

**Algorithm**:
```python
def solve_machine_brute_force(target, buttons):
    num_buttons = len(buttons)
    min_presses = float('inf')
    
    # Try all 2^num_buttons combinations
    for mask in range(1 << num_buttons):
        state = [0] * len(target)
        presses = 0
        
        # Apply each button according to mask
        for i in range(num_buttons):
            if (mask >> i) & 1:
                presses += 1
                for light in buttons[i]:
                    state[light] ^= 1
        
        # Check if matches target
        if state == target:
            min_presses = min(min_presses, presses)
    
    return min_presses if min_presses != float('inf') else None
```

**Time Complexity**: O(2^B × L) where B = buttons, L = lights

**Space Complexity**: O(L)

**Pros**:
- Simple to implement
- Easy to understand
- Guaranteed correct

**Cons**:
- Exponential in number of buttons
- Too slow for B > 20
- Not practical for typical AoC inputs (B may be 20-30)

**When to use**: Only if B ≤ 15-20 buttons

### Part 2 Approaches

Part 2 is fundamentally different - it's an Integer Linear Programming problem. Here are viable approaches:

#### Approach 1: Linear Programming with Integer Constraints (Recommended for Part 2)

**Strategy**: Use the simplex algorithm or specialized ILP solvers to find optimal integer solution.

**Algorithm**:
```python
from scipy.optimize import linprog
import numpy as np

def solve_machine_part2(targets, buttons):
    """
    Solve ILP problem: minimize sum(x) subject to Ax = b, x ≥ 0, x integer.
    """
    num_counters = len(targets)
    num_buttons = len(buttons)
    
    # Build coefficient matrix A
    A = np.zeros((num_counters, num_buttons))
    for j, button in enumerate(buttons):
        for counter in button:
            A[counter][j] = 1
    
    # Option 1: Use scipy with MILP if available
    # Option 2: Solve LP relaxation, then round and verify
    # Option 3: Custom branch-and-bound
    
    # For AoC, often there's a simpler pattern...
```

**Pros**:
- Optimal solution if solver works correctly
- Leverages existing libraries
- Handles general case

**Cons**:
- May require external library (scipy, pulp, ortools)
- Integer constraints are computationally expensive
- AoC typically avoids requiring external solvers

#### Approach 2: Greedy Algorithm with Backtracking (Practical for Part 2)

**Strategy**: Try to solve the system greedily, using backtracking if needed.

**Key Insight**: If the system has a solution, we can often find it by:
1. Solving the system over real numbers (LP relaxation)
2. Using the solution as a guide
3. Making greedy choices for buttons that affect single counters
4. Backtracking or adjusting if constraints violated

**Algorithm**:
```python
def solve_part2_greedy(targets, buttons):
    """
    Greedy approach: prioritize buttons based on coverage.
    """
    num_counters = len(targets)
    num_buttons = len(buttons)
    
    # Current counter values
    counters = [0] * num_counters
    presses = [0] * num_buttons
    
    # Strategy depends on problem structure:
    # 1. Find buttons that only affect one counter
    # 2. Press them exactly the needed amount
    # 3. For multi-counter buttons, solve the remaining system
    
    # This requires problem-specific analysis
```

**Pros**:
- No external dependencies
- Often works for AoC problems (they're usually "nice")
- Fast for well-structured problems

**Cons**:
- May not find optimal solution for all inputs
- Requires problem-specific insights
- May need verification step

#### Approach 3: Gaussian Elimination + Integer Solution Search

**Strategy**: Use Gaussian elimination (over regular integers, not GF(2)) to reduce the system, then search for minimum integer solution.

**Algorithm**:
```python
def solve_part2_gaussian(targets, buttons):
    """
    Use Gaussian elimination to simplify, then find minimum integer solution.
    """
    # 1. Build augmented matrix [A | b]
    # 2. Gaussian elimination (regular arithmetic, not GF(2))
    # 3. Express solution in terms of free variables
    # 4. Search for non-negative integer assignment to free variables
    # 5. Minimize total presses
    
    # Similar to Part 1 but:
    # - No modulo 2 arithmetic
    # - Search space may be larger
    # - Need bounds on free variables
```

**Complexity**: 
- Gaussian elimination: O(C × B²) where C = counters, B = buttons
- Search: depends on free variables and bounds

**Pros**:
- Builds on Part 1 approach
- Mathematical rigor
- Works if free variables are bounded

**Cons**:
- Free variables may have large ranges
- Harder to bound search space

#### Approach 4: Matrix Inverse Method (If Matrix is Invertible)

**Strategy**: If matrix A is square and invertible, solve directly.

**Algorithm**:
```python
def solve_part2_inverse(targets, buttons):
    """
    If A is square and invertible: x = A⁻¹ · b
    """
    import numpy as np
    
    num_counters = len(targets)
    num_buttons = len(buttons)
    
    if num_counters != num_buttons:
        # System is over/under-determined
        return None
    
    # Build matrix A
    A = np.zeros((num_counters, num_buttons))
    for j, button in enumerate(buttons):
        for counter in button:
            A[counter][j] = 1
    
    # Check if invertible
    if np.linalg.det(A) == 0:
        return None
    
    # Solve: x = A^(-1) * b
    x = np.linalg.solve(A, targets)
    
    # Check if solution is non-negative integers
    if all(xi >= 0 and xi == int(xi) for xi in x):
        return int(sum(x))
    
    return None  # Not a valid integer solution
```

**Pros**:
- Very fast if applicable
- Exact solution

**Cons**:
- Only works if matrix is square and invertible
- Only works if solution happens to be integer and non-negative
- Rare in AoC to be this simple

### Recommended Approach for Part 2

**Start with Approach 4 (Matrix Inverse)** to check if there's a simple solution, then:

**Fall back to Approach 2 (Greedy) or Approach 3 (Gaussian + Search)** depending on problem structure.

**Why this strategy**:
1. AoC problems often have special structure that makes them solvable
2. The examples suggest the systems are "nice" (have clean integer solutions)
3. Avoid external dependencies if possible
4. Can verify solution by simulation

**Implementation priority for Part 2**:
1. Reuse parsing from Part 1 (but use joltage targets)
2. Try matrix inverse method first (quick check)
3. Implement Gaussian elimination over integers
4. Add bounded search for free variables
5. Verify solution correctness
6. Optimize if needed

### Comparison of Part 1 vs Part 2 Approaches

| Aspect | Part 1 | Part 2 |
|--------|--------|--------|
| **Arithmetic** | GF(2) (XOR) | Regular integers |
| **Solution bounds** | Each x_i ∈ {0, 1} | Each x_i ∈ {0, 1, ..., ∞} |
| **Search space** | 2^n combinations | Unbounded (need to find bounds) |
| **Best method** | Gaussian GF(2) + enumeration | Matrix inverse or LP-based |
| **Complexity** | O(L·B² + 2^F·B) | O(C·B²) to O(2^F·B_max) |

## Data Structures

### Primary Structures

**Machine Representation**:
```python
@dataclass
class Machine:
    target: List[int]  # Target state for each light (0 or 1)
    buttons: List[List[int]]  # Each button is a list of light indices it toggles
```

**Matrix for Gaussian Elimination**:
```python
# Augmented matrix [A | b]
# matrix[i][j] = 1 if button j toggles light i
# matrix[i][num_buttons] = target state of light i
matrix: List[List[int]]  # 2D array of 0s and 1s
```

**Solution Vector**:
```python
solution: List[int]  # solution[i] = 1 if button i is pressed, 0 otherwise
```

### Helper Structures

- **Pivot tracking**: `pivot_cols: List[int]` - columns that have pivots
- **Free variables**: `free_vars: List[int]` - buttons that are free variables
- **Current state**: `state: List[int]` - current light states during simulation

**Why these structures**:
- Direct representation of mathematical problem
- Efficient matrix operations with 2D lists
- Clear separation between data and algorithm
- Easy to debug and visualize

## Implementation Guidance

### Step-by-Step Implementation

#### Step 1: Parse Input

```python
import re

def parse_machine(line: str) -> Machine:
    """Parse a single machine specification line."""
    # Extract indicator diagram
    diagram_match = re.search(r'\[(.*?)\]', line)
    diagram = diagram_match.group(1)
    target = [1 if c == '#' else 0 for c in diagram]
    
    # Extract button patterns
    button_matches = re.findall(r'\(([0-9,]+)\)', line)
    buttons = []
    for button_str in button_matches:
        indices = [int(x) for x in button_str.split(',')]
        buttons.append(indices)
    
    return Machine(target, buttons)

def parse_input(text: str) -> List[Machine]:
    """Parse all machines from input text."""
    machines = []
    for line in text.strip().split('\n'):
        if line:
            machines.append(parse_machine(line))
    return machines
```

**Key points**:
- Use regex to extract components
- Convert diagram to binary (0/1)
- Parse button indices as integers
- Handle single-index buttons like `(3)`

#### Step 2: Build Augmented Matrix

```python
def build_matrix(machine: Machine) -> List[List[int]]:
    """
    Build augmented matrix [A | b] for Gaussian elimination.
    Matrix[i][j] = 1 if button j toggles light i.
    Matrix[i][num_buttons] = target state of light i.
    """
    num_lights = len(machine.target)
    num_buttons = len(machine.buttons)
    
    matrix = []
    for light_idx in range(num_lights):
        row = [0] * (num_buttons + 1)
        
        # Check each button
        for button_idx, button in enumerate(machine.buttons):
            if light_idx in button:
                row[button_idx] = 1
        
        # Augment with target
        row[num_buttons] = machine.target[light_idx]
        matrix.append(row)
    
    return matrix
```

#### Step 3: Gaussian Elimination over GF(2)

```python
def gaussian_elimination_gf2(matrix: List[List[int]]) -> tuple:
    """
    Perform Gaussian elimination over GF(2).
    Returns: (reduced_matrix, pivot_cols)
    """
    num_rows = len(matrix)
    num_cols = len(matrix[0]) - 1  # Exclude augmented column
    
    pivot_row = 0
    pivot_cols = []
    
    for col in range(num_cols):
        # Find pivot in this column
        found_pivot = False
        for row in range(pivot_row, num_rows):
            if matrix[row][col] == 1:
                # Swap rows if needed
                if row != pivot_row:
                    matrix[pivot_row], matrix[row] = matrix[row], matrix[pivot_row]
                found_pivot = True
                break
        
        if not found_pivot:
            continue  # Free variable
        
        pivot_cols.append(col)
        
        # Eliminate all other 1s in this column
        for row in range(num_rows):
            if row != pivot_row and matrix[row][col] == 1:
                # XOR this row with pivot row
                for c in range(num_cols + 1):
                    matrix[row][c] ^= matrix[pivot_row][c]
        
        pivot_row += 1
    
    return matrix, pivot_cols
```

**Key operations**:
- Use XOR (`^`) for all arithmetic (mod 2)
- Find pivots and eliminate
- Track which columns have pivots
- Columns without pivots are free variables

#### Step 4: Find Minimum Solution

```python
def find_minimum_solution(matrix: List[List[int]], pivot_cols: List[int]) -> int:
    """
    Find minimum number of button presses from reduced matrix.
    """
    num_buttons = len(matrix[0]) - 1
    num_lights = len(matrix)
    
    # Check for inconsistency
    for row in matrix:
        # Check if row is all zeros except augmented column
        if all(row[i] == 0 for i in range(num_buttons)) and row[num_buttons] == 1:
            return float('inf')  # No solution
    
    # Identify free variables
    free_vars = [i for i in range(num_buttons) if i not in pivot_cols]
    
    # If no free variables, unique solution
    if not free_vars:
        # Extract solution from reduced matrix
        solution = [0] * num_buttons
        for row_idx, col in enumerate(pivot_cols):
            solution[col] = matrix[row_idx][num_buttons]
        return sum(solution)
    
    # Multiple solutions: enumerate all combinations of free variables
    min_presses = float('inf')
    
    for mask in range(1 << len(free_vars)):
        solution = [0] * num_buttons
        
        # Set free variables
        for i, var in enumerate(free_vars):
            solution[var] = (mask >> i) & 1
        
        # Solve for basic variables
        for row_idx, col in enumerate(pivot_cols):
            val = matrix[row_idx][num_buttons]
            for j in range(num_buttons):
                if j != col:
                    val ^= matrix[row_idx][j] * solution[j]
            solution[col] = val
        
        presses = sum(solution)
        min_presses = min(min_presses, presses)
    
    return min_presses
```

#### Step 5: Solve Part 1

```python
def solve_part1(text: str) -> int:
    """Solve Part 1: Sum minimum presses across all machines."""
    machines = parse_input(text)
    total_presses = 0
    
    for machine in machines:
        # Build and solve system
        matrix = build_matrix(machine)
        matrix, pivot_cols = gaussian_elimination_gf2(matrix)
        min_presses = find_minimum_solution(matrix, pivot_cols)
        
        if min_presses == float('inf'):
            # Machine cannot be configured
            # Handle according to problem (likely won't happen)
            continue
        
        total_presses += min_presses
    
    return total_presses
```

### Part 2 Implementation Steps

#### Step 1: Parse for Part 2 (Reuse with Joltage)

```python
def parse_machine_part2(line: str) -> tuple:
    """
    Parse machine for Part 2 - extract joltage instead of diagram.
    """
    # Extract joltage requirements between { and }
    joltage_match = re.search(r'\{([0-9,]+)\}', line)
    joltage_str = joltage_match.group(1)
    targets = [int(x) for x in joltage_str.split(',')]
    
    # Extract button patterns (same as Part 1)
    button_matches = re.findall(r'\(([0-9,]+)\)', line)
    buttons = []
    for button_str in button_matches:
        indices = [int(x) for x in button_str.split(',')]
        buttons.append(indices)
    
    return targets, buttons
```

#### Step 2: Build Integer Matrix (Not GF(2))

```python
def build_matrix_part2(targets, buttons):
    """
    Build augmented matrix for Part 2 (integer arithmetic).
    Same structure as Part 1 but different interpretation.
    """
    num_counters = len(targets)
    num_buttons = len(buttons)
    
    # Build coefficient matrix A
    matrix = []
    for counter_idx in range(num_counters):
        row = [0] * (num_buttons + 1)
        
        # Check which buttons increment this counter
        for button_idx, button in enumerate(buttons):
            if counter_idx in button:
                row[button_idx] = 1
        
        # Augment with target value
        row[num_buttons] = targets[counter_idx]
        matrix.append(row)
    
    return matrix
```

#### Step 3: Try Matrix Inverse Method

```python
def solve_part2_inverse_method(targets, buttons):
    """
    Try to solve using matrix inverse (if square and invertible).
    Returns number of presses if successful, None otherwise.
    """
    num_counters = len(targets)
    num_buttons = len(buttons)
    
    # Only works if system is square
    if num_counters != num_buttons:
        return None
    
    # Build coefficient matrix
    A = [[0] * num_buttons for _ in range(num_counters)]
    for counter_idx in range(num_counters):
        for button_idx, button in enumerate(buttons):
            if counter_idx in button:
                A[counter_idx][button_idx] = 1
    
    # Try to solve using Gaussian elimination
    # (would need full implementation of integer matrix operations)
    # For AoC, can use numpy if allowed
    
    # Check if solution is non-negative integers
    # Return sum if valid, None otherwise
    
    return None  # Placeholder
```

#### Step 4: Gaussian Elimination (Integer Arithmetic)

```python
def gaussian_elimination_integer(matrix):
    """
    Gaussian elimination over integers (not GF(2)).
    Returns reduced matrix and pivot columns.
    """
    num_rows = len(matrix)
    if num_rows == 0:
        return matrix, []
    
    num_cols = len(matrix[0]) - 1
    
    pivot_row = 0
    pivot_cols = []
    
    for col in range(num_cols):
        # Find pivot (prefer 1 or -1 for simplicity)
        found_pivot = False
        for row in range(pivot_row, num_rows):
            if matrix[row][col] != 0:
                # Swap rows
                if row != pivot_row:
                    matrix[pivot_row], matrix[row] = matrix[row], matrix[pivot_row]
                found_pivot = True
                break
        
        if not found_pivot:
            continue
        
        pivot_cols.append(col)
        pivot_val = matrix[pivot_row][col]
        
        # Eliminate below (integer operations, not XOR)
        for row in range(pivot_row + 1, num_rows):
            if matrix[row][col] != 0:
                # Scale and subtract to eliminate
                # This gets complex with fractions - may need different approach
                pass
        
        pivot_row += 1
    
    return matrix, pivot_cols
```

#### Step 5: Bounded Search for Integer Solutions

```python
def find_minimum_integer_solution(matrix, pivot_cols):
    """
    Find minimum button presses for integer solution.
    Uses bounded search on free variables.
    """
    num_buttons = len(matrix[0]) - 1
    free_vars = [i for i in range(num_buttons) if i not in pivot_cols]
    
    # Determine bounds on free variables
    # Upper bound: could be sum of all targets (very loose)
    max_target = max(row[-1] for row in matrix)
    max_presses_per_button = max_target * 2  # Heuristic bound
    
    # Search for minimum solution
    min_presses = float('inf')
    
    # This can get expensive - need good bounds
    # Alternative: use LP relaxation to guide search
    
    return min_presses
```

#### Step 6: Solve Part 2

```python
def solve_part2(text: str) -> int:
    """
    Solve Part 2: Sum minimum presses for joltage configuration.
    """
    total_presses = 0
    
    for line in text.strip().split('\n'):
        if not line:
            continue
        
        # Parse for Part 2 (joltage targets)
        targets, buttons = parse_machine_part2(line)
        
        # Try matrix inverse method first (fast if it works)
        presses = solve_part2_inverse_method(targets, buttons)
        
        if presses is None:
            # Fall back to general method
            matrix = build_matrix_part2(targets, buttons)
            matrix, pivot_cols = gaussian_elimination_integer(matrix)
            presses = find_minimum_integer_solution(matrix, pivot_cols)
        
        if presses == float('inf'):
            # Unsolvable - skip or error
            continue
        
        total_presses += presses
    
    return total_presses
```

### Common Pitfalls

#### Part 1 Pitfalls

1. **Using regular arithmetic instead of mod 2**:
   - Wrong: `row[c] = row[c] + pivot_row[c]`
   - Right: `row[c] ^= pivot_row[c]`

2. **Forgetting to check for inconsistency**:
   - A row of all zeros with target = 1 means no solution

3. **Off-by-one in light indexing**:
   - Lights are 0-indexed
   - Button `(0)` toggles the first light (index 0)

4. **Not handling free variables**:
   - If system is underdetermined, need to enumerate solutions

5. **Incorrect matrix dimensions**:
   - Matrix should be (num_lights × num_buttons)
   - Augmented: (num_lights × (num_buttons + 1))

#### Part 2 Pitfalls

1. **Confusing Part 1 and Part 2 interpretations**:
   - Part 1: Use indicator diagram `[...]`, ignore joltage `{...}`
   - Part 2: Use joltage `{...}`, ignore indicator diagram `[...]`
   - Part 1: Toggle logic (XOR)
   - Part 2: Increment logic (addition)

2. **Using GF(2) arithmetic in Part 2**:
   - Wrong: `row[c] ^= pivot_row[c]` (that's Part 1)
   - Right: Regular integer arithmetic

3. **Not bounding the search space**:
   - Integer solutions can be arbitrarily large in theory
   - Need to establish upper bounds on button presses
   - Use problem constraints or LP relaxation to find bounds

4. **Assuming unique solutions**:
   - System may have multiple solutions
   - Need to find the one with minimum total presses

5. **Integer division issues**:
   - When doing Gaussian elimination with integers
   - May get fractions - need to handle carefully
   - Consider working with rational numbers or keeping denominators

6. **Not verifying solution correctness**:
   - After finding solution, verify it satisfies all equations
   - Check that all button press counts are non-negative integers

7. **Memory/time limits with unbounded search**:
   - Exponential search without bounds can hang
   - Always establish reasonable upper bounds

#### General Pitfalls (Both Parts)

1. **Parsing edge cases**:
   - Single-index buttons: `(3)` not `(3,)`
   - Multiple spaces between components
   - Empty lines in input

2. **Assuming square matrices**:
   - System may be over-determined (more equations than variables)
   - System may be under-determined (more variables than equations)

3. **Not handling unsolvable systems**:
   - Some configurations may be impossible
   - Return infinity or skip machine appropriately

4. **Integer overflow** (not in Python):
   - Not a concern with Python's arbitrary precision
   - But be aware if using other languages

### Edge Cases to Handle

#### Part 1 Edge Cases

1. **Single light machine**: `[#] (0) {1}`
   - Simplest case: need 1 press

2. **No buttons**: `[#] {1}`
   - Impossible to configure (no solution)

3. **All lights already off**: `[....] (0,1) (2,3) {1,2}`
   - Need 0 presses (already configured)

4. **Redundant buttons**: Multiple buttons toggle same lights
   - May increase free variables
   - Still solvable

5. **Unsolvable configuration**: Buttons cannot reach target state
   - Should handle gracefully (return infinity or skip)

6. **Many free variables**: 10+ free variables
   - Enumeration becomes expensive (2^10 = 1024)
   - May need optimization or pruning

7. **Large number of lights/buttons**: 50+ each
   - Matrix operations still tractable
   - Gaussian elimination is O(L × B²)

#### Part 2 Edge Cases

1. **Single counter, single button**: `[#] (0) {5}`
   - Simplest case: press button 5 times

2. **All counters already zero**: `[....] (0,1) (2,3) {0,0,0,0}`
   - Need 0 presses (already at target)

3. **Very large target values**: `[#] (0) {1000000}`
   - Need to press button 1,000,000 times
   - Make sure algorithm doesn't enumerate all possibilities

4. **Unsolvable with counters**: Button increments wrong counter
   - Example: `[#.] (1) {5,0}` - cannot increment counter 0
   - Should detect and handle

5. **System with many solutions**: Need to find minimum
   - Example: `[#] (0) (0) {5}` - two identical buttons
   - Minimum is 5 (use one button), not 10 (use both)

6. **Over-determined system**: More constraints than variables
   - May not have solution
   - Example: `[##] (0) {3,5}` - button increments counter 0 only
   - Cannot reach counter 1 = 5

7. **Under-determined system**: More variables than constraints
   - Many solutions, need minimum
   - Example: `[#] (0) (1) {5}` - both buttons increment same counter
   - Minimum: press one button 5 times, not both

8. **Fractional solutions in relaxation**: LP gives x = 2.5
   - Need to round/search for integer solution
   - LP solution may not be achievable with integers

9. **Negative intermediate values**: During Gaussian elimination
   - Need to ensure final solution has all non-negative values
   - May need to adjust approach

#### Performance Edge Cases (Both Parts)

1. **Many machines**: 1000+ machines
   - Process sequentially is fine
   - Each machine independent

2. **Dense button matrix**: Every button affects every light/counter
   - Matrix is full, no sparsity to exploit
   - Still manageable with small dimensions

3. **Sparse button matrix**: Most buttons affect 1-2 lights/counters
   - Could optimize with sparse matrix representation
   - Probably not necessary for AoC

4. **Pathological free variables**: 20+ free variables
   - 2^20 = 1,048,576 combinations
   - Need better bounds or pruning strategy

### Testing Strategy

Test in order of increasing complexity:

1. **Single machine examples** from puzzle
2. **Edge cases** (single light, all off, no solution)
3. **Full puzzle example** (expected: 7)
4. **Verify each machine** individually
5. **Performance test** with many buttons/lights

## Test Plan

### Part 1 Tests

#### Main Example (from puzzle)

**Input**:
```
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
```

**Expected Output**: `7`

**Breakdown**:
- Machine 1: 2 presses (as shown in puzzle)
- Machine 2: 3 presses (as shown in puzzle)
- Machine 3: 2 presses (as shown in puzzle)
- Total: 2 + 3 + 2 = 7

#### Machine 1 Detailed Trace

**Specification**: `[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1)`

**Target**: `[0, 1, 1, 0]` (lights 1 and 2 on)

**Buttons**:
- Button 0: `(3)` → toggles light 3
- Button 1: `(1,3)` → toggles lights 1, 3
- Button 2: `(2)` → toggles light 2
- Button 3: `(2,3)` → toggles lights 2, 3
- Button 4: `(0,2)` → toggles lights 0, 2
- Button 5: `(0,1)` → toggles lights 0, 1

**Matrix setup**:
```
       b0  b1  b2  b3  b4  b5 | target
Light0: 0   0   0   0   1   1 | 0
Light1: 0   1   0   0   0   1 | 1
Light2: 0   0   1   1   1   0 | 1
Light3: 1   1   0   1   0   0 | 0
```

**One valid solution**: Press buttons 4 and 5
- b4 = 1, b5 = 1, others = 0
- Total: 2 presses ✓

**Verification**:
```
Start:      [0, 0, 0, 0]
Press b4:   [1, 0, 1, 0]  (toggle lights 0, 2)
Press b5:   [0, 1, 1, 0]  (toggle lights 0, 1)
Result:     [0, 1, 1, 0] ✓ matches target
```

#### Simple Test Cases

**Test 1: Single Light, Single Button**

**Input**: `[#] (0) {1}`

**Expected**: `1`
- Need to press button 0 once to turn on light 0

**Test 2: Already Configured**

**Input**: `[....] (0,1) (2,3) {1,2}`

**Expected**: `0`
- All lights already off (target state)
- No presses needed

**Test 3: Two Lights, One Button Each**

**Input**: `[##] (0) (1) {1,1}`

**Expected**: `2`
- Press button 0 to turn on light 0
- Press button 1 to turn on light 1
- Total: 2 presses

**Test 4: Two Lights, One Button Toggles Both**

**Input**: `[##] (0,1) {1}`

**Expected**: `1`
- Press button 0 to toggle both lights
- Result: both on

**Test 5: Overlapping Buttons**

**Input**: `[#.] (0,1) (1) {1,1}`

**Expected**: `2`
- Press button 0: toggles 0,1 → `[1,1]`
- Press button 1: toggles 1 → `[1,0]`
- Total: 2 presses

Wait, let me recalculate:
- Need: light 0 on, light 1 off
- Option 1: Press button 0 only → `[1,1]` ✗
- Option 2: Press button 1 only → `[0,1]` ✗
- Option 3: Press both → `[1,0]` ✓
- Total: 2 presses

**Test 6: Multiple Solutions**

**Input**: `[#] (0) (0) {1,1}`

**Expected**: `1`
- Two identical buttons (both toggle light 0)
- Press either one (not both)
- Multiple solutions exist, minimum is 1

#### Edge Cases

**Edge 1: Unsolvable Configuration**

**Input**: `[#.] (1) {1}`

**Expected**: Unsolvable or infinity
- Button only toggles light 1
- Cannot turn on light 0
- No solution exists

**Edge 2: All Lights On**

**Input**: `[####] (0,1,2,3) {1}`

**Expected**: `1`
- One button toggles all lights
- Press once to turn all on

**Edge 3: Complex Interdependence**

**Input**: `[#.#.] (0,2) (1,3) (0,1) {1,2,3}`

**Expected**: `2`
- Press buttons (0,2) and (0,1)
- Toggles: 0,2 and 0,1 → lights 0,1,2 affected
- Result: `[1,0,1,0]` if correct combination

Let me work through:
- Target: `[1,0,1,0]`
- Button 0: toggles 0,2
- Button 1: toggles 1,3
- Button 2: toggles 0,1

Matrix:
```
       b0  b1  b2 | t
L0:     1   0   1 | 1
L1:     0   1   1 | 0
L2:     1   0   0 | 1
L3:     0   1   0 | 0
```

From L2: b0 = 1
From L3: b1 = 0
From L1: b2 = 0
From L0: b0 + b2 = 1 → 1 + 0 = 1 ✓

**Solution**: Press button 0 only → 1 press

Let me verify:
- Start: `[0,0,0,0]`
- Press b0: toggles 0,2 → `[1,0,1,0]` ✓

**Corrected Expected**: `1`

#### Validation Trace for Full Example

**Machine 1**: `[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1)`
- Minimum presses: **2** ✓

**Machine 2**: `[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4)`

**Target**: `[0,0,0,1,0]` (light 3 on)

**Solution from puzzle**: Press buttons (0,4), (0,1,2), and (1,2,3,4) = **3 presses**

**Verification**:
- Start: `[0,0,0,0,0]`
- Press button 2 (0,4): toggles 0,4 → `[1,0,0,0,1]`
- Press button 3 (0,1,2): toggles 0,1,2 → `[0,1,1,0,1]`
- Press button 4 (1,2,3,4): toggles 1,2,3,4 → `[0,0,0,1,0]` ✓

**Machine 3**: `[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2)`

**Target**: `[0,1,1,1,0,1]` (lights 1,2,3,5 on)

**Solution from puzzle**: Press buttons (0,3,4) and (0,1,2,4,5) = **2 presses**

**Verification**:
- Start: `[0,0,0,0,0,0]`
- Press button 1 (0,3,4): toggles 0,3,4 → `[1,0,0,1,1,0]`
- Press button 2 (0,1,2,4,5): toggles 0,1,2,4,5 → `[0,1,1,1,0,1]` ✓

**Total**: 2 + 3 + 2 = **7** ✓

### Part 2 Tests

Part 2 uses joltage requirements and increment logic instead of indicator lights and toggle logic.

#### Main Example (from puzzle)

**Input** (same machines, different interpretation):
```
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
```

**Expected Output**: `33`

**Breakdown**:
- Machine 1: 10 presses
- Machine 2: 12 presses
- Machine 3: 11 presses
- Total: 10 + 12 + 11 = 33

#### Machine 1 Part 2 Detailed Trace

**Specification**: `[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}`

**Part 2 Setup**:
- **Target joltage**: `{3,5,4,7}` → counters must reach [3, 5, 4, 7]
- **Ignore indicator diagram**: `[.##.]` not used in Part 2
- **Buttons** (increment mode):
  - Button 0 `(3)`: increments counter 3
  - Button 1 `(1,3)`: increments counters 1 and 3
  - Button 2 `(2)`: increments counter 2
  - Button 3 `(2,3)`: increments counters 2 and 3
  - Button 4 `(0,2)`: increments counters 0 and 2
  - Button 5 `(0,1)`: increments counters 0 and 1

**System of equations**:
```
Counter 0: x₄ + x₅ = 3
Counter 1: x₁ + x₅ = 5
Counter 2: x₂ + x₃ + x₄ = 4
Counter 3: x₀ + x₁ + x₃ = 7
```

**One valid solution** (from puzzle):
- Button 0 `(3)`: press 1 time → x₀ = 1
- Button 1 `(1,3)`: press 3 times → x₁ = 3
- Button 2 `(2)`: press 0 times → x₂ = 0
- Button 3 `(2,3)`: press 3 times → x₃ = 3
- Button 4 `(0,2)`: press 1 time → x₄ = 1
- Button 5 `(0,1)`: press 2 times → x₅ = 2

**Verification**:
```
Counter 0: x₄ + x₅ = 1 + 2 = 3 ✓
Counter 1: x₁ + x₅ = 3 + 2 = 5 ✓
Counter 2: x₂ + x₃ + x₄ = 0 + 3 + 1 = 4 ✓
Counter 3: x₀ + x₁ + x₃ = 1 + 3 + 3 = 7 ✓
```

**Total presses**: 1 + 3 + 0 + 3 + 1 + 2 = **10 presses** ✓

#### Machine 2 Part 2 Detailed Trace

**Specification**: `[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}`

**Part 2 Setup**:
- **Target joltage**: `{7,5,12,7,2}` → counters must reach [7, 5, 12, 7, 2]
- **Buttons** (increment mode):
  - Button 0 `(0,2,3,4)`: increments counters 0, 2, 3, 4
  - Button 1 `(2,3)`: increments counters 2, 3
  - Button 2 `(0,4)`: increments counters 0, 4
  - Button 3 `(0,1,2)`: increments counters 0, 1, 2
  - Button 4 `(1,2,3,4)`: increments counters 1, 2, 3, 4

**System of equations**:
```
Counter 0: x₀ + x₂ + x₃ = 7
Counter 1: x₃ + x₄ = 5
Counter 2: x₀ + x₁ + x₃ + x₄ = 12
Counter 3: x₀ + x₁ + x₄ = 7
Counter 4: x₀ + x₂ + x₄ = 2
```

**One valid solution** (from puzzle):
- Button 0 `(0,2,3,4)`: press 2 times → x₀ = 2
- Button 1 `(2,3)`: press 5 times → x₁ = 5
- Button 2 `(0,4)`: press 0 times → x₂ = 0
- Button 3 `(0,1,2)`: press 5 times → x₃ = 5
- Button 4 `(1,2,3,4)`: press 0 times → x₄ = 0

**Verification**:
```
Counter 0: x₀ + x₂ + x₃ = 2 + 0 + 5 = 7 ✓
Counter 1: x₃ + x₄ = 5 + 0 = 5 ✓
Counter 2: x₀ + x₁ + x₃ + x₄ = 2 + 5 + 5 + 0 = 12 ✓
Counter 3: x₀ + x₁ + x₄ = 2 + 5 + 0 = 7 ✓
Counter 4: x₀ + x₂ + x₄ = 2 + 0 + 0 = 2 ✓
```

**Total presses**: 2 + 5 + 0 + 5 + 0 = **12 presses** ✓

#### Machine 3 Part 2 Detailed Trace

**Specification**: `[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}`

**Part 2 Setup**:
- **Target joltage**: `{10,11,11,5,10,5}` → counters must reach [10, 11, 11, 5, 10, 5]
- **Buttons** (increment mode):
  - Button 0 `(0,1,2,3,4)`: increments counters 0, 1, 2, 3, 4
  - Button 1 `(0,3,4)`: increments counters 0, 3, 4
  - Button 2 `(0,1,2,4,5)`: increments counters 0, 1, 2, 4, 5
  - Button 3 `(1,2)`: increments counters 1, 2

**System of equations**:
```
Counter 0: x₀ + x₁ + x₂ = 10
Counter 1: x₀ + x₂ + x₃ = 11
Counter 2: x₀ + x₂ + x₃ = 11
Counter 3: x₀ + x₁ = 5
Counter 4: x₀ + x₁ + x₂ = 10
Counter 5: x₂ = 5
```

**One valid solution** (from puzzle):
- Button 0 `(0,1,2,3,4)`: press 5 times → x₀ = 5
- Button 1 `(0,3,4)`: press 0 times → x₁ = 0
- Button 2 `(0,1,2,4,5)`: press 5 times → x₂ = 5
- Button 3 `(1,2)`: press 1 time → x₃ = 1

**Verification**:
```
Counter 0: x₀ + x₁ + x₂ = 5 + 0 + 5 = 10 ✓
Counter 1: x₀ + x₂ + x₃ = 5 + 5 + 1 = 11 ✓
Counter 2: x₀ + x₂ + x₃ = 5 + 5 + 1 = 11 ✓
Counter 3: x₀ + x₁ = 5 + 0 = 5 ✓
Counter 4: x₀ + x₁ + x₂ = 5 + 0 + 5 = 10 ✓
Counter 5: x₂ = 5 ✓
```

**Total presses**: 5 + 0 + 5 + 1 = **11 presses** ✓

#### Simple Test Cases for Part 2

**Test 1: Single Counter, Single Button**

**Input**: `[#] (0) {5}`

**Expected**: `5`
- Counter 0 needs to reach 5
- Button 0 increments counter 0
- Press button 0 five times

**Test 2: All Counters Already Zero**

**Input**: `[....] (0,1) (2,3) {0,0,0,0}`

**Expected**: `0`
- All counters already at 0 (target state)
- No presses needed

**Test 3: Two Counters, Independent Buttons**

**Input**: `[##] (0) (1) {3,7}`

**Expected**: `10`
- Counter 0: press button 0 three times
- Counter 1: press button 1 seven times
- Total: 3 + 7 = 10

**Test 4: Two Counters, One Button Affects Both**

**Input**: `[##] (0,1) {5,5}`

**Expected**: `5`
- Button 0 increments both counters
- Press button 0 five times → both counters reach 5

**Test 5: System with Multiple Solutions**

**Input**: `[#] (0) (0) {5}`

**Expected**: `5`
- Two identical buttons (both increment counter 0)
- Could press first button 5 times, or second 5 times, or any combination
- Minimum is 5 (press one button 5 times, don't press the other)

#### Edge Cases for Part 2

**Edge 1: Unsolvable Configuration**

**Input**: `[#.] (1) {5,0}`

**Expected**: Unsolvable or infinity
- Counter 0 needs to reach 5
- Only button increments counter 1
- Cannot reach target for counter 0

**Edge 2: Large Target Values**

**Input**: `[#] (0) {1000}`

**Expected**: `1000`
- Need to increment counter 0 by 1000
- Press button 1000 times

**Edge 3: Over-determined System**

**Input**: `[##] (0,1) (0) (1) {5,7}`

**Expected**: Depends on solvability
- Counter 0: x₀ + x₁ = 5
- Counter 1: x₀ + x₂ = 7
- System: x₀ + x₁ = 5, x₁ = 5, x₂ = 7
- From equation 2: x₁ = 5
- From equation 1: x₀ = 0
- From equation 3: Check if consistent
- May or may not be solvable

**Edge 4: Efficient Solution vs. Naive**

**Input**: `[###] (0,1,2) (0) (1) (2) {5,5,5}`

**Expected**: `5`
- Button 0 increments all three counters
- Press button 0 five times → all counters at 5
- Better than pressing buttons 1, 2, 3 individually (15 presses)

## Complexity Analysis

### Part 1: Time Complexity

**Parsing**: O(M × (L + B)) where M = machines, L = lights, B = buttons

**For each machine**:
- Build matrix: O(L × B)
- Gaussian elimination: O(L × B²)
- Enumeration: O(2^F × B) where F = free variables
- **Typical F**: 0-5, so O(2^F) is manageable

**Overall**: O(M × (L × B² + 2^F × B))

**Typical values**:
- M = 100-1000 machines
- L = 5-20 lights per machine
- B = 5-30 buttons per machine
- F = 0-5 free variables

**Estimated runtime**: Under 1 second for typical inputs

### Part 2: Time Complexity

**Parsing**: O(M × (C + B)) where M = machines, C = counters, B = buttons

**For each machine** (depends on approach):

**Matrix inverse method** (if applicable):
- Build matrix: O(C × B)
- Matrix inversion: O(B³) if square
- Check validity: O(B)
- **Overall**: O(B³)

**Gaussian elimination + bounded search**:
- Build matrix: O(C × B)
- Gaussian elimination: O(C × B²)
- Determine bounds: O(B) to O(C)
- Search: O(2^F × B_max) where B_max = max button presses
- **Overall**: O(C × B² + 2^F × B_max)

**LP-based approach** (if using solver):
- Setup: O(C × B)
- Simplex: O(B³) typical, O(2^B) worst case
- Integer constraints: adds exponential factor
- **Overall**: Hard to analyze, depends on solver

**Practical complexity**: 
- For small problems (C, B ≤ 10): Very fast with any method
- For medium problems (C, B ≤ 30): Gaussian + bounded search works well
- For large problems: May need specialized techniques

### Space Complexity

**Part 1**: O(L × B) for the matrix per machine

**Part 2**: O(C × B) for the matrix per machine

**Overall**: O(max(L, C) × B) per machine, O(M) machines processed sequentially

**Memory efficient**: Even with L=C=20, B=30, matrix is only 600 integers

### Performance Characteristics

**Part 1**:
- **Best case**: Unique solution (F=0) → O(L × B²)
- **Average case**: Few free variables (F=1-3) → O(L × B² + 2^F × B)
- **Worst case**: Many free variables (F=10+) → May need optimization

**Part 2**:
- **Best case**: Square invertible matrix with integer solution → O(B³)
- **Average case**: Small free variables or tight bounds → O(C × B² + 2^F × B_max)
- **Worst case**: Large free variables and loose bounds → Expensive search

**Optimization strategies** if needed:
1. **Early termination**: If found solution with 0 presses, stop
2. **Pruning**: Skip combinations that already exceed current minimum
3. **Better enumeration**: Use backtracking instead of bit mask
4. **Parallel processing**: Solve machines independently in parallel
5. **Bound tightening**: Use LP relaxation to find tighter bounds

## Common AoC Patterns

This problem demonstrates:

1. **Hidden mathematical structure**: Disguised as a game, but it's linear algebra
2. **Modular arithmetic**: GF(2) operations throughout
3. **Optimization over constraints**: Find minimum subject to system of equations
4. **Parsing complexity**: Multi-component input format
5. **Matrix manipulation**: Gaussian elimination technique

**Similar AoC problems**:
- 2015 Day 6: Lights toggling (simpler, no optimization)
- 2018 Day 23: Linear optimization with constraints
- 2019 Day 22: Modular arithmetic with large numbers
- 2020 Day 20: Matrix operations and transformations

**Key insights rewarded**:
- Recognizing this as a linear algebra problem
- Understanding GF(2) arithmetic (XOR)
- Implementing Gaussian elimination correctly
- Handling free variables through enumeration

## Summary

**Day 10: Factory** is a two-part mathematical puzzle that demonstrates the difference between binary and integer linear systems:

### Part 1: Linear Algebra over GF(2)
- **State**: Binary (lights on/off)
- **Operations**: Toggle (XOR)
- **Mathematics**: Linear equations over Galois Field 2
- **Solution**: Gaussian elimination + enumeration
- **Key insight**: Pressing button twice = no effect

### Part 2: Integer Linear Programming
- **State**: Integer (counter values)
- **Operations**: Increment (addition)
- **Mathematics**: Integer linear programming
- **Solution**: Matrix methods + bounded search or LP-based
- **Key insight**: Buttons can be pressed multiple times

### Key Formulas

**Part 1**: For each light i (mod 2 arithmetic):
```
(Σ button_presses[j] where j toggles i) mod 2 = target[i]
```
Solve this system, minimize Σ button_presses[j], each press ∈ {0, 1}

**Part 2**: For each counter i (integer arithmetic):
```
Σ button_presses[j] where j increments i = target[i]
```
Solve this system, minimize Σ button_presses[j], each press ≥ 0

### Critical Insights

**Part 1**:
1. **Pressing twice = no effect**: Only need to consider 0 or 1 presses per button
2. **XOR arithmetic**: All operations are in GF(2) (use `^` in code)
3. **Multiple solutions**: System may be underdetermined, need to find minimum
4. **Matrix form**: Express as Ax = b (mod 2) and solve

**Part 2**:
1. **Different target**: Use joltage `{...}`, not diagram `[...]`
2. **Different operation**: Increment (+), not toggle (XOR)
3. **Unbounded solution space**: Need to establish bounds on button presses
4. **Integer constraints**: Solutions must be non-negative integers
5. **Matrix form**: Express as Ax = b (integers), x ≥ 0

### Implementation Checklist

**Part 1**:
- [ ] Parse input (indicator diagram, buttons, ignore joltage)
- [ ] Build augmented matrix [A | b]
- [ ] Implement Gaussian elimination over GF(2)
  - [ ] Use XOR for all arithmetic
  - [ ] Track pivot columns
  - [ ] Identify free variables
- [ ] Check for consistency (no 0=1 rows)
- [ ] If unique solution: extract and count presses
- [ ] If multiple solutions: enumerate to find minimum
- [ ] Sum across all machines
- [ ] Test with provided examples (expect 7)
- [ ] Verify each machine individually
- [ ] Handle edge cases (no solution, all off, etc.)

**Part 2**:
- [ ] Parse input (joltage requirements, buttons, ignore diagram)
- [ ] Build coefficient matrix [A | b] for integers
- [ ] Try matrix inverse method (if square and invertible)
- [ ] Implement Gaussian elimination over integers
- [ ] Determine bounds on free variables
- [ ] Search for minimum integer solution
- [ ] Verify solution is non-negative integers
- [ ] Sum across all machines
- [ ] Test with provided examples (expect 33)
- [ ] Verify each machine individually (10, 12, 11)
- [ ] Handle edge cases (unsolvable, large targets, etc.)

### Success Factors

**Part 1**:
- Correct recognition of GF(2) structure
- Proper Gaussian elimination implementation
- Handling multiple solutions through enumeration
- Careful parsing of input format
- Using XOR (^) for all mod 2 operations

**Part 2**:
- Recognizing the fundamental change from Part 1
- Understanding this is now Integer Linear Programming
- Proper parsing: use joltage, not diagram
- Regular integer arithmetic, not GF(2)
- Bounding the search space appropriately
- Verifying solutions are non-negative integers
- Finding efficient solution method (matrix inverse vs. search)

### Common Mistakes to Avoid

1. **Mixing up Part 1 and Part 2**:
   - Part 1 uses `[...]` (diagram), Part 2 uses `{...}` (joltage)
   - Part 1 uses XOR, Part 2 uses addition
   - Don't use GF(2) arithmetic in Part 2!

2. **Not handling different solution spaces**:
   - Part 1: Binary (0 or 1 presses)
   - Part 2: Non-negative integers (0, 1, 2, ...)

3. **Unbounded search in Part 2**:
   - Must establish upper bounds
   - Can't enumerate infinitely

4. **Assuming solutions exist**:
   - Check for inconsistent systems
   - Handle gracefully if unsolvable

### Recommended Approach

**Part 1**: 
1. ✅ Implement Gaussian elimination over GF(2)
2. ✅ Test thoroughly with examples
3. ✅ Ensure handles all edge cases
4. ✅ Optimize enumeration if needed
5. ✅ Submit Part 1

**Part 2**:
1. ✅ Understand the fundamental change (increment vs toggle)
2. ✅ Parse joltage instead of diagram
3. ✅ Try matrix inverse method first (quick)
4. ✅ Implement bounded search for general case
5. ✅ Verify with examples (10, 12, 11 → 33)
6. ✅ Test edge cases thoroughly
7. ✅ Submit Part 2

### Comparison Table

| Feature | Part 1 | Part 2 |
|---------|--------|--------|
| **Input used** | Diagram `[...]` | Joltage `{...}` |
| **Input ignored** | Joltage `{...}` | Diagram `[...]` |
| **Operation** | Toggle (XOR) | Increment (+) |
| **Arithmetic** | GF(2) (mod 2) | Integers |
| **Button presses** | 0 or 1 | 0, 1, 2, ... |
| **Problem type** | Linear algebra GF(2) | Integer Linear Programming |
| **Algorithm** | Gaussian + enumerate | Matrix inverse or LP |
| **Complexity** | O(L·B² + 2^F·B) | O(C·B² + search) |
| **Example total** | 7 (2+3+2) | 33 (10+12+11) |
