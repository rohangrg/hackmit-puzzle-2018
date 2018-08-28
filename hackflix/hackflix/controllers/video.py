from hackflix import app
from hackflix.config import DURATION
from hackflix.worker.models import Session, GenerateVideoRequest
from hackflix.utils import username_to_mp4
from sqlalchemy.exc import IntegrityError

import os

from flask import (
    send_from_directory,
    request,
    redirect,
    render_template,
    url_for,
    jsonify
)

@app.route('/u/<username>/flix/video/<id>.json')
def serve_video_info(username, id):
    if id == 'puzzle':
        # Get filename of puzzle video.
        fn, _, _, name = username_to_mp4(username)
        if os.path.exists(fn):
            return jsonify({
                'rendered': True,
                'url': url_for('static', filename='bin/%s' % name)
            })
        else:
            try:
                session = Session()
                session.add(GenerateVideoRequest(username=username))
                session.commit()
            except IntegrityError as e:
                pass
            finally:
                session.close()
            return jsonify({
                'rendered': False,
                'url': None
            })
    else:
        return jsonify({
            'rendered': True,
            'url': url_for('static', filename=('vids/' + id))
        })

@app.route('/u/<username>/flix/player/<id>')
def render_player(username, id):
    title = "None"
    if id == 'puzzle':
        title = "Adventures at HackMIT II"
    else:
        title = id.split('.')[0].replace('_', ' ')
    return render_template("player.html", username=username, id=id, title=title)
  
