"""
This modules handle reciveced data from XBee Nodes
"""
import sys
import glob
import serial


START_DELIMETER = 0x7E
FRAME_MODEM_STATUS = 0x8A
FRAME_TRANSMIT_REQUEST = 0x10
FRAME_TRANSMIT_STATUS = 0x8B
FRAME_RECIVE_PACKET = 0x90


START = 'xbee_start_packet'
LENGTH_Msb = 'xbee_length_Msb'
LENGTH_Lsb = 'xbee_length_Lsb'
FRAME_TYPE = 'frame_type'
FRAME_DATA = 'frame_data'
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
    Handling communication with XBee
    """
    def __init__(self):
        self.reciveStatus = START
        self.xbeeStartDelimeter = 0x7E
        self.xbeePacketLength_Msb = 0
        self.xbeePacketLength_Lsb = 0
        self.xbeeLength = 0
        self.xbeeFrameType = FRAME_MODEM_STATUS
        self.dataValue = 0xFF

    def current_method(self, method_name):
        try:
            method = getattr(self, method_name)
        except AttributeError:
            print("AttributeError")            
        return method()

    def packet_print(self):
        print("{}".format(self.dataValue), end=' ')

    def byte_recieved(self, val):
        self.dataValue = val
        self.current_method(START)

    def xbee_start_packet(self):
        print("\r\n New Packet Arrived . . . !")
        self.packet_print()
        self.reciveStatus = LENGTH_Msb
    
    def xbee_length_Msb(self):
        self.reciveStatus = LENGTH_Lsb
        self.packet_print()
        self.xbeePacketLength_Msb = self.dataValue


    def xbee_length_Lsb(self):
        self.reciveStatus = FRAME_TYPE
        self.packet_print()
        self.xbeeFrameType = self.dataValue
        self.xbeeLength = LENGTH_Msb * 256 + LENGTH_Lsb

    def frame_type(self):
        self.reciveStatus = FRAME_DATA
        self.packet_print()
        self.frame_type = self.dataValue
    


xbeeNode = serial.Serial()
xbeeNode.port = serial_ports()[0]
xbeeNode.baudrate = 9600
xbeeNode.open()
xbeeNode.reset_input_buffer()
xbeeNode.readline()        

