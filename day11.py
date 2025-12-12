from collections import defaultdict, deque
from functools import lru_cache

with open('input_day11.txt') as f:
    lines = f.readlines()

adj_list = defaultdict(list)

for line in lines:
    line = line.strip().split()
    adj_list[line[0][:3]] = line[1:]

queue = deque(['you'])
output = 'out'
answer = 0

while queue:
    node = queue.popleft()
    if node == output:
        answer += 1
    else:
        queue.extend(adj_list[node])

print('Part 1', answer)

# Part 2 - Top Down

queue = deque([('svr', 0)])
output = 'out'
answer = 0
aux = set()

@lru_cache(None)
def dfs(node, seen):
    if node == 'out':
        return seen > 1

    answer = 0
    for next_node in adj_list[node]:
        answer += dfs(next_node, seen + (node == 'dac' or node == 'fft'))
    return answer

print('Part 2 (top-down)', dfs('svr', 0))

# Part 2 - Bottom Up

# Build reverse graph and compute in-degrees
reverse_adj = defaultdict(list)
in_degree = defaultdict(int)
all_nodes = set(adj_list.keys())

for node in adj_list:
    for next_node in adj_list[node]:
        reverse_adj[next_node].append(node)
        in_degree[node] += 1
        all_nodes.add(next_node)

# Topological sort starting from 'out'
queue = deque([n for n in all_nodes if in_degree[n] == 0])
topo_order = []

while queue:
    node = queue.popleft()
    topo_order.append(node)
    for prev_node in reverse_adj[node]:
        in_degree[prev_node] -= 1
        if in_degree[prev_node] == 0:
            queue.append(prev_node)

# dp[node][seen] = number of paths from node to 'out' with 'seen' special nodes
dp = defaultdict(lambda: defaultdict(int))
dp['out'][0] = 1

# Process in topological order
for node in topo_order:
    if node == 'out':
        continue
    is_special = (node == 'dac' or node == 'fft')
    for next_node in adj_list[node]:
        for seen, count in dp[next_node].items():
            dp[node][seen + is_special] += count

# Sum paths where seen > 1
answer_bottom_up = sum(count for seen, count in dp['svr'].items() if seen > 1)
print('Part 2 (bottom-up)', answer_bottom_up)

# I thought this might work, but then it did not finish in a second
# Then i figured there might me cycles, but since they were not present for part 1
# that meant there were overlapping subproblems due to how you choose the paths,
# hence you do DP, again...

    # while queue:
    #     node, seen = queue.popleft()
    #     if node == 'dac':
    #         print(seen)
    #     # if (node, seen) in aux:
    #     #     print(node, seen)
    #     if node == output:
        
    #         answer += 1 if seen > 1 else 0
    #     else:
    #         if node == 'dac':
    #             print(seen)
    #         if ('dac', 1) in aux:
    #             print(aux)
    #         for next_node in adj_list[node]:
    #             queue.append((next_node, seen + (node == 'fft' or node == 'dac')))
    #             aux.add((next_node, seen + (node == 'fft' or node == 'dac')))
    #         print(len(aux))
    
# print('Part 2', answer)