"""
dispatch_async.py
By Paul Malmsten, 2010
pmalmsten@gmail.com
This example continuously reads the serial port and dispatches packets
which arrive to appropriate methods for processing in a separate thread.
"""

from xbee.thread import XBee, ZigBee
from xbee.helpers.dispatch import Dispatch
import serial
import struct
import paho.mqtt.client as mqtt
import time
import json

# Create handlers for various packet types


def status_handler(name, packet):
    print("Status Update - Status is now: {}".format(packet['status']))
    # sensor_data_1['fsrN1'] = 4000
    # client.publish('v1/devices/me/telemetry', json.dumps(sensor_data_1), 1)
    # sensor_data_2['fsrN2'] = 2000
    # client_2.publish('v1/devices/me/telemetry', json.dumps(sensor_data_2), 1)


def io_sample_handler(name, packet):
    print("Samples Received: {}".format(packet['samples']))


def receive_packet(name, packet):
    sensor_data_1 = {'fsrN1': 0}
    sensor_data_2 = {'fsrN2': 0}
    print(packet)
    rf_data = struct.unpack('>BBBHB', packet['rf_data'])
    data_type = chr(rf_data[0])
    data_node = chr(rf_data[1])
    data = rf_data[3]
    if data_type == 'f':
        if data_node == '1':
            sensor_data_1['fsrN1'] = data
            print(data_type + ' ' + data_node + ' ' + '{}'.format(sensor_data_1['fsrN1']))
            client.publish('v1/devices/me/telemetry', json.dumps(sensor_data_1), 1)
        elif data_node == '2':
            sensor_data_2['fsrN2'] = data
            print(data_type + ' ' + data_node + ' ' + '{}'.format(sensor_data_2['fsrN2']))
            client.publish('v1/devices/me/telemetry', json.dumps(sensor_data_2), 1)
    # print("rf_data: {}".format(packet['rf_data']))
    # sensor_data_1['fsrN1'] = int.from_bytes(packet['rf_data'], 'big')
    # print("sensor_data: {}".format(sensor_data_1))
    # time.sleep(2)
    # Sending humidity and temperature data to ThingsBoard
    # client.publish('v1/devices/me/telemetry', json.dumps(sensor_data_1), 1)

    # next_reading += INTERVAL
    # sleep_time = next_reading - time.time()
    # if sleep_time > 0:
    #     time.sleep(sleep_time)
    # pass

THINGSBOARD_HOST = '172.25.224.84'
ACCESS_TOKEN_1 = 'sXEes3EvtyUZJkreuRCb'
ACCESS_TOKEN_2 = 'Y1PBluwmhe3UfLLPSAg7'
# ACCESS_TOKEN = '7d92fc20-a1ca-11e7-9e43-df630275a618'
# PORT = '/dev/ttyUSB0'
PORT = 'COM13'
BAUD_RATE = 9600

# Data capture and upload interval in seconds. Less interval will eventually hang the DHT22.
INTERVAL = 2
fsrValue = 0

next_reading = time.time()
client = mqtt.Client()
client_2 = mqtt.Client()
# Set access token
client.username_pw_set(ACCESS_TOKEN_1)
client_2.username_pw_set(ACCESS_TOKEN_2)
# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(THINGSBOARD_HOST, 1883, 60)
client_2.connect(THINGSBOARD_HOST, 1883, 60)
client.loop_start()
client_2.loop_start()
# Open serial port
ser = serial.Serial(PORT, BAUD_RATE)
# When a Dispatch is created with a serial port, it will automatically
# create an XBee object on your behalf for accessing the device.
# If you wish, you may explicitly provide your own XBee:
#
#  xbee = XBee(ser)
#  dispatch = Dispatch(xbee=xbee)
#
# Functionally, these are the same.
dispatch = Dispatch(ser)

# Register the packet handlers with the dispatch:
#  The string name allows one to distinguish between mutiple registrations
#   for a single callback function
#  The second argument is the function to call
#  The third argument is a function which determines whether to call its
#   associated callback when a packet arrives. It should return a boolean.
dispatch.register(
    "status",
    status_handler,
    lambda packet: packet['id']=='status'
)

dispatch.register(
    "io_data",
    io_sample_handler,
    lambda packet: packet['id']=='rx_io_data'
)

dispatch.register(
    "rec_packet",
    receive_packet,
    lambda packet: packet['id']=='rx'
)

# Create API object, which spawns a new thread
# Point the asyncronous callback at Dispatch.dispatch()
#  This method will dispatch a single XBee data packet when called
xbee = ZigBee(ser, callback=dispatch.dispatch)

# Do other stuff in the main thread
while True:
    try:
        pass
        # time.sleep(2)
    except KeyboardInterrupt:
        break

# halt() must be called before closing the serial
# port in order to ensure proper thread shutdown
xbee.halt()
ser.close()
