
from flask import Flask, render_template, request, redirect, url_for, session
from iot_core import *
import threading
app = Flask(__name__)

t = threading.Thread(target=main)
t.start()
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
    t.join()


