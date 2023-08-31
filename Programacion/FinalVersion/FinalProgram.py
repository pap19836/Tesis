import Robonova_Control
import threading

t1 = threading.Thread(target=Robonova_Control.GUI,args=())
t2 = threading.Thread(target=Robonova_Control.pb,args=())

t1.start()
t2.start()

while True:
    a = 5