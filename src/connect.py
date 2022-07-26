import serial
from time import sleep

class _AVR:
    def __init__(self):
        self.ser = None

    def connect(self, port, baudrate=115200):
        if self.ser != None:
            self.close()
        try:
            self.ser = serial.Serial(port, baudrate, timeout=0.1)
            sleep(2.5)
            return True
        except:
            self.ser = None
            return False

    def close(self):
        if self.ser != None:
            self.ser.close()
            self.ser = None
        
#カラーセンサをもつArduino
class AVR_1(_AVR):
    def __init__(self):
        super(AVR_1, self).__init__()

    def receive(self):
        self.ser.write(b'a')
        data = self.ser.read()
        return int.from_bytes(data, 'big')

#モータを制御するArduino
class AVR_2(_AVR):
    def __init__(self):
        super(AVR_2, self).__init__()

    def send(self, command):
        self.ser.write(command)
    

