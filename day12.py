import numpy as np
from collections import defaultdict

presents = np.zeros((6, 3, 3))

with open('input_day12_1.txt') as f:
    lines = f.readlines()

i = 0
j = 0

for line in lines:
    line = line.strip()
    if line and (line[0] == '.' or line[0] == '#'):
        presents[i][j] = np.array([0 if ch == '.' else 1 for ch in line])
        j += 1
    if j == 3:
        j = 0
        i += 1
    
with open('input_day12_2.txt') as f:
    lines = f.readlines()

grids = {}

for idx, line in enumerate(lines):
    line = line.strip().split(' ')
    grids[idx] = (int(line[0][0:2]), int(line[0][3:5]), [int(ch) for ch in line[1:]])

sizes = [np.sum(presents[i]) for i in range(6)]
answer = 0
for idx, (w, h, quantities) in grids.items():
    total = sum(sizes[i] * quantities[i] for i in range(6))
    if total <= w * h:
        answer += 1
print("Part 1", answer)
print("Part 2: None ;)")

# Here is a proper checker for some arbitrary shapes, but ofc it's exponential

from pysat.solvers import Glucose3
from pysat.card import CardEnc, EncType

def get_all_orientations(shape):
    orientations = set()
    current = shape
    for _ in range(4):
        orientations.add(tuple(map(tuple, current)))
        orientations.add(tuple(map(tuple, np.flipud(current))))
        current = np.rot90(current)
    return [np.array(o) for o in orientations]

def can_fit_sat(w, h, quantities, presents):
    pieces = [(i, presents[i]) for i, qty in enumerate(quantities) for _ in range(qty)]
    if not pieces:
        return True
    
    total_needed = sum(np.sum(presents[i]) * qty for i, qty in enumerate(quantities))
    if total_needed > w * h:
        return False
    
    all_placements = []
    for piece_idx, (shape_idx, shape) in enumerate(pieces):
        placements = []
        for orient in get_all_orientations(shape):
            cells = [(r, c) for r in range(orient.shape[0]) 
                            for c in range(orient.shape[1]) if orient[r, c] == 1]
            oh, ow = orient.shape
            for r0 in range(h - oh + 1):
                for c0 in range(w - ow + 1):
                    placement = frozenset((r0 + dr, c0 + dc) for dr, dc in cells)
                    placements.append(placement)
        all_placements.append(placements)
    
    var_count = 0
    placement_vars = []
    for placements in all_placements:
        piece_vars = [var_count + i + 1 for i in range(len(placements))]
        var_count += len(placements)
        placement_vars.append(piece_vars)
    
    solver = Glucose3()
    
    for piece_vars in placement_vars:
        cnf = CardEnc.equals(lits=piece_vars, bound=1, top_id=var_count, encoding=EncType.seqcounter)
        var_count = cnf.nv
        for clause in cnf.clauses:
            solver.add_clause(clause)
    
    cell_to_vars = {}
    for piece_idx, placements in enumerate(all_placements):
        for pl_idx, placement in enumerate(placements):
            var = placement_vars[piece_idx][pl_idx]
            for cell in placement:
                if cell not in cell_to_vars:
                    cell_to_vars[cell] = []
                cell_to_vars[cell].append(var)
    
    for cell, vars_list in cell_to_vars.items():
        if len(vars_list) > 1:
            cnf = CardEnc.atmost(lits=vars_list, bound=1, top_id=var_count, encoding=EncType.seqcounter)
            var_count = cnf.nv
            for clause in cnf.clauses:
                solver.add_clause(clause)
    
    return solver.solve()

count = sum(1 for idx, (w, h, quantities) in grids.items() if can_fit_sat(w, h, quantities, presents))
print(count)