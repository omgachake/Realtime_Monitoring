from ctypes import Array
from ctypes.wintypes import SHORT
import logging
import logging.config
import time
import sys
import re
from threading import Thread, Lock
#import asciirw as arw
import serport
import struct
import bitstring
from pyModbusTCP.server import ModbusServer as server
import pyModbusTCP.server
from pyModbusTCP import utils

# Modbus Serial Server
from pymodbus.version import version
from pymodbus.server.sync import StartSerialServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSparseDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.transaction import ModbusRtuFramer, ModbusBinaryFramer

store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [17]*100),
        co=ModbusSequentialDataBlock(0, [17]*100),
        hr=ModbusSequentialDataBlock(0, [17]*100),
        ir=ModbusSequentialDataBlock(0, [17]*100))

identity = ModbusDeviceIdentification()
context = ModbusServerContext(slaves=store, single=True)
#end region

server = server(host='localhost', port=502)
databank = pyModbusTCP.server.DataBank

NO_Regex = '=(?P<data>.*)'


def ConvertFloatToRegisters(rawInput):
    rawInput = float(rawInput)
    b = struct.pack('<f', rawInput)
    #b= bitstring.BitArray(float=rawInput,length=32)
    ary = struct.unpack('HH', b)
    #print(ary)
    return ary

def SetRegsToDataBank(regArry, offset):
    databank.set_words(offset, regArry)
    #store.setValues(3,offset,regArry[offset])
    values = context[0].getValues(3, 0, count=100)
    values[offset] = regArry[offset]
    values[offset+1] = regArry[offset+1]
    store.setValues(3,offset,values)

def Parse(rawInput, regexInput):
    val = 9999
    m = re.search(regexInput, rawInput)
    if not m:
        regArry = ConvertFloatToRegisters(val)
        SetRegsToDataBank(regArry,0)
    else:
        regArry = ConvertFloatToRegisters(m.group('data'))
        SetRegsToDataBank(regArry,0)
        return m.group('data')


def Poll():
    while(1):
        asciiPort.serialport.write(b'T 200 NO')
        time.sleep(3)
        rawString = asciiPort.serialport.readline()
        asciiPort.serialport.reset_input_buffer()
        print("Raw String received : -->  "+rawString)
        data = Parse(rawString, NO_Regex)
        print("Extracted data = "+str(data))

def StartRTUServer():
    StartSerialServer(context, framer=ModbusRtuFramer, identity=identity,port='COM6', timeout=.005, baudrate=9600)

def StartModbusServer():
    serverThread = Thread(target=server.start)
    serverThread.daemon = True
    serverThread.start()
    databank.set_words(0, [0,0,0,0])

    serialServerThread = Thread(target=StartRTUServer)
    serialServerThread.daemon=True
    serialServerThread.start()




def main():
    logging.config.fileConfig(fname='logging.conf',disable_existing_loggers=False)
    log = logging.getLogger(__name__)
    log.debug("App Started")
    global asciiPort
    global modbusPort
    asciiPort = serport.serport('WIN', 'Ascii', 2)
    #modbusPort = serport.serport('WIN', 'Modbus', 2)
    StartModbusServer()
    Poll()
    input('Press any key to exit...')
    sys.exit(0)


if __name__ == '__main__':
    main()
