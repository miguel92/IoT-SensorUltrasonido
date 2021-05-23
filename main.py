import time
from flask import Flask, render_template, request, redirect, url_for, session
from bridge import *
import threading
from views import *
import json
from bson import json_util

app = Flask(__name__)
app.secret_key = 'BQ2S5Idd4C'


@app.route('/')
def index():
    datos = {}

    if session.get('rol') == 0:
        datos = lista_usuarios()

    return render_template('index.html', datos=datos)


@app.route('/lectura_datos', methods=['POST','GET'])
def lectura_datos():
    response = {"estado": False, "datos": None}
    datos = None
    if request.form:
        chip_id = request.form['chipID']
        datos = get_last_registry_view(chip_id)

    if datos is not None:
        if len(datos) > 0:
            response['estado'] = True
            response['datos'] = list(datos)
    response = json.dumps(response, default=json_util.default)
    return response


@app.route('/iniciarSesion', methods=["GET", "POST"]) # Se llama a iniciar sesion en views.py
def iniciarSesion():
    datos = {}
    if request.form:
        datos = iniciar_sesion(request)

        if datos['logeado']:
            datos = {}

            if session.get('rol') == 0:
                datos = lista_usuarios()
            return render_template('index.html',datos=datos)

    return render_template('iniciar_sesion.html', datos=datos)


@app.route('/salir') #Se liberan las variables de sesion para cerrar la sesion del cliente
def salir():
    session.clear()

    return render_template('index.html')


if __name__ == '__main__':
    '''
    t = threading.Thread(target=comenzar, daemon=True)
    t.start()
    time.sleep(2)
    '''
    app.run(host='127.0.0.1', port=8080, debug=True)
