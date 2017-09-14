import os
import time
from time import sleep
import sys
import json
import select
import serial
import paho.mqtt.client as mqtt
from XBee import xbeeNode
import XBee

THINGSBOARD_HOST = '172.25.224.84'
ACCESS_TOKEN = 'sXEes3EvtyUZJkreuRCb'

XBEE_R_W = 0
BUFFER = 1
PUBLISH = 2
STATE = XBEE_R_W

inputs = [xbeeNode]
outputs = []
exceptions = []

dataHandling = XBee.XBeeHandler()
# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL = 2
fsrValue = 0
sensor_data = {'fsr': 0}
next_reading = time.time() 
client = mqtt.Client()
# Set access token
client.username_pw_set(ACCESS_TOKEN)
# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)
client.loop_start()


try:
    while True:
        if STATE == XBEE_R_W:
            STATE = BUFFER
            readable, writable, exceptional = select.select(inputs, outputs, inputs)
            for rData in readable:
                #handle recive data
                # handle_data(rData)
                STATE = XBEE_R_W
                dataRecived = rData.readline()
        elif STATE == BUFFER:
            STATE = PUBLISH
            pass
        elif STATE == PUBLISH:
            STATE = XBEE_R_W
            pass
except KeyboardInterrupt:
    pass




# try:
#     while True:
#         # humidity,temperature = dht.read_retry(dht.DHT22, 4)
#         fsrValue += 1
#         print("FSR VALUE: {}".format(fsrValue))
#         sensor_data['fsr'] = fsrValue
#         sleep(2);

#         # Sending humidity and temperature data to ThingsBoard
#         client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)

#         next_reading += INTERVAL
#         sleep_time = next_reading-time.time()
#         if sleep_time > 0:
#             time.sleep(sleep_time)
# except KeyboardInterrupt:
#     pass

client.loop_stop()
client.disconnect()
