'''

Middleware/Helper functions that are used in routing.

'''

import os
import random
import json

from hackgps.models import User, db

def logger(route, uid, params, values):
    '''Log data from the http requests.'''
    print('--------------------------------')
    print(f'{route} called by {uid}!')
    print(f'Params: {params}')
    print(f'DEBUG: {values}')
    print('--------------------------------')

def validate_user(uid):
    '''
    Make sure uid is valid.
    Return user if valid, None otherwise.
    '''
    try:
        user = User.query.filter_by(uuid=uid).first()
    except Exception as e:
        print(e)
        return None
    return user

def reset_user(root_path, user):
    '''Reset the user data.'''
    # Constant
    NUMGRAPHS = len(next(os.walk(os.path.join(root_path, 'static', 'graphs')))[2])
    
    # Calculate new values
    newmap = random.randint(0, NUMGRAPHS-1)
    with open(os.path.join(root_path, 'static', 'graphs', f'graph.{newmap:03}.json'), 'r') as f:
        data = json.load(f)
    
    # Set new values
    user.map = newmap
    user.row = 0
    user.col = 0
    user.prob = data['mistake']
    user.time = data['time']

    # Log changes
    logger('reset_user', user.uuid, {}, {'NUMGRAPHS':NUMGRAPHS, 'new map':user.map, 'mistake':data['mistake'], 'time':data['time'], 'path':os.path.join(root_path, 'static', 'graphs')})
    
    # Commit changes
    db.session.commit()

def get_map_data(mapnum, root_path):
    '''Returns a dict of the data from the graph.{mapnum}.json.'''
    with open(os.path.join(root_path, 'static', 'graphs', f'graph.{mapnum:03}.json'), 'r') as f:
        data = json.load(f)
    return data

def is_stuck(adjLists, pos):
    '''Determines whether pos is a dead end in the graph.'''
    node = _get_node(pos, len(adjLists))
    return not adjLists[node]

def check_move(adjLists, pos, dpos):
    '''Check whether dpos is a valid move from pos in the graph.'''
    # Check if move stays on graph
    if not ((0 <= pos[0] + dpos[0] < len(adjLists)) and (0 <= pos[1] + dpos[1] < len(adjLists))):
        return False
    # Check if move is valid according to adjLists
    curnode = _get_node(pos, len(adjLists))
    newnode = _get_node((pos[0]+dpos[0], pos[1]+dpos[1]), len(adjLists))
    return newnode in adjLists[curnode]

def get_random_move(adjLists, pos):
    '''Randomly choose and return a move from the current position in the graph.'''
    node = _get_node(pos, len(adjLists))
    newnode = random.choice(adjLists[node])
    return _get_pos(newnode, len(adjLists))

def _get_node(pos, size):
    '''Convert (row, col) position to node in graph.'''
    return int(pos[0] * (size ** 0.5) + pos[1])

def _get_pos(node, size):
    '''Convert node in graph to (row, col) position.'''
    return (int(node// (size ** 0.5)), int(node % (size ** 0.5) ))
