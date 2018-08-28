'''

Base solver class.

'''

class Solver():
    def __init__(self, _adj_list, _T, _p):
        self.adj_list = _adj_list
        self.T = _T
        self.p = _p
        self.N = len(self.adj_list)

    def move(self, cur, t_left):
        """
        Assuming car is at node `cur` with `t_left` timesteps left,
        returns the optimal node to travel to occuring to self.prob
        """
        raise NotImplementedError('Move method not implemented')
