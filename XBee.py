"""
This modules handle reciveced data from XBee Nodes
"""
import sys
import glob
import serial

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
    if __name__ == '__main__':
        print(serial_ports())
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

class XBeeHandler:
    """
    initialinzing a serial object to communicate with XBEE module
    """
    def __init__(self):
        #Initializing of a serial port
        self.ser = serial.Serial()
        self.ser.port = serial_ports()[0]
        self.ser.baudrate = 9600
        self.ser.open()
        self.ser.reset_input_buffer()
        # self.ser.readline()

xbeeNode = serial.Serial()
xbeeNode.port = serial_ports()[0]
xbeeNode.baudrate = 9600
xbeeNode.open()
xbeeNode.reset_input_buffer()
xbeeNode.readline()        