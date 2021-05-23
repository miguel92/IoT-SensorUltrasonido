import hashlib

from google.cloud import bigquery
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('./claveBigQuery.json')
project_id = 'learned-pact-312010'

client = bigquery.Client(credentials=credentials, project=project_id)

def get_last_registry(chip_id):

    QUERY = ('SELECT distancia, tiempo, date FROM `learned-pact-312010.ProyectoIoT.TablaProyectoIoT` WHERE chipID='+chip_id+' ORDER BY date DESC LIMIT 1')
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish
    datos = {}
    for row in rows:
        datos=row

    return datos


def comprobar_usuario(correo, password):
    hashed_password = hashlib.new("sha1", password.encode())
    QUERY = ('SELECT userName,email,chipID,rol FROM `learned-pact-312010.ProyectoIoT.users` WHERE email="' + correo + '" AND password="'+ hashed_password.hexdigest() +'" LIMIT 1')
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish
    resultado = False
    datos = {}

    for row in rows:
        datos = row

    return datos


def get_all_users():
    QUERY = ('SELECT userName,email,chipID FROM `learned-pact-312010.ProyectoIoT.users` WHERE rol !=0 Order by userName DESC')
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish
    return rows


def get_colision_by_chip_id(chip_id):
    QUERY = ('SELECT chipID, lat, lon, namePhoto, dateColision FROM `learned-pact-312010.ProyectoIoT.colisiones` WHERE chipID=' + chip_id + ' ORDER BY dateColision DESC LIMIT 1')
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish
    datos = {}
    for row in rows:
        datos = row

    return datos

def get_all_colisiones():
    QUERY = ('SELECT lat, lon, COUNT(*) AS numberColision FROM `learned-pact-312010.ProyectoIoT.colisiones` GROUP BY lat, lon')
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish
    return rows