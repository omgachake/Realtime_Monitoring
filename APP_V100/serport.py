import logging
import ConfigParser
from serial.serialutil import PARITY_NAMES, PARITY_NONE, STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE,STOPBITS_TWO, to_bytes
import serial
from logging import log
log = logging.getLogger(__name__)

class serport:
    '''Model for Serialport'''
    def __init__(self,portname,baudrate,parity,stopbits,databits):
        self.serialport =serial.Serial(portname)
        self.serialport.port = portname
        self.serialport.baudrate = baudrate
        self.serialport.parity = parity
        self.serialport.stopbits = stopbits
        #self.serialport.bytesize = databits
        self.serialport.bytesize=8
        pass

    def __init__(self,platform,mode,timeout):
        config = ConfigParser.ConfigParser()
        config.read('./App_V100/app.config')
        print(config.sections())
        if(mode=='Ascii'):
            self.serialport =serial.Serial(config.get(platform,'A_COMPORT'))
            #self.serialport.port = config[platform]['A_COMPORT']
            self.serialport.baudrate = config.getint(platform,'A_BAUDRATE')
            self.serialport.parity = config.get(platform,'A_PARITY')
            self.serialport.stopbits = config.getint(platform,'A_STOPBITS')
            #self.serialport.bytesize = to_bytes(config.get(platform,'A_DATABITS'))
            self.serialport.bytesize = 8
            self.serialport.timeout=timeout
            log.debug("Ascii Port Configured on --> " +self.serialport.port)
        if(mode=='Modbus'):
            self.serialport =serial.Serial(config.get(platform,'M_COMPORT'))
            #self.serialport.port = config[platform]['A_COMPORT']
            self.serialport.baudrate = config.getint(platform,'M_BAUDRATE')
            self.serialport.parity = config.get(platform,'M_PARITY')
            self.serialport.stopbits = config.getint(platform,'M_STOPBITS')
            #self.serialport.bytesize = to_bytes(config.get(platform,'M_DATABITS'))
            self.serialport.bytesize = 8
            self.serialport.timeout=timeout
            log.debug("Modbus Port Configured on --> " +self.serialport.port)
        pass