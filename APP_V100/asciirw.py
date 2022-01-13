from logging import log
import serial
import ConfigParser
import logging
import serial
from serial.serialutil import PARITY_NONE, STOPBITS_ONE

log = logging.getLogger(__name__)

class asciirw:
    _platform='WIN'
    ser = serial()

    def __init__(self):
        pass

    def __init__(self,platform,portName,baudrate,parity,stopbit,databits):
        
        config = ConfigParser.ConfigParser()
        config.read('./App_V100/app.config')

        self._platform = platform
        log.debug(self._platform +" Selected")
        
        self.InitializeSerialPort()

    def InitializeSerialPort(self):
        self.ser = serial.Serial(self.portName)
        self.ser.baudrate=self.baudrate
        self.ser.parity=self.parity
        self.ser.stopbits=self.stopbit
        self.ser.bytesize=self.databits

