#!/usr/bin/env python

DEVICE_ID='ultrasonido-proyecto-iot'
PROJECT_ID='learned-pact-312010'
CLOUD_REGION='europe-west1'
REGISTRY_ID='proyecto-iot'
PRIVATE_KEY_FILE='./rsa_private.pem'
ALGORITHM='RS256'
CA_CERTS='roots.pem'
MQTT_BRIDGE_HOSTNAME='mqtt.googleapis.com'
dataset_id = 'ProyectoIoT'
table_id = 'TablaProyectoIoT'
table_colision_id = 'colisiones'
MQTT_BRIDGE_PORT=8883

from threading import Lock
from mqtt import *
import datetime
from google.cloud import bigquery
from google.oauth2 import service_account

# generate random integer values
from random import seed
from random import randint

import datetime

# seed random number generator
seed(1)

credentials = service_account.Credentials.from_service_account_file('./claveBigQuery.json')
periodo = 10
blue = (0, 0, 255)
yellow = (255, 255, 0)
lock = Lock()

latArray=[37.04993522029004,36.75028952696957,37.16911456446883,36.70791599215552,36.41849324241656,36.01335427600287,36.288488050052294,36.61356670359828,37.25991267788193,37.27308500947552]
lonArray=[-2.393221994503847,-3.0241147020982737,-3.604505605052509,-4.406015107604105,-5.14769287133916,-5.6086675125635,-6.06328759355543,-6.233218741365761,-7.233280696317195,-5.955097723743307]

dateFirstColision = datetime.datetime(2009,1,1,00,00,00)
chipIDLastColision={"418957": dateFirstColision, "455863": dateFirstColision, "377143": dateFirstColision} 

def subscribe(client: mqtt_client, topic):
    def on_message(client, userdata, msg):

        topic = msg.topic

        if "sensorDatos" in topic:
            client.mensajeQueLlega = eval(msg.payload)

    client.subscribe(topic)
    client.on_message = on_message

def comenzar():
    mqtt_topic = '/devices/{}/events'.format(DEVICE_ID)

    #Nos conectamos al cliente MQTT y a Google.
    clientshiftr = Mqtt.connect_mqtt("intercambiador")
    clientGoogle = bigquery.Client(credentials=credentials, project=PROJECT_ID)

    #Nos suscribimos al topic
    subscribe(clientshiftr, "sensorDatos")

    #Siempre
    while True:

        mensaje_recibido = False

        #Cuando llegue un valor, lo guardamos en 'mensajeQueLlega' y continuamos
        clientshiftr.loop_start()

        while not mensaje_recibido:
            if hasattr(clientshiftr, 'mensajeQueLlega'):
                mensaje_recibido = True
        clientshiftr.loop_stop()

        #Añadimos la fecha
        clientshiftr.mensajeQueLlega["date"]=datetime.datetime.now()

        #Obtenemos la tabla de bigQuery
        table_ref = clientGoogle.dataset(dataset_id).table(table_id)
        table = clientGoogle.get_table(table_ref)

         #Obtenemos la tabla de bigQuery
        table_colision_ref = clientGoogle.dataset(dataset_id).table(table_colision_id)
        table_colision = clientGoogle.get_table(table_colision_ref)


        #Preparamos la fila a insertar con los datos recibidos.
        rows = [
            {"chipID": clientshiftr.mensajeQueLlega["chipID"], "distancia": clientshiftr.mensajeQueLlega["distancia"],"tiempo": clientshiftr.mensajeQueLlega["tiempo"],"date": clientshiftr.mensajeQueLlega["date"]} 
        ]

        #Se inserta la fila en la tabla.
        errors = clientGoogle.insert_rows(table, rows)

        #Finalizamos inserción.
        if len(errors)==0:
            print("Enviado correctamente.")
        else:
            print(errors)

        #Si hay colision...
        if int(clientshiftr.mensajeQueLlega["distancia"]) < 5:
            
            lastColisionDate = datetime.datetime.strptime(str(clientshiftr.mensajeQueLlega["date"]), '%Y-%m-%d %H:%M:%S.%f')
            lastColisionDateRegistered = chipIDLastColision[clientshiftr.mensajeQueLlega["chipID"]]

            difference = lastColisionDate - lastColisionDateRegistered

            if difference.seconds >= 3600:

                chipIDLastColision[clientshiftr.mensajeQueLlega["chipID"]]=lastColisionDate

                number = randint(1, 10)

                rowsColision = [
                    {"chipID": clientshiftr.mensajeQueLlega["chipID"], "lat": latArray[number],"lon": lonArray[number],"namePhoto": "colision"+str(number)+".png","dateColision": clientshiftr.mensajeQueLlega["date"]} 
                ]

                #Se inserta la fila en la tabla.
                errorsColision = clientGoogle.insert_rows(table_colision, rowsColision)

                #Finalizamos inserción.
                if len(errorsColision)==0:
                    print("Enviado correctamente (Colision).")
                else:
                    print(errorsColision)

        #Borramos los datos recibidos.
        delattr(clientshiftr, "mensajeQueLlega")