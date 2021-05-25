import time
from flask import Flask, render_template, request, redirect, url_for, session
from bridge import *
import threading
from views import *
import json
from bson import json_util
import folium

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
    response = {"estado": False, "datos": None, "colision": None}
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

@app.route('/mapaEstadistica') #Se liberan las variables de sesion para cerrar la sesion del cliente
def mapa_estadistica():
    map = folium.Map(
        left='20%',
        width=760,
        height=500,
        location=[37.6000000, -4.5000000],
        zoom_start=7
    )
    rows = get_all_colisiones_views()

    for row in rows:
        lat=row[0]
        lon=row[1]
        lat_lng = (lat, lon)
        numero_colisiones = row[2]
        html = folium.Html('<div style="text-align:center"><h4>Numero de colisiones: ' + str(numero_colisiones) + '</div>', script=True)
        folium.CircleMarker(
                location=lat_lng,
                radius=numero_colisiones*5,
                popup=folium.Popup(html, max_width=300, height=500),
                tooltip="Click aqui",
                fill=True,
                fill_color="crimson"
            ).add_to(map)

    return render_template('mapaEstadistica.html', map=map._repr_html_())


@app.route('/colisiones')
def colisiones():
    datos = {}

    if session['rol'] == 1:
        datos = colisiones_usuario(str(session['chipID']))
    else:
        datos = lista_usuarios()

    return render_template('colision.html', datos=datos)


@app.route('/lectura_colisiones', methods=['POST','GET'])
def lectura_colisiones():
    response = {"estado": False, "datos": None}
    datos = []
    if request.form:
        chip_id = request.form['chipID']
        rows = colisiones_usuario(str(chip_id))
        for row in rows:
            datos.append(list(row))
        response['estado'] = True
        response['datos'] = datos

    response = json.dumps(response, default=json_util.default)
    return response


if __name__ == '__main__':
    '''
    t = threading.Thread(target=comenzar, daemon=True)
    t.start()
    time.sleep(2)
    '''
    app.run(host='127.0.0.1', port=8080, debug=True)
