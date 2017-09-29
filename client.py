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
import paho.mqtt.client as mqtt
import time
import json

# Create handlers for various packet types
def status_handler(name, packet):
    print("Status Update - Status is now: {}".format(packet['status']))
    sensor_data['fsr'] = 4000
    client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)

def io_sample_handler(name, packet):
    print("Samples Received: {}".format(packet['samples']))

def receive_packet(name, packet):
    print(packet)
    print("rf_data: {}".format(packet['rf_data']))
    sensor_data['fsr'] = int.from_bytes(packet['rf_data'], 'big')
    print("sensor_data: {}".format(sensor_data))
    # time.sleep(2)
    # Sending humidity and temperature data to ThingsBoard
    client.publish('v1/devices/me/telemetry', json.dumps(sensor_data), 1)

    # next_reading += INTERVAL
    # sleep_time = next_reading - time.time()
    # if sleep_time > 0:
    #     time.sleep(sleep_time)
    # pass

THINGSBOARD_HOST = '172.25.224.84'
ACCESS_TOKEN = 'sXEes3EvtyUZJkreuRCb'
# ACCESS_TOKEN = '7d92fc20-a1ca-11e7-9e43-df630275a618'
# PORT = '/dev/ttyUSB0'
PORT = 'COM13'
BAUD_RATE = 9600

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
