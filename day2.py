import numpy as np

# Part 1

arr = np.loadtxt('input_day2.txt', dtype=str, delimiter=',')
# arr = np.asarray(np.array([a.split('-') for a in arr]), dtype=np.int64)
arr = np.array([a.split('-') for a in arr])
answer = 0
limit = 2 ** 63 - 1
for interval in arr:
    start = interval[0]
    end = interval[1]
    lstart = len(start)
    lend = len(end)
    start = int(start)
    end = int(end)
    if lstart % 2 == 1 and lstart == lend:
        continue
    if lstart % 2 == 1:
        power = (lstart + 1) // 2 - 1
        for trial in range(10 ** power, limit):
            aux = trial * 10 ** (len(str(trial))) + trial
            if aux > end:
                break
            if aux >= start and aux <= end:
                answer += aux
    if lstart % 2 == 0:
        power = (lstart) // 2 - 1
        for trial in range(10 ** power, limit):
            aux = trial * 10 ** (len(str(trial))) + trial
            if aux > end:
                break
            if aux >= start and aux <= end:
                answer += aux
print('Part 1', answer)

# Part 2 

answer = 0
arr = np.loadtxt('input_day2.txt', dtype=str, delimiter=',')

def is_repeating_number(num):
    num_str = str(num)
    for i in range(1, len(num_str) // 2 + 1):
        seq = num_str[:i]
        if seq * (len(num_str) // len(seq)) == num_str:
            return True
    return False

for interval in arr:
    start, end = map(int, interval.split('-'))
    
    for num in range(start, end + 1):
        if is_repeating_number(num):
            answer += num
# for interval in arr:
#     start = interval[0]
#     end = interval[1]
#     lstart = len(start)
#     lend = len(end)
#     start = int(start)
#     end = int(end)
#     for trial in range(1, limit):
#         for repeat in range(2, 1000000):
#             aux = trial
#             while repeat - 1 > 0:
#                 aux = aux * 10 ** (len(str(trial))) + trial
#                 repeat -= 1
            
#             if aux > end:
#                 break
#             if aux >= start and aux <= end:
#                 answer += aux
                # print(start, aux, end)
# print(arr)
print('Part 2', answer)
# print(len(arr))