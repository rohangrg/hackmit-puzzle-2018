'''

Solution: DP with greedy solution to choose path that maximizes probability of reaching end node in time

'''

from .solver import Solver

class OptimalSolver(Solver):
    def __init__(self, _adj_list, _T, _p):
        super().__init__(_adj_list, _T, _p)
        
        self.prob = [[0 for _ in range(self.T + 1)] for _ in range(self.N)]
        self.prob[self.N - 1][0] = 1
        for t in range(1, self.T + 1):
            self.prob[self.N - 1][t] = 1
            for n in range(self.N - 1):
                neigh_probs = [self.prob[neigh][t - 1] for neigh in self.adj_list[n]]
                if len(neigh_probs) == 0:
                    self.prob[n][t] = 0
                else:
                    self.prob[n][t] = max(neigh_probs) * (1 - self.p) + sum(neigh_probs) / len(neigh_probs) * self.p

        print(f"Optimal solution: probability that node {self.N - 1} can be reached from node 0 in at most {self.T} timesteps is {self.prob[0][self.T]}")


    def move(self, cur, t_left):
        if cur < 0 or cur >= self.N or t_left <= 0 or t_left > self.T:
            raise ValueError('Invalid arguments to move method')
        if len(self.adj_list[cur]) == 0:
            return cur
        else:
            return max(self.adj_list[cur], key=lambda n: self.prob[n][t_left - 1])
