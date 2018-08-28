import requests
import json

from puzzle.optimal_solver import OptimalSolver as OS

PUZZLE_URL = 'http://localhost:3000/'
USERNAME = 'rahul01'

def get_value(n):
    params = {'user':USERNAME}
    r = requests.get(PUZZLE_URL + f'api/{n}', params=params)
    return r.json()

def post_move(move):
    params = {'user':USERNAME, 'move':move}
    r = requests.post(PUZZLE_URL + f'api/move', params=params)
    return r.json()

def node_to_pos(node, size):
    return (node//size, node%size)

def pos_to_node(pos, size):
    return (pos[0] * size + pos[1])

def make_move(curpos, newpos):
    change = (newpos[0]-curpos[0], newpos[1]-curpos[1])
    if change == (-1, 0):
        return 'up'
    elif change == (1, 0):
        return 'down'
    elif change == (0, -1):
        return 'left'
    elif change == (0, 1):
        return 'right'
    raise ValueError("Not a valid move.")

if __name__=='__main__':
    # Make User
    # requests.get(PUZZLE_URL + f'u/{USERNAME}')
    print("User Made")
    # Construct Solver
    adjList = get_value('map')['graph']
    T = get_value('time')['time']
    p = get_value('probability')['probability']
    opts = OS(adjList, T, p)
    print("Solver made")
    # Make moves
    size = int(len(adjList) ** 0.5)
    while(T > 0):
        print(f"Moves Remaining: {T}")
        curpos = get_value('position')
        curpos = (curpos['row'], curpos['col'])
        curnode = pos_to_node(curpos, size)
        newpos = node_to_pos(opts.move(curnode, T), size)
        print(f'{curpos} -> {newpos}')
        movestr = make_move(curpos, newpos)
        print(f'{curpos} -> {newpos}: {movestr}')
        move_response = post_move(movestr)
        T = get_value('time')['time']
        print(move_response.get('message', 'succesful move!'))
