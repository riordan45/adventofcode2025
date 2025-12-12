import numpy as np

intervals = np.loadtxt('input_day5_part1.txt', dtype=str)
ids = np.loadtxt('input_day5_part2.txt', dtype=int)

intervals = [interval.split('-') for interval in intervals]
intervals = [[int(interval[0]), int(interval[1])] for interval in intervals]
 
# Part 1 

intervals.sort()
answer = 0
for id in ids:
    f = 0
    for interval in intervals:
        f = f or interval[0] <= id <= interval[1]
    answer += f

# Part 2

stack = [intervals[0]]
for i in range(1, len(intervals)):
    if stack[-1][1] >= intervals[i][1]:
        continue
    elif stack[-1][1] < intervals[i][0]:
        stack.append(intervals[i])
    else:
        stack[-1][1] = intervals[i][1]

answer2 = sum(interval[1] - interval[0] + 1 for interval in stack)
print('Part 1 and 2', answer, answer2)