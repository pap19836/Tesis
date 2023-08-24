import socket
from time import sleep

import json
s = socket.socket()
ip = '192.168.215.32'
port = 8091
s.connect((ip,port))
global pos
pos = [0,50,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
pos = [str(x) for x in pos]

data = {'LeftShoulder1':None,
        'LeftShoulder2':None,
        'RightShoulder1':None,
        'RightShoulder2':None,
        'LeftWaist':None,
        'LeftHip1':None,
        'LeftHip2':None,
        'LeftKnee':None,
        'LeftAnkle1':None,
        'LeftAnkle2':None,
        'RightWaist':None,
        'RightHip1':None,
        'RightHip2':None,
        'RightKnee':None,
        'RightAnkle1':None,
        'RightAnkle2':None}

#for key,value in data.items


print(type(data))
while True:
    data = {'LeftShoulder1':pos[0],
        'LeftShoulder2':pos[1],
        'RightShoulder1':pos[2],
        'RightShoulder2':pos[3],
        'LeftWaist':pos[4],
        'LeftHip1':pos[5],
        'LeftHip2':pos[6],
        'LeftKnee':pos[7],
        'LeftAnkle1':pos[8],
        'LeftAnkle2':pos[9],
        'RightWaist':pos[10],
        'RightHip1':pos[11],
        'RightHip2':pos[12],
        'RightKnee':pos[13],
        'RightAnkle1':pos[14],
        'RightAnkle2':pos[15]}
    
    data_json = json.dumps(data)
    
    
    s.sendall(bytes(data_json, "utf-8"))
    sleep(1)