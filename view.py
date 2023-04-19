from flask import Flask, Response, render_template, request
from static.python.polly_req import PollySession
import sys
import os

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/tips_and_tricks')
def tips_and_tricks():
    return render_template('tips_and_tricks.html')

@app.post('/polly')
def polly_resp():
    p = PollySession(request.json['ssml'])
    return p.getMP3Blob()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)