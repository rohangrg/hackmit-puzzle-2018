# HackAngel

This is a simple puzzle that's a play on the Arkangel episode from Blackmirror. It shows a video with scary things blurred out. The puzzle answer is also blurred out.

To uncover, you simply need to delete the HTML element that contains the blur video. Super easy level to teach people the mechanics.

<p align="center">
	<img src="https://github.com/techx/hackmit-puzzle-2018/raw/revalo-things/hackangel/screen.png" alt="screenshot" height="400" />
</p>

## Setup

Place the `config.py` file in the root. The exact secret for the current videos is:

```python
# Secret to generate deterministic answers.
SECRET = "shhh"

# Flask debug?
DEBUG = True

# Server port to run on.
PORT = 80
```

Place pre-rendered videos in `static/media/vids`

## Development

This is _almost_ a static puzzle, the files are served through flask to serve the right media to the right person. The only dependancy is Flask. For development, run,

```
python runserver.py
```