from hackflix import app
from hackflix.utils import gen_uuid
from hackflix.worker.models import Session, VerifySolutionRequest
import os

from flask import (
    abort,
    send_from_directory,
    request,
    redirect,
    render_template,
    url_for
)

# TODO Review for security.
@app.route('/u/<username>', methods=['GET', 'POST'])
def render_hackbay(username):
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('hackbay.html', message="File was empty :/", username=username)
          
        file = request.files['file']
        if file and file.filename.endswith('.mp4'):
            # Save file.
            user_file = gen_uuid() + '.mp4'
            user_file_path = os.path.join(app.config['UPLOAD_FOLDER'], user_file)
            file.save(user_file_path)

            session = Session()
            r = VerifySolutionRequest(username=username, upload_filename=user_file_path)
            session.add(r)
            session.commit()
            verify_id = r.id
            session.close()
            return redirect(url_for('render_verify', username=username, verify_id=verify_id))
        else:
            return render_template('hackbay.html', message="File needs to be mp4.", username=username)
    return render_template('hackbay.html', username=username)

@app.route('/u/<username>/verify/<verify_id>')
def render_verify(username, verify_id):
    session = Session()
    verify_result = session.query(VerifySolutionRequest).filter(VerifySolutionRequest.id == verify_id, VerifySolutionRequest.username == username).first()
    session.close()
    if verify_result == None:
        return abort(404)
    result = {
            'message': "Queued. Please wait",
            'sender': "Sad HackMirror servers"
    }
    should_reload = True
    if verify_result.result:
        result = verify_result.result
        should_reload = False
    return render_template('hackbay.html', result=result, username=username, should_reload=should_reload)

