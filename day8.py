import numpy as np
import heapq

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.size = [1] * n
        self.count = n
        self.last = -1
        self.second_last = -1

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return
        # union by rank, this is purely for optimization
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        self.size[px] += self.size[py]
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.count -= 1
        if self.count == 1:
            self.last = x
            self.second_last = y

    def get_size(self, x):
        return self.size[self.find(x)]

coordinates = np.loadtxt('input_day8.txt', dtype=int, delimiter=',')

n = len(coordinates)

uf = UnionFind(n)

heap = []

# Part 1

for i in range(n):
    for j in range(i + 1, n):
        if i != j:
            distance = np.sum((coordinates[i] - coordinates[j]) ** 2)
            heapq.heappush(heap, (distance, i, j))

for _ in range(1000):
    distance, i, j = heapq.heappop(heap)
    uf.union(i, j)

print("Part 1", np.prod(heapq.nlargest(3, uf.size)))

# Part 2

for _ in range(n * n):
    distance, i, j = heapq.heappop(heap)
    uf.union(i, j)
    if uf.count == 1:
        break

print("Part 2", coordinates[uf.last][0] * coordinates[uf.second_last][0])


