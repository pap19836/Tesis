import time
import json
import serial
from pprint import pprint
import random

from prototype_functions import *
import prototype_settings


# start serial communication
prototype_settings.init()


prototype_settings.ser  = serial.Serial("COM4", baudrate= 9600, 
       timeout=2.5, 
       parity=serial.PARITY_NONE, 
       bytesize=serial.EIGHTBITS, 
       stopbits=serial.STOPBITS_ONE
    )
data = {}
data['servo1'] = '100'
data['servo2'] = '50'

exchangeJSON(data) #data must be sent as dictionary/key

