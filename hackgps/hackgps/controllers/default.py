import os
import random
import json
from .comhash import comhash

from flask import (send_from_directory, request, render_template, abort, jsonify)

from hackgps.models import User, db
from hackgps.controllers.utils import *

MOVES = {
    'left': (0, -1),
    'up': (-1, 0),
    'right': (0, 1),
    'down': (1, 0)
}

def init_app_routes(app):
    '''Register all the app routes.'''
    if app:
        # Basic
        app.add_url_rule('/favicon.ico', 'favicon', favicon, methods=['GET'], defaults={'root_path':app.root_path})
        app.add_url_rule('/', 'index', index, methods=['GET'])
        # Puzzle View
        app.add_url_rule('/u/<uid>', 'puzzle', puzzle, methods=['GET'], defaults={'root_path':app.root_path})
        # API
        app.add_url_rule('/api/map', 'map', map, methods=['GET'], defaults={'root_path':app.root_path})
        app.add_url_rule('/api/position', 'position', position, methods=['GET'])
        app.add_url_rule('/api/time', 'time', timeLeft, methods=['GET'])
        app.add_url_rule('/api/probability', 'probability', probability, methods=['GET'])
        app.add_url_rule('/api/move', 'move', move, methods=['POST'], defaults={'root_path':app.root_path})
        app.add_url_rule('/api/reset', 'reset', reset, methods=['POST'], defaults={'root_path':app.root_path})

#--------------------------
# VIEW FUNCTIONS
#--------------------------
def favicon(root_path):
    return send_from_directory(
        os.path.join(root_path, 'static'),
        'favicon.ico',
        mimetype='image/x-icon'
    )

def index():
    return render_template("home.html")

def puzzle(uid, root_path):
    '''Return index.html if the user is valid.'''
    u = validate_user(uid)
    # logger('puzzle', uid, {}, {'u': u})
    if u is None:
        u = User(uid, 0, 0, 0, 0, 0)
        db.session.add(u)
        db.session.commit()
        reset_user(root_path, u)
    # print("New User")
    # print(u)
    return send_from_directory(
        os.path.join(root_path, 'templates'),
        'index.html'
    )

#--------------------------
# API GET FUNCTIONS
#--------------------------
def map(root_path):
    '''Return the adjList for the user.'''
    # Get Parameters
    uid = request.args.get('user')
    if uid is None:
        abort(400, 'Missing user.')

    # Validate user
    u = validate_user(uid)
    if u is None:
        # logger('map', uid, {}, {'mapNum': 'invalid user'}) # Log request
        abort(400, 'Invalid User.')

    # logger('map', uid, {}, {'mapNum': u.map}) # Log request
    data = get_map_data(u.map, root_path) # Get the adjList from file
    return jsonify({'graph': data['graph']})

def position():
    '''Return the current position of the user.'''
    # Get Parameters
    uid = request.args.get('user')
    if uid is None:
        abort(400, 'Missing user.')

    # logger('position', uid, {}, {}) # Log request

    # Validate user
    u = validate_user(uid)
    if u is None:
        abort(400, 'Invalid User.')

    return jsonify({ 'row': u.row, 'col': u.col })

def timeLeft():
    '''Return the number of moves the user has left.'''
    # Get Parameters
    uid = request.args.get('user')
    if uid is None:
        abort(400, 'Missing user.')

    # logger('timeLeft', uid, {}, {}) # Log request

    # Validate user
    u = validate_user(uid)
    if u is None:
        abort(400, 'Invalid User.')

    return jsonify({'time': u.time})

def probability():
    '''Return the probability of mistake for the user.'''
    # Get Parameters
    uid = request.args.get('user')
    if uid is None:
        abort(400, 'Missing user.')

    # logger('probability', uid, {}, {}) # Log request

    # Validate user
    u = validate_user(uid)
    if u is None:
        abort(400, 'Invalid user.')

    return jsonify({ 'probability': u.prob })

#--------------------------
# API POST FUNCTIONS
#--------------------------
def move(root_path):
    '''Request handler to allow the user to make a move.'''
    # Get Parameters
    uid = request.args.get('user')
    move = request.args.get('move')
    if uid is None or move is None:
        abort(400, 'Missing parameters.')

    # logger('move', uid, {'move':move}, {'MOVE':MOVES[move]}) # Log request

    # Validate user
    u = validate_user(uid)
    if u is None:
        abort(400, 'Invalid User.')

    data = get_map_data(u.map, root_path)

    # Check if we finished
    if u.row == (int(len(data['graph'])**0.5)-1) and u.col == (int(len(data['graph'])**0.5)-1):
        answer = comhash('hackgps-f91u3f190hf2f3', uid)
        return jsonify({'message': f"You win! The answer is {answer}", 'row': u.row, 'col': u.col})

    # Check number of moves remaining, redundant
    if u.time <= 0:
        return jsonify({'message':"You're out of moves, go ahead and reset!"})

    # Check if they are stuck
    if is_stuck(data['graph'], (u.row, u.col)):
        return jsonify({'message':"You are stuck, go ahead and reset!"})

    # Check if move is valid
    if not check_move(data['graph'], (u.row, u.col), MOVES[move]):
        return jsonify({'message':"Invalid move."})

    # Make move, subject to randomness
    if random.random() > data['mistake']:
        final_move = (u.row + MOVES[move][0], u.col + MOVES[move][1])
        final_message = "Phew! The message made it through - your driver made the correct turn."
    else:
        final_move = get_random_move(data['graph'], (u.row, u.col))
        final_message = "Connection failed! Your driver had to choose a random direction."
    u.row = final_move[0]
    u.col = final_move[1]
    u.time -= 1
    db.session.commit()

    # Check if we are out of time
    # if u.time == 0:
    #     return jsonify({'message':"You're out of moves, go ahead and reset!"})

    # Successful move, return position
    return jsonify({'message':final_message, 'row': u.row, 'col': u.col, 'time': u.time})

def reset(root_path):
    '''Request handler to reset the user's state.'''
    # Get Parameters
    uid = request.args.get('user')
    if uid is None:
        abort(400, 'Missing user')

    # logger('reset', uid, {}, {}) # Log request

    # Validate user
    u = validate_user(uid)
    if u is None:
        abort(400, 'Invalid User.')

    reset_user(root_path, u)
    return "Puzzle Reset!"
