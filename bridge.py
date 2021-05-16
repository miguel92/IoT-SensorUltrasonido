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
MQTT_BRIDGE_PORT=8883

import datetime
import os
import random
import ssl
import time

import jwt
import paho.mqtt.client as mqtt

import random
import json
import datetime

from threading import Lock
from mqtt import *

import base64
import json
import datetime
from google.cloud import bigquery
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('./claveBigQuery.json')
periodo = 10
blue = (0, 0, 255)
yellow = (255, 255, 0)
lock = Lock()

def subscribe(client: mqtt_client, topic):
    def on_message(client, userdata, msg):

        topic = msg.topic
        
        if "sensorDatos" in topic:
            client.mensajeQueLlega = eval(msg.payload)
            
    client.subscribe(topic)
    client.on_message = on_message

def main():
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

        #Preparamos la fila a insertar con los datos recibidos.
        rows = [
            {"chipID": clientshiftr.mensajeQueLlega["chipID"], "distancia": clientshiftr.mensajeQueLlega["distancia"],"tiempo": clientshiftr.mensajeQueLlega["tiempo"],"date": clientshiftr.mensajeQueLlega["date"]}  # works
        ]
        
        #Se inserta la fila en la tabla.
        errors = clientGoogle.insert_rows(table, rows)
        
        #Finalizamos inserción.
        if len(errors)==0:
            print("Enviado correctamente.")
        else: 
            print(errors)

        #Borramos los datos recibidos.
        delattr(clientshiftr, "mensajeQueLlega")

if __name__ == '__main__':
    main()
