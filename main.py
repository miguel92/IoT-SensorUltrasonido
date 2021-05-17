import time
from flask import Flask, render_template, request, redirect, url_for, session
from bridge import *
import threading
from views import *
import json
from bson import json_util

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lectura_datos', methods=['POST','GET'])
def lectura_datos():
    response = {"estado": False, "datos": None}
    datos = get_last_registry_view('455863')
    if datos is not None:
        response['estado'] = True
        response['datos'] = list(datos)
    response = json.dumps(response, default=json_util.default)
    return response

if __name__ == '__main__':
    '''
    t = threading.Thread(target=comenzar, daemon=True)
    t.start()
    time.sleep(2)
    '''
    app.run(host='127.0.0.1', port=8080, debug=True)