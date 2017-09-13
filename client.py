import os
import time
from time import sleep
import sys
import json
import serial
import paho.mqtt.client as mqtt
# import XBee


#A function to find the COM port in different platforms
def serial_ports():
    
    """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result
    if __name__ == '__main__':
        print(serial_ports())



THINGSBOARD_HOST = '172.25.224.84'
ACCESS_TOKEN = 'sXEes3EvtyUZJkreuRCb'

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

xbee = serial.Serial()
xbee.port = serial_ports()[0]
xbee.baudrate = 115200
xbee.open()
xbee.reset_input_buffer()


try:
    while True:
        print(xbee.read())
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
