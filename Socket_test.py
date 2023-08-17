import socket
s = socket.socket
ip = '0.0.0.0'
port = 8091
s.bind((ip,port))
s.listen(0)

while True:
    client, addr = s.accept()
    while True:
        content = client.recv(32)
        if len(content)==0:
            break
        else:
            print(content)
        print("closing connection")
        client.close()