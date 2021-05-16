import time
from flask import Flask, render_template, request, redirect, url_for, session
from bridge import *
import threading
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    '''
    t = threading.Thread(target=comenzar, daemon=True)
    t.start()
    time.sleep(2)
    '''
    app.run(host='127.0.0.1', port=8080, debug=True)


