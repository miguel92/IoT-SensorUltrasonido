#!/usr/bin/env python

DEVICE_ID='ultrasonido-proyecto-iot'
PROJECT_ID='learned-pact-312010'
CLOUD_REGION='europe-west1'
REGISTRY_ID='proyecto-iot'
PRIVATE_KEY_FILE='./rsa_private.pem'
ALGORITHM='RS256'
CA_CERTS='roots.pem'
MQTT_BRIDGE_HOSTNAME='mqtt.googleapis.com'
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

periodo = 10
blue = (0, 0, 255)
yellow = (255, 255, 0)
lock = Lock()

def create_jwt(project_id, private_key_file, algorithm):

    token = {
            # The time that the token was issued at
            'iat': datetime.datetime.utcnow(),
            # The time the token expires.
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            # The audience field should always be set to the GCP project id.
            'aud': project_id
    }

    # Read the private key file.
    with open(private_key_file, 'r') as f:
        private_key = f.read()

    print('Creating JWT using {} from private key file {}'.format(
            algorithm, private_key_file))

    return jwt.encode(token, private_key, algorithm=algorithm)


def error_str(rc):
    """Convert a Paho error to a human readable string."""
    return '{}: {}'.format(rc, mqtt.error_string(rc))


def on_connect(unused_client, unused_userdata, unused_flags, rc):
    """Callback for when a device connects."""
    print('on_connect', mqtt.connack_string(rc))


def on_disconnect(unused_client, unused_userdata, rc):
    """Paho callback for when a device disconnects."""
    print('on_disconnect', error_str(rc))


def on_publish(unused_client, unused_userdata, unused_mid):
    """Paho callback when a message is sent to the broker."""
    print('on_publish')


def on_message(unused_client, unused_userdata, message):
    """Callback when the device receives a message on a subscription."""
    payload = str(message.payload,"utf-8")
    #print('Received message \'{}\' on topic \'{}\' with Qos {}'.format(
    #        payload, message.topic, str(message.qos)))
    if message.topic.endswith('commands'):
        global periodo

        dict_command=json.loads(payload)
        periodo = int(dict_command['periodo'])
        lock.acquire()
        lock.release()

def get_client(project_id, cloud_region, registry_id, device_id, private_key_file, algorithm, ca_certs, mqtt_bridge_hostname, mqtt_bridge_port):

    client = mqtt.Client(
            client_id=('projects/{}/locations/{}/registries/{}/devices/{}'
                       .format(
                               project_id,
                               cloud_region,
                               registry_id,
                               device_id)))

    # With Google Cloud IoT Core, the username field is ignored, and the
    # password field is used to transmit a JWT to authorize the device.
    client.username_pw_set(
            username='unused',
            password=create_jwt(
                    project_id, private_key_file, algorithm))

    # Enable SSL/TLS support.
    client.tls_set(ca_certs=ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

    # Register message callbacks. https://eclipse.org/paho/clients/python/docs/
    # describes additional callbacks that Paho supports. In this example, the
    # callbacks just print to standard out.
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Connect to the Google MQTT bridge.
    client.connect(mqtt_bridge_hostname, mqtt_bridge_port)

    # This is the topic that the device will receive configuration updates on.
    mqtt_config_topic = '/devices/{}/config'.format(device_id)

    # Subscribe to the config topic.
    client.subscribe(mqtt_config_topic, qos=1)

    # The topic that the device will receive commands on.
    mqtt_command_topic = '/devices/{}/commands/#'.format(device_id)

    # Subscribe to the commands topic, QoS 1 enables message acknowledgement.
    print('Subscribing to {}'.format(mqtt_command_topic))
    client.subscribe(mqtt_command_topic, qos=0)

    return client
    
def subscribe(client: mqtt_client, topic):
    def on_message(client, userdata, msg):

        topic = msg.topic
        
        if "sensorDatos" in topic:
            client.mensajeQueLlega = eval(msg.payload)
            
    client.subscribe(topic)
    client.on_message = on_message

def main():
    mqtt_topic = '/devices/{}/events'.format(DEVICE_ID)

    client = get_client(
        PROJECT_ID, CLOUD_REGION, REGISTRY_ID, DEVICE_ID,
        PRIVATE_KEY_FILE, ALGORITHM, CA_CERTS,
        MQTT_BRIDGE_HOSTNAME, MQTT_BRIDGE_PORT)

    client.loop_start()

    client2 = Mqtt.connect_mqtt("intercambiador")
    
    while True:

        mensaje_recibido = False

        client2.loop_start()
        subscribe(client2, "sensorDatos")
        while not mensaje_recibido:
            if hasattr(client2, 'mensajeQueLlega'):
                mensaje_recibido = True
        client2.loop_stop()

        client2.mensajeQueLlega["date"]=datetime.datetime.now()
        print(client2.mensajeQueLlega)

        json_data=json.dumps(client2.mensajeQueLlega,default=str)
        client.publish(mqtt_topic, json_data, qos=1)

        delattr(client2, "mensajeQueLlega")
        '''
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')

        print('Comienza insercion')
        client = bigquery.Client()
        dataset_id = 'ProyectoIoT'  # replace with your dataset ID
        table_id = 'TablaProyectoIoT'  # replace with your table ID
        table_ref = client.dataset(dataset_id).table(table_id)
        table = client.get_table(table_ref)

        response_dict = json.loads(pubsub_message)
        rows_to_insert = [response_dict]

        errors = client.insert_rows(table, rows_to_insert)  # API request
        print(errors)
        print('Termina insercion')
        '''

if __name__ == '__main__':
    main()
