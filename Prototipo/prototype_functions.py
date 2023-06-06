import time
import json
import serial
from pprint import pprint
import random

import prototype_settings

def exchangeJSON(data): # value must be sent as ascii string
    data = json.dumps(data)
    if prototype_settings.ser.isOpen():
        prototype_settings.ser.write(data.encode('ascii'))
        prototype_settings.ser.flush()
        try:
            incoming = prototype_settings.ser.readline().decode('ascii')
            print (incoming)
        except Exception as e:
            print (e)
            pass
#         prototype_settings.ser.close()

