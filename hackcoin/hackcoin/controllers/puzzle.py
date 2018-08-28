from hackcoin import app, redis_store
from hackcoin.utils import *
from hackcoin.config import PRICE, BLOCKRATE
from hackcoin.core.crypto import generate_keys
from hackcoin.core.blockchain import Blockchain, Block

import os
import json
import jsonpickle
import datetime

from flask import (
    send_from_directory,
    request,
    redirect,
    render_template
)

user_states = {}

def get_user_state(username):
    priv, pub = generate_keys()

    if redis_store.get(username) != None:
        decoded = jsonpickle.decode(redis_store.get(username))
        if 'created_at' not in decoded:
            decoded['created_at'] = datetime.datetime.now()
        if (datetime.datetime.now() - decoded['created_at']).total_seconds() > 2*3600:
            # Reset chain.
            priv = decoded['private']
            pub = decoded['public']
        else:
            return decoded
    
    current_state = {
        'public': pub,
        'private': priv,
        'donated': 0,
        'last_wallet': 0,
        'blockchain': Blockchain(),
        'last_added': datetime.datetime.now(),
        'created_at': datetime.datetime.now()
    }

    redis_store.set(username, jsonpickle.encode(current_state))

    return current_state

def commit_user_state(username, us):
    redis_store.set(username, jsonpickle.encode(us))

def create_bogus_block(bc):
    return Block(
        timestamp = datetime.datetime.now(),
        transactions = [],
        previous_hash = bc.head.hash_block()
    )

def simulate_server_mining(username):
    us = get_user_state(username)
    bc = us['blockchain']

    spent_duration = (datetime.datetime.now() - us['last_added']).total_seconds()
    num_blocks = int(round(BLOCKRATE * spent_duration))

    # Add blocks we would have mined since last call.

    # Cap simulation.
    num_blocks = min(num_blocks, 5)

    for _ in xrange(num_blocks):
        b = create_bogus_block(bc)
        bc.add_block(b, cheat=True)

    us['last_added'] = datetime.datetime.now()
    commit_user_state(username, us)

@app.route('/u/<username>/reset')
def reset_chain(username):
    us = get_user_state(username)
    us['blockchain'] = Blockchain()
    commit_user_state(username, us)

    return json.dumps({
        'success': True,
    })

@app.route('/u/<username>/store')
def render_store(username):
    us = get_user_state(username)
    answer = username_answer(username)
    return render_template('store.html', username=username, price=PRICE, us=us, answer=answer)

@app.route('/u/<username>/tracker/blockchain', methods=['GET', 'POST'])
def get_bc(username):
    simulate_server_mining(username)
    us = get_user_state(username)
    return jsonpickle.encode(us['blockchain'])

@app.route('/u/<username>/tracker/add', methods=['POST'])
def add_block(username):
    simulate_server_mining(username)

    # Get user blockchain.
    us = get_user_state(username)
    bc = us['blockchain']

    # Parse added block.
    d = request.get_data()
    js = json.loads(d)
    b = Block.from_json(js)

    success, message = bc.add_block(b, cheat=False)

    if success:
        # Update price we have.
        current_wallet = bc.get_wallet_amount(us['public'])
        if current_wallet - us['last_wallet'] > 0:
            us['donated'] += current_wallet - us['last_wallet']

        us['last_wallet'] = current_wallet

    print(success)
    commit_user_state(username, us)

    return json.dumps({
        'success': success,
        'message': message
    })
