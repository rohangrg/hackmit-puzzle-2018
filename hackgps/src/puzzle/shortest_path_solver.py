'''

Solution: Take the shortest path edge to the end node

'''

from .solver import Solver
from collections import deque

class SPSolver(Solver):    
    def __init__(self, _adj_list, _T, _p):
        super().__init__(_adj_list, _T, _p)

        reverse_list = [[] for _ in range(self.N)]
        for n in range(self.N):
            for v in self.adj_list[n]:
                reverse_list[v].append(n)
        
        self.dist = [1e10 for _ in range(self.N)]
        self.dist[self.N - 1] = 0
        queue = deque([self.N - 1])
        while len(queue) > 0:
            top = queue.popleft()
            for n in reverse_list[top]:
                if self.dist[n] > self.dist[top] + 1:
                    self.dist[n] = self.dist[top] + 1
                    queue.append(n)

        self.prob = [[0 for _ in range(self.T + 1)] for _ in range(self.N)]
        self.prob[self.N - 1][0] = 1
        for t in range(1, self.T + 1):
            self.prob[self.N - 1][t] = 1
            for n in range(self.N - 1):
                neigh_probs = [self.prob[neigh][t - 1] for neigh in self.adj_list[n]]
                if len(neigh_probs) == 0:
                    self.prob[n][t] = 0
                else:
                    self.prob[n][t] = self.prob[min(self.adj_list[n], key=lambda n: self.dist[n])][t - 1] * (1 - self.p) + sum(neigh_probs) / len(neigh_probs) * self.p
                 
        print(f"Shortest path solution: probability that node {self.N - 1} can be reached from node 0 in at most {self.T} timesteps is {self.prob[0][self.T]}")


    def move(self, cur, t_left):
        if cur < 0 or cur >= self.N or t_left <= 0 or t_left > self.T:
            raise ValueError('Invalid arguments to move method')
        if len(self.adj_list[cur]) == 0:
            return cur
        else:
            return min(self.adj_list[cur], key=lambda n: self.dist[n])
