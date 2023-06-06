import tkinter as tk

def init():
    global ser, ServoControl, w1, w2
    ser = 0
    
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
        print(w1.get(), w2.get())
        self.root.after(1, self.poll)

