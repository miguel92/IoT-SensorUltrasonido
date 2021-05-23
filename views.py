from flask import session

from models import *

def get_last_registry_view(chip_id):
    return get_last_registry(chip_id)


# Funcion para iniciar sesion
def iniciar_sesion(request):
    datos = {'correo': None, 'ok': False, 'msg': "", "logeado": False, "nombre": None}
    correo= request.form['correo']
    cont1 = request.form['pass']

    resultado = comprobar_usuario(correo, cont1)
    if resultado:
        datos['logeado'] = True
        session["usuario"] = correo
        session["nombre"] = resultado["userName"]
        session["rol"] = resultado["rol"]
        session["chipID"] = resultado["chipID"]
    else:
        datos['ok'] = False
        datos['msg'] = "Contraseña incorrecta"

    return datos


def lista_usuarios():
    return get_all_users()

def colision_usuario(chip_id):
    return get_colision_by_chip_id(chip_id)
