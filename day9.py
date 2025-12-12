import numpy as np

# Part 1

coordinates = np.loadtxt('input_day9.txt', dtype=int, delimiter=',')
max_area = 0
m = len(coordinates)
for i in range(m-1):
    for j in range(i+1, m):
        aux = (abs(coordinates[i][0] - coordinates[j][0]) + 1) * (abs(coordinates[i][1] - coordinates[j][1]) + 1)
        max_area = max(max_area, aux)

print('Part 1', max_area)

# Part 2, Here you have to check if any line intersects any rectangle, but coding it up, holy moly

red_points = [(int(c[0]), int(c[1])) for c in coordinates]
n = len(red_points)

vertical_segs = {}
horizontal_segs = {}

for i in range(n):
    (x1, y1), (x2, y2) = red_points[i], red_points[(i + 1) % n]
    if x1 == x2:
        vertical_segs.setdefault(x1, []).append((min(y1, y2), max(y1, y2)))
    else:
        horizontal_segs.setdefault(y1, []).append((min(x1, x2), max(x1, x2)))

crossing_cache = {}

def compute_crossings(py):
    crossings = []
    for i in range(n):
        x1, y1 = red_points[i]
        x2, y2 = red_points[(i+1) % n]
        if y1 == y2:
            continue
        if (y1 > py) != (y2 > py):
            crossings.append(x1 + (x2 - x1) * (py - y1) / (y2 - y1))
    crossings.sort()
    return crossings

def point_inside(px, py):
    if py not in crossing_cache:
        crossing_cache[py] = compute_crossings(py)
    return sum(1 for x in crossing_cache[py] if px < x) % 2 == 1

def is_valid(min_x, max_x, min_y, max_y):
    cx, cy = (min_x + max_x) / 2.0, (min_y + max_y) / 2.0
    
    # Center must be inside
    if not point_inside(cx, cy):
        return False
    
    # No vertical polygon segment crosses horizontal rectangle edges
    for x, segs in vertical_segs.items():
        if x <= min_x or x >= max_x:
            continue
        for y_lo, y_hi in segs:
            if y_lo < min_y < y_hi or y_lo < max_y < y_hi:
                return False
    
    # No horizontal polygon segment crosses vertical rectangle edges
    for y, segs in horizontal_segs.items():
        if y <= min_y or y >= max_y:
            continue
        for x_lo, x_hi in segs:
            if x_lo < min_x < x_hi or x_lo < max_x < x_hi:
                return False
    
    # Check points just inside each edge are inside polygon
    eps = 0.5
    if not point_inside(min_x + eps, cy):
        return False
    if not point_inside(max_x - eps, cy):
        return False
    if not point_inside(cx, min_y + eps):
        return False
    if not point_inside(cx, max_y - eps):
        return False
    
    return True

max_area = 0
for i in range(n - 1):
    for j in range(i + 1, n):
        x1, y1 = red_points[i]
        x2, y2 = red_points[j]
        if x1 == x2 or y1 == y2:
            continue
        min_x, max_x = min(x1, x2), max(x1, x2)
        min_y, max_y = min(y1, y2), max(y1, y2)
        if is_valid(min_x, max_x, min_y, max_y):
            area = (max_x - min_x + 1) * (max_y - min_y + 1)
            if area > max_area:
                max_area = area

print('Part 2', max_area)

# Cleverer solutions

coordinates = np.loadtxt('input_day9.txt', dtype=int, delimiter=',')
points = [(int(c[0]), int(c[1])) for c in coordinates]
n = len(points)

def make_rect(p1, p2):
    """Returns (min_x, min_y, max_x, max_y)"""
    return (min(p1[0], p2[0]), min(p1[1], p2[1]), max(p1[0], p2[0]), max(p1[1], p2[1]))

def area(r):
    return (r[2] - r[0] + 1) * (r[3] - r[1] + 1)

def overlaps(r1, r2):
    """Check if two rectangles overlap (share interior points)"""
    return r1[0] < r2[2] and r1[2] > r2[0] and r1[1] < r2[3] and r1[3] > r2[1]

# All candidate rectangles from pairs of red points
rectangles = [make_rect(points[i], points[j]) for i in range(n-1) for j in range(i+1, n)]

# Part 1
print('Part 1', max(area(r) for r in rectangles))

# Part 2
# Lines are rectangles formed by consecutive red points (the green segments)
lines = [make_rect(points[i], points[(i+1) % n]) for i in range(n)]

# A rectangle is valid if it doesn't overlap with any of the boundary segments
print('Part 2', max(area(r) for r in rectangles if not any(overlaps(r, line) for line in lines)))