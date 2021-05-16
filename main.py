
from flask import Flask, render_template, request, redirect, url_for, session
from iot_core import *
import threading
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

#v0.1
if __name__ == '__main__':
    t = threading.Thread(target=main, daemon=True)
    t.start()
    app.run(host='127.0.0.1', port=8080, debug=True)

