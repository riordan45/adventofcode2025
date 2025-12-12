from functools import lru_cache
import numpy as np
from collections import deque

# Part 1

arr = np.loadtxt('input_day7.txt', dtype=str)
arr = np.array([list(row) for row in arr])

m = len(arr)
n = len(arr[1])

queue = deque([])
for i in range(m):
    if arr[0][i] == 'S':
        idx = i
        break
queue.append((1, idx))
arr[1][idx] = "|"

# for i in range(m):
#     for j in range(n - 1):
#         if arr[i][j] == arr[i][j+1] == '^':
#             print(i, j)

answer = 0
while queue:
    row, idx = queue.popleft()
    if row == m - 1:
        continue
    if arr[row + 1][idx] == ".":
        arr[row + 1][idx] = "|"
        queue.append((row + 1, idx))
    
    if arr[row + 1][idx] == "^":
        arr[row + 1][idx + 1] = "|"
        arr[row + 1][idx - 1] = "|"
        queue.append((row + 1, idx - 1))
        queue.append((row + 1, idx + 1))
        answer += 1

print("Part 1", answer)

# Part 2

arr = np.loadtxt('input_day7.txt', dtype=str)
arr = np.array([list(row) for row in arr])

for i in range(m):
    if arr[0][i] == 'S':
        idx = i
        break
dp = [[0 for _ in range(n)] for _ in range(m)]
dp[1][idx] = 1
for i in range(m):
    for j in range(n):
        if arr[i][j] == "^":
            dp[i][j-1] += dp[i-1][j]
            dp[i][j+1] += dp[i-1][j]
        else:
            dp[i][j] += dp[i-1][j]
print("Part 2", np.sum(dp[-1]))

arr_tuple = tuple(tuple(row) for row in arr)

@lru_cache(maxsize=None)
def count_paths(row, col, arr_tuple):
    if row == 0:
        return 1 if col == idx else 0
    
    paths = 0
    # Check if we came from above
    if arr_tuple[row][col] == "^":
        # We must have come from directly above
        paths = count_paths(row - 1, col, arr_tuple)
    else:
        # Check if we came straight down
        if arr_tuple[row - 1][col] != "^":
            paths += count_paths(row - 1, col, arr_tuple)
        # Check if we came from a split
        if col > 0 and arr_tuple[row - 1][col - 1] == "^":
            paths += count_paths(row - 1, col - 1, arr_tuple)
        if col < n - 1 and arr_tuple[row - 1][col + 1] == "^":
            paths += count_paths(row - 1, col + 1, arr_tuple)
    
    return paths

total = sum(count_paths(m - 1, j, arr_tuple) for j in range(n))
print("Part 2", total)