
import numpy as np
import cvxpy as cp
from scipy.optimize import milp, LinearConstraint, Bounds
from z3 import *
from collections import defaultdict
from itertools import combinations, product

with open('input_day10.txt') as f:
    lines = f.readlines()

machines = defaultdict(lambda: {'lights': [], 'buttons': [], 'joltage': []})


for idx, line in enumerate(lines):
    line = line.strip()
    
    lights_end = line.index(']')
    machines[idx]['lights'] = line[1:lights_end]
    
    joltage_start = line.index('{')
    joltage_str = line[joltage_start+1:-1]
    machines[idx]['joltage'] = [int(x) for x in joltage_str.split(',')]
    
    buttons_str = line[lights_end+1:joltage_start].strip()
    buttons = []
    for button in buttons_str.split(') '):
        button = button.strip('() ')
        if button:
            buttons.append(tuple(int(x) for x in button.split(',')))
    machines[idx]['buttons'] = buttons

answer = 0

for idx in range(len(machines)):
    min_ = float('inf')
    for i in range(1, len(machines[idx]['buttons']) + 1):
        schematic = ['.'] * len(machines[idx]['lights'])
        for combo in combinations(machines[idx]['buttons'], i):
            schematic = ['.'] * len(machines[idx]['lights'])
            for sequence in combo:
                for button in sequence:
                    schematic[button] = '#' if schematic[button] == '.' else '.'
            result = ''.join(schematic)
            if result == machines[idx]['lights']:

                min_ = min(min_, len(combo))

    answer += min_

z3_gf2_answer = 0

for idx in range(len(machines)):
    m = len(machines[idx]['lights'])
    n = len(machines[idx]['buttons'])
    
    # Build matrix A
    A = np.zeros((m, n), dtype=int)
    for j, button in enumerate(machines[idx]['buttons']):
        for pos in button:
            A[pos, j] = 1
    
    # Target vector
    b = np.array([1 if c == '#' else 0 for c in machines[idx]['lights']], dtype=int)
    
    # Z3 with binary variables
    x = [Int(f'x_{i}') for i in range(n)]
    s = Optimize()
    
    # x is 0 or 1
    for xi in x:
        s.add(Or(xi == 0, xi == 1))
    
    # Ax = b (mod 2)
    for i in range(m):
        s.add(sum(int(A[i][j]) * x[j] for j in range(n)) % 2 == int(b[i]))
    
    s.minimize(sum(x))
    
    if s.check() == sat:
        model = s.model()
        result = sum(model[xi].as_long() for xi in x)
        z3_gf2_answer += result

def solve_gf2_min(A, b):
    """Gaussian elimination over GF(2), returns minimum weight solution"""
    A = A.copy() % 2
    b = b.copy() % 2
    m, n = A.shape
    
    Ab = np.hstack([A, b.reshape(-1, 1)]).astype(int)
    
    pivot_cols = []
    row = 0
    
    for col in range(n):
        pivot = None
        for r in range(row, m):
            if Ab[r, col] == 1:
                pivot = r
                break
        
        if pivot is None:
            continue
        
        pivot_cols.append(col)
        Ab[[row, pivot]] = Ab[[pivot, row]]
        
        for r in range(m):
            if r != row and Ab[r, col] == 1:
                Ab[r] = (Ab[r] + Ab[row]) % 2
        
        row += 1
    
    # Free variables (not pivot columns)
    free_cols = [c for c in range(n) if c not in pivot_cols]
    
    # Try all combinations of free variables
    min_weight = float('inf')
    best_x = None
    
    for free_vals in product([0, 1], repeat=len(free_cols)):
        x = np.zeros(n, dtype=int)
        
        # Set free variables
        for i, col in enumerate(free_cols):
            x[col] = free_vals[i]
        
        # Back-substitute pivot variables
        for i in range(len(pivot_cols) - 1, -1, -1):
            col = pivot_cols[i]
            x[col] = Ab[i, -1]
            for j in range(col + 1, n):
                x[col] = (x[col] - Ab[i, j] * x[j]) % 2
        
        weight = np.sum(x)
        if weight < min_weight:
            min_weight = weight
            best_x = x.copy()
    
    return best_x

gaussian_elimination_answer = 0

for idx in range(len(machines)):
    m = len(machines[idx]['lights'])
    n = len(machines[idx]['buttons'])
    
    A = np.zeros((m, n), dtype=int)
    for j, button in enumerate(machines[idx]['buttons']):
        for pos in button:
            A[pos, j] = 1
    
    b = np.array([1 if c == '#' else 0 for c in machines[idx]['lights']], dtype=int)
    
    x = solve_gf2_min(A, b)
    gaussian_elimination_answer += np.sum(x)

print('Part 1', answer, z3_gf2_answer, gaussian_elimination_answer)

optimized_answer = 0
z3_answer = 0
answer = 0

for idx in range(len(machines)):
    min_ = float('inf')
    m = len(machines[idx]['joltage'])
    n = len(machines[idx]['buttons'])
    A = np.zeros((m, n))
    b = np.array(machines[idx]['joltage'])
    for i in range(m):
        for j, button in enumerate(machines[idx]['buttons']):
            if i in button:
                A[i][j] = 1

    # cvxpy
    x = cp.Variable(n, integer=True)
    objective = cp.Minimize(cp.sum(x))  # minimize sum of x
    constraints = [A @ x == b, x >= 0]
    prob = cp.Problem(objective, constraints)
    prob.solve()
    answer += np.sum(x.value)
    
    # scipy milp
    c = np.ones(n)
    constraints = LinearConstraint(A, b, b)  # Ax = b
    integrality = np.ones(n)  # all variables are integers
    bounds = Bounds(0, np.inf)
    result = milp(c, constraints=constraints, integrality=integrality, bounds=bounds)
    optimized_answer += np.sum(result.x)

    # z3
    z3_x = [Int(f'x_{i}') for i in range(n)]
    s = Optimize()  # Use Optimize() instead of Solver() for optimization
    
    for xi in z3_x:
        s.add(xi >= 0)
    
    for i in range(m):
        s.add(sum(int(A[i][j]) * z3_x[j] for j in range(n)) == int(b[i]))
    
    s.minimize(sum(z3_x))  # minimize sum of x
    
    if s.check() == sat:
        model = s.model()
        z3_result = [model[xi].as_long() for xi in z3_x]
        z3_answer += sum(z3_result)

print('Part 2')
print(f"cvxpy: {answer}")
print(f"milp: {optimized_answer}")
print(f"z3: {z3_answer}")