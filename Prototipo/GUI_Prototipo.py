import time
import json
import serial
from pprint import pprint
import random

print ("Ready...")
ser  = serial.Serial("COM4", baudrate= 9600, 
       timeout=2.5, 
       parity=serial.PARITY_NONE, 
       bytesize=serial.EIGHTBITS, 
       stopbits=serial.STOPBITS_ONE
    )
data = {}
data["operation"] = "sequenc"

data=json.dumps(data)
print (data)
if ser.isOpen():
    ser.write(data.encode('ascii'))
    ser.flush()
    try:
        incoming = ser.readline().decode('ascii')
        print (incoming)
    except Exception as e:
        print (e)
        pass
    ser.close()
else:
    print ("opening error")
