import numpy as np

# Part 1

arr = np.loadtxt('input_day4.txt', dtype=str)

m = len(arr)
n = len(arr[0])

def is_valid(i, j):
    return 0 <= i < m and 0 <= j < n
answer = 0
for i in range(m):
    for j in range(n):
        surround = 0
        if  arr[i][j] == '@':
            for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
                if is_valid(i + di, j + dj) and arr[i+di][j+dj] == '@':
                    surround += 1
            answer += surround < 4

# answer2 = 0
# change = 1
# arr = [[ch for ch in a] for a in arr]
# while change != 0:
#     change = 0
#     for i in range(m):
#         for j in range(n):
#             surround = 0
#             if  arr[i][j] == '@':
#                 for di, dj in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
#                     if is_valid(i + di, j + dj) and arr[i+di][j+dj] == '@':
#                         surround += 1
#                 if surround < 4:
#                     answer2 += 1
#                     arr[i][j] = '.'
#                     change = 1

# Part 2

from collections import deque
arr = np.loadtxt('input_day4.txt', dtype=str)

def solve_part2(arr):
    m, n = len(arr), len(arr[0])
    grid = [list(row) for row in arr]
    dirs = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]
    
    def count_neighbors(i, j):
        return sum(1 for di, dj in dirs 
                   if 0 <= i+di < m and 0 <= j+dj < n and grid[i+di][j+dj] == '@')
    
    queue = deque()
    for i in range(m):
        for j in range(n):
            if grid[i][j] == '@' and count_neighbors(i, j) < 4:
                queue.append((i, j))
    
    removed = 0
    while queue:
        i, j = queue.popleft()
        if grid[i][j] != '@': 
            continue
        if count_neighbors(i, j) >= 4: 
            continue
        grid[i][j] = '.'
        removed += 1
        
        for di, dj in dirs:
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == '@':
                if count_neighbors(ni, nj) < 4:
                    queue.append((ni, nj))
    
    return removed
print("Part 1 and 2", answer, solve_part2(arr))