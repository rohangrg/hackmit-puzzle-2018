from flask import (
    Flask,
    render_template,
    url_for,
    send_from_directory
)

import os
import hashing

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.png',
        mimetype='image/png'
    )

@app.route("/")
def index():
    return "There is nothing here. But a fun fact: snails are pretty cute."

@app.route("/u/<username>")
def serve_puzzle(username):
    filename = url_for('static',
                       filename=os.path.join('media/vids/',
                       hashing.user_to_file(username)))

    return render_template("index.html", username=username,
                                         answer_url=filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
