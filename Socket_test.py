import socket
from time import sleep

import json
s = socket.socket()
ip = '192.168.215.32'
port = 8091
s.connect((ip,port))

data = {}
data['servo1'] = "10"
data['servo2'] = "10"

data = json.dumps(data)
print(type(data))
while True:
    s.sendall(bytes(data, "utf-8"))
    #data = s.recv(1024)
    #print(f"Received {data!r}")
    sleep(1)