import json
import serial
import socket

def init():
    global ser, ServoControl, w1, w2
    ser = serial.Serial("COM4", baudrate= 9600, 
       timeout=2.5, 
       parity=serial.PARITY_NONE, 
       bytesize=serial.EIGHTBITS, 
       stopbits=serial.STOPBITS_ONE
    )

def exchangeJSON(data): # value must be sent as ascii string
    data = json.dumps(data)
    if ser.isOpen():
        ser.write(data.encode('ascii'))
        ser.flush()
        try:
            incoming = ser.readline().decode('ascii')
            print (incoming)
        except Exception as e:
            print (e)
            pass
#         ser.close()

