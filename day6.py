import numpy as np

# Part 1

arr = np.loadtxt("input_day6.txt", dtype=str)
numbers = np.asarray(arr[:4], dtype=np.int64)
operations = arr[4]
answer = []
for idx, operation in enumerate(operations):
    answer.append(numbers[:, idx].prod() if operation == '*' else numbers[:, idx].sum())
answer = np.array(answer)


print("Part 1", sum(answer))

# Part 2

numbers = []
col = []
with open('input_day6.txt') as f:
    lines = iter(f)
    for line1, line2, line3, line4 in zip(lines, lines, lines, lines):
        for i in range(len(line1.rstrip('\n'))):
            col_char1 = line1[i]
            col_char2 = line2[i]
            col_char3 = line3[i]
            col_char4 = line4[i]
            
            no = f"{col_char1}{col_char2}{col_char3}{col_char4}"
            if col_char4 == col_char3 == col_char2 == col_char1 == " ":
                numbers.append(col)
                col = []
            else:
                col.append(int(no))
numbers.append(col)
for idx, operation in enumerate(operations):
    numbers[idx] += (4 - len(numbers[idx])) * [1 if operation == "*" else 0]
numbers = np.array(numbers)
answer = []
for idx, operation in enumerate(operations):
    answer.append(numbers[idx, :].prod() if operation == '*' else numbers[idx, :].sum())
answer = np.array(answer)
print("Part 2", sum(answer))
