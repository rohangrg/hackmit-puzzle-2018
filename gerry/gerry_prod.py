import numpy as np
import scipy.stats

def population_imbalance(district_populations):
    return ((district_populations - district_populations.mean()) ** 2).sum()

def expected_A_wins(district_A, district_B, district_populations, p_true_vote):
    mu = (p_true_vote * district_A) + ((1 - p_true_vote) * district_B)
    sigma = np.sqrt(district_populations * p_true_vote * (1 - p_true_vote))
    P_A_win_district = 1 - scipy.stats.norm.cdf(district_populations/2, loc=mu, scale=sigma)
    return P_A_win_district.sum()

def efficiency_gap(district_A, district_B, district_populations, p_true_vote):
    # find the probability for each district
    mu = (p_true_vote * district_A) + ((1 - p_true_vote) * district_B)
    sigma = np.sqrt(district_populations * p_true_vote * (1 - p_true_vote))
    P_A_win_district = 1 - scipy.stats.norm.cdf(district_populations/2, loc=mu, scale=sigma)
    EV_wasted_votes_A = mu - district_populations*P_A_win_district/2
    EV_wasted_votes_B = district_populations/2.0 - EV_wasted_votes_A
    return (EV_wasted_votes_A - EV_wasted_votes_B).sum()/district_populations.sum()

def generate_neighbors(n):
    n_blocks = n * n

    neighbors = np.zeros(shape=(n_blocks, n_blocks), dtype=np.bool)
    for x in range(n):
        for y in range(n):
            i = n*y + x
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                xn, yn = x + dx, y + dy
                if xn < 0 or yn < 0 or xn >= n or yn >= n:
                    continue
                j = n*yn + xn
                neighbors[i, j] = 1
    neighbors.flags.writeable = False
    return neighbors

def all_districts_connected(labeling, neighbors):
    n_districts, n_blocks = labeling.shape
    
    visited = np.zeros(n_blocks, dtype=np.bool_)
    
    for d in range(n_districts):
        # check if district d is connected
        start_block = labeling[d, :].nonzero()[0][0]
        q = [start_block]
        visited[:] = 0
        visited[start_block] = 1
        while len(q) > 0:
            u = q.pop()
            for v in (neighbors[u, :] & labeling[d, :]).nonzero()[0]:
                if not visited[v]:
                    visited[v] = 1
                    q.append(v)
        if not (visited == labeling[d, :]).all():
            return False
    return True
