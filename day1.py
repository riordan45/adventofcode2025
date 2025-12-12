import numpy as np

arr = np.loadtxt("input_day1.txt", dtype=str)

arr = np.array([int(ch[1:]) if ch[0] == 'R' else -int(ch[1:]) for ch in arr])
start = 50
answer = 0

# Part 1

for pos in arr:
    start += pos
    answer += start % 100 == 0
    start %= 100

print('Part 1', answer) 

# Part 2

start = 50
answer = 0

for pos in arr:
    start += pos
    if start == 0:
        answer += 1
        continue
    if start > 99:
        answer += start // 100
    elif start < 0:
        if start % 100 == 0:
            answer += abs(start) // 100 + 1
        else:
            answer += (-start + 100) // 100 - ((start - pos) == 0)
    start = start % 100

print('Part 2', answer)