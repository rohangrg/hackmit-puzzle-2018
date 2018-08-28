from hackflix import app
from hackflix.utils import username_pick_range

import os
import json
import glob

from flask import (
    send_from_directory,
    request,
    redirect,
    render_template
)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.png',
        mimetype='image/png'
    )

@app.route('/')
def uhh():
    # Nothing here.
    return "Nothing here."

@app.route('/u/<username>/flix')
def index(username):
    # Find distractors.
    distractors = glob.glob(os.path.join('hackflix', 'static', 'vids', '*.mp4'))
    videos = [os.path.basename(x) for x in distractors]

    # Insert puzzle into position.
    puzzle_position = username_pick_range(username, len(distractors) + 1)
    videos.insert(puzzle_position, 'puzzle')

    # Display the home page.
    return render_template("home.html", username=username, videos=videos)
