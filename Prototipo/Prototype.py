import time
import json
import serial
from pprint import pprint
import random
import tkinter as tk
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

# Define window
class ServoControl(object):

    def __init__(self):
        self.root = tk.Tk()
        global w1, w2
        w1 = tk.Scale(self.root, from_=0, to=180)
        w1.pack()
        w2 = tk.Scale(self.root, from_=0, to=180)
        w2.pack()
        self.poll()
        
    def poll(self):
#         if(prototype_settings.ser.is_open != 1):
#             prototype_settings.ser.open()
        data = {}
        data['servo1'] = str(w1.get())
        data['servo2'] = str(w2.get())
        print(data)
        exchangeJSON(data)
        self.root.after(100, self.poll)





# exchangeJSON(data) #data must be sent as dictionary/key
# root = tk.Tk()
# global w1, w2
# w1 = tk.Scale(root, from_=0, to=180)
# w1.pack()
# w2 = tk.Scale(root, from_=0, to=180)
# w2.pack()
# while(1):
#     if(prototype_settings.ser.is_open != 1):
#         prototype_settings.ser.open()
#     root.update()
#     data = {}
#     data['servo1'] = str(w1.get())
#     data['servo2'] = str(w2.get())
#     print(data)
#     exchangeJSON(data)
#     time.sleep(100)
servos = ServoControl()
servos.root.mainloop()