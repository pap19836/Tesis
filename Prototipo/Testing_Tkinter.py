import tkinter as tk, time

# class ServoControl(object):
# 
#   def __init__(self):
#     self.root = tk.Tk()
#     
#     w1 = tk.Scale(self.root, from_=0, to=180)
#     w1.pack()
#     w2 = tk.Scale(self.root, from_=0, to=180)
#     w2.pack()
#     self.poll()
# 
#   def poll(self):
#     print(w1.get(), w2.get())
#     self.root.after(1000, self.poll)
# 
# servos = ServoControl()
# servos.root.mainloop()

root = tk.Tk()
global w1, w2
w1 = tk.Scale(root, from_=0, to=180)
w1.pack()
w2 = tk.Scale(root, from_=0, to=180)
w2.pack()
while(1):
    root.update()