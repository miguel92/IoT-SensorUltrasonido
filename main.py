import time
from flask import Flask, render_template, request, redirect, url_for, session
from bridge import *
import threading
from views import *
app = Flask(__name__)


@app.route('/')
def index():
    datos=get_last_registry_view('455863')
    return render_template('index.html',datos=datos)

if __name__ == '__main__':
    '''
    t = threading.Thread(target=comenzar, daemon=True)
    t.start()
    time.sleep(2)
    '''
    app.run(host='127.0.0.1', port=8080, debug=True)