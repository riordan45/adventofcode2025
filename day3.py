from functools import lru_cache
import numpy as np

# Part 1

arr = np.loadtxt('input_day3.txt', dtype=str)
answer = 0
for bank in arr:
    first = bank[0]
    second = '0'
    i = 1
    while i < len(bank):
        if i < len(bank) - 1 and first < bank[i]:
            first = bank[i]
            second = '0'
            i += 1
            continue
        second = max(second, bank[i])
        i += 1
    answer += int(first + second)

# Part 2

@lru_cache(None)
def dfs(bank_id, i, remaining, n):
    
    if i >= n or remaining == 0:
        return ''
    max_ = 0
    for dx in range(i, n):
        curr = arr[bank_id][dx] + dfs(bank_id, dx + 1, remaining - 1, n)
        max_ = max(max_, int(curr))
    
    return str(max_)

@lru_cache(None)
def dfs2(bank_id, i, remaining):
    if remaining == 0:
        return 0
    if i >= len(arr[bank_id]):
        return float('-inf')
    
    take = int(arr[bank_id][i]) * (10 ** (remaining - 1)) + dfs2(bank_id, i + 1, remaining - 1)
    
    skip = dfs2(bank_id, i + 1, remaining)
    
    return max(take, skip)

answer2 = 0
answer3 = 0
for idx in range(len(arr)):
    n = len(bank)
    answer2 += int(dfs(idx, 0, 12, n))
    answer3 += dfs2(idx, 0, 2) # ;)

print("Part 1 and 2 and whatever ;)", answer, answer2, answer3)
