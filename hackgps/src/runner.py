# TODO(rahul): Change the file writing format to separate graph, params (time, prob)
import random
import os
import json

from puzzle.optimal_solver import OptimalSolver as OS
from puzzle.shortest_path_solver import SPSolver as SPS

from puzzle import lib
from puzzle.generator import Generator

def run(solver, log=False):
    T = solver.T
    p = solver.p
    cur = 0
    while T > 0:
        if random.random() > p:
            nxt = solver.move(cur, T)
        else:
            if len(solver.adj_list[cur]) > 0:
                nxt = random.choice(solver.adj_list[cur])
            else:
                nxt = cur
        assert nxt in solver.adj_list[cur] or nxt == cur, 'Invalid move: attempting to move from {} to {}'.format(cur, nxt)
        cur = nxt

        T -= 1
        if cur == solver.N - 1:
            log and print('{} reached goal in {} timesteps'.format(solver.__class__.__name__, solver.T - T))
            return True

    log and print('{} did not reach goal within {} timesteps'.format(solver.__class__.__name__, solver.T))
    return False


def test(solver, num):
    assert num > 0
    success = 0
    for _ in range(num):
        if run(solver):
            success += 1
    print('{} had {}% ({} / {}) success rate'.format(solver.__class__.__name__, str(round(success / num, 3) * 100), str(success), str(num)))


def run_dummy_graph():
    with open('graph.txt', 'r') as input_file:
        adj_list = eval(input_file.readline())
        T = int(input_file.readline())
        p = float(input_file.readline())

        opts = OS(adj_list, T, p)
        sps = SPS(adj_list, T, p)

        test(opts, 100)
        test(sps, 100)


def main():
    generator = Generator(lib.WIDTH, lib.HEIGHT)
    files = generator.run(3)
    files_to_delete = []
    for filename in files:
        with open(os.path.join(lib.DIR, filename), 'r') as input_file:
            print(filename + ':')

            data = json.load(input_file)
            adj_list = data['graph']
            T = int(data['time'])
            p = data['mistake']

        goodps = []
        for p in [x*0.01 for x in range(30, 35)]:
            good = False
            opts = OS(adj_list, T, p)
            if opts.prob[0][opts.T] > 0.80:
                sps = SPS(adj_list, T, p)
                if sps.prob[0][sps.T] < 0.05:
                    # test(opts, 50)
                    # test(sps, 50)
                    good = True
            else:
                break
            if good:
                goodps.append(p)
                print('Good: {}'.format(p))
        if len(goodps) == 0:
            files_to_delete.append(filename)
        else:
            finalp = random.choice(goodps)
            with open(os.path.join(lib.DIR, filename), 'w') as output:
                toWrite = {
                    'graph': adj_list,
                    'time': T,
                    'mistake': finalp
                }
                json.dump(toWrite, output)
        print()

    for filename in files_to_delete:
        print(f"Deleting {filename}.")
        os.remove(os.path.join(lib.DIR, filename))

    num_graphs = 0
    curfiles = os.listdir(lib.DIR)
    curfiles.sort()
    for filename in curfiles:
        if filename.endswith('.json'):
            if filename != lib.filename(num_graphs):
                newname = lib.filename(num_graphs)
                print(f'{filename} -> {newname}')
                os.rename(os.path.join(lib.DIR, filename), os.path.join(lib.DIR, newname))
            num_graphs += 1
    return num_graphs


if __name__ == '__main__':
    num_made = 0
    while(num_made < 50):
        num_made = main()
