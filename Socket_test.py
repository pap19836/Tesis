import socket
from time import sleep
from Prototipo.prototype_functions import exchangeJSON
s = socket.socket()
ip = '192.168.215.32'
port = 8091
s.connect((ip,port))

data = {}
data['servo1'] = 50
data['servo2'] = 10
while True:
    s.sendall(b"Hello world\n")
    s.sendall(b"Puto el que lea\n")
    #data = s.recv(1024)
    #print(f"Received {data!r}")
    sleep(3)