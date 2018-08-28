from flask import Flask, render_template, jsonify, request
import pickle
import hashlib
import json
import numpy as np
from gerry_prod import *
from comhash import comhash
import os

with open('data.p', 'rb') as f:
    data = pickle.load(f)

PUZZLE_SECRET = os.environ.get('PUZZLE_SECRET', 'shhh')

N = 10
N_BLOCKS = N * N
N_DISTRICTS = 20
P_TRUE_VOTE = 0.6
neighbors = generate_neighbors(N)
FRIENDLY_NAMES = {
    'population_imbalance': 'District Population Imbalance',
    'ev_district_wins': 'Expected Party A Districts',
    'ev_efficiency_gap': 'Expected Efficiency Gap'
}

def token_to_index(token):
    m = hashlib.sha256()
    m.update(token.encode('utf8'))
    return int.from_bytes(m.digest(), 'big', signed=False) % len(data)

app = Flask(__name__)

@app.route('/')
def home():
    return 'Go back to command center'

class BadSubmissionError(Exception):
    pass

@app.route('/u/<token>/', methods=['GET', 'POST'])
def serve_puzzle(token):
    ind = token_to_index(token)
    puzzle = data[ind]
    sr = puzzle['submission_requirements']
    cv = {
        'ind': ind,
        'districts': '$ %d $' % sr['min_ev_district_wins'],
        'population': '$ %d \\times 10^{10}$' % (sr['max_population_imbalance'] / 1e10),
        'efficiency_gap': '$ %.3f $' % sr['min_ev_efficiency_gap']
    }
    submission_error_message = None
    answer = None
    if request.method == 'POST':
        try:
            try:
                submission = json.loads(request.form['json'])
            except json.decoder.JSONDecodeError:
                raise BadSubmissionError('Submission not JSON')

            if not isinstance(submission, list):
                raise BadSubmissionError('Submission was not a list')

            if len(submission) != N_DISTRICTS:
                raise BadSubmissionError('Submission has wrong number of rows')
                
            labeling = np.zeros((N_DISTRICTS, N_BLOCKS), dtype=np.bool)
            for j, district in enumerate(submission):
                if not isinstance(district, list):
                    raise BadSubmissionError('Submission row was not a list')
                for block in district:
                    if not isinstance(block, int) or block < 0 or block >= N_BLOCKS:
                        raise BadSubmissionError('Invalid block id found')
                    labeling[j, block] = 1

            if np.any(labeling.sum(axis=1) == 0):
                raise BadSubmissionError('Found district with zero blocks')

            if np.any(labeling.sum(axis=0) != 1):
                raise BadSubmissionError('Found block where # of assigned districts != 1')

            if not all_districts_connected(labeling, neighbors):
                raise BadSubmissionError('Not all districts were contigious')

            district_A = np.matmul(labeling, puzzle['voters'][0])
            district_B = np.matmul(labeling, puzzle['voters'][1])
            district_populations = district_A + district_B

            s = {
                'ev_district_wins': expected_A_wins(district_A, district_B, district_populations, P_TRUE_VOTE),
                'population_imbalance': population_imbalance(district_populations),
                'ev_efficiency_gap': efficiency_gap(district_A, district_B, district_populations, P_TRUE_VOTE)
            }

            bound_violations = []

            for k, v in sr.items():
                ks = k.split('_')
                var_name = '_'.join(ks[1:])
                if ks[0] == 'min':
                    if v > s[var_name]:
                        bound_violations.append(var_name)
                else:
                    if v < s[var_name]:
                        bound_violations.append(var_name)

            if len(bound_violations) != 0:
                raise BadSubmissionError('Violated bounds for %s' % ', '.join(list(map(FRIENDLY_NAMES.get, bound_violations))))

            answer = comhash(PUZZLE_SECRET, token)

        except BadSubmissionError as e:
            submission_error_message = str(e)
    return render_template('welcome.html', cv=cv, token=token, submission_error_message=submission_error_message, answer=answer)

@app.route('/u/<token>/voters.json')
def serve_voters(token):
    puzzle = data[token_to_index(token)]
    voters = puzzle['voters'].tolist()
    return jsonify({
        'voters_by_block': {
            'party_A': voters[0],
            'party_B': voters[1]
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
