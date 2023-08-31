#!C:\Users\stefa\OneDrive - Universidad del Valle de Guatemala\UVG\Tesis\Programacion\tesis_env\Scripts\python.exe"
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QPlainTextEdit, QCheckBox, QDial, QLabel,
                             QWidget,
                             QVBoxLayout, QHBoxLayout, QGridLayout)
import sys
import threading
import pybullet_simulation
import GUI_Functions
import time
from math import ceil
from numpy import deg2rad
global servoValues
t1 = threading.Thread(target=pybullet_simulation.pb,args=())
t1.start()
time.sleep(2)


servoValues = None
global data
data = []

global sliderValues
sliderValues = []
for i in range(len(pybullet_simulation.joints_info)):
    sliderValues.append(0)
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.p = None

        self.GetDataBtn = QPushButton("Get Data")
        self.GetDataBtn.pressed.connect(self.getData)
        self.SendDataBtn = QPushButton("Send Data")
        self.SendDataBtn.pressed.connect(self.sendData)
        self.connectCB = QCheckBox("Connect to Robonova")
        self.connectCB.stateChanged.connect(self.connectRobonva)
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)

        self.dials = GUI_Functions.creatDials(self,pybullet_simulation.joints_info)
        self.dials[0].itemAt(0).widget().valueChanged.connect(lambda: self.updateDial(0))
        self.dials[1].itemAt(0).widget().valueChanged.connect(lambda: self.updateDial(1))
        self.dials[2].itemAt(0).widget().valueChanged.connect(lambda: self.updateDial(2))
        self.dials[3].itemAt(0).widget().valueChanged.connect(lambda: self.updateDial(3))
        self.dials[4].itemAt(0).widget().valueChanged.connect(lambda: self.updateDial(4))
        self.dials[5].itemAt(0).widget().valueChanged.connect(lambda: self.updateDial(5))
        self.dials[6].itemAt(0).widget().valueChanged.connect(lambda: self.updateDial(6))
        self.dials[7].itemAt(0).widget().valueChanged.connect(lambda: self.updateDial(7))
        self.dials[8].itemAt(0).widget().valueChanged.connect(lambda: self.updateDial(8))
        self.dials[9].itemAt(0).widget().valueChanged.connect(lambda: self.updateDial(9))
        self.dials[10].itemAt(0).widget().valueChanged.connect(lambda: self.updateDial(10))
        self.dials[11].itemAt(0).widget().valueChanged.connect(lambda: self.updateDial(11))
        self.dials[12].itemAt(0).widget().valueChanged.connect(lambda: self.updateDial(12))
        self.dials[13].itemAt(0).widget().valueChanged.connect(lambda: self.updateDial(13))
        self.dials[14].itemAt(0).widget().valueChanged.connect(lambda: self.updateDial(14))
        self.dials[15].itemAt(0).widget().valueChanged.connect(lambda: self.updateDial(15))

        dialsLayout = GUI_Functions.dialsLayout(self.dials)
        l = QVBoxLayout()
        l.addWidget(self.GetDataBtn)
        l.addWidget(self.SendDataBtn)
        l.addWidget(self.connectCB)
        l.addLayout(dialsLayout)
        l.addWidget(self.text)
        w = QWidget()
        w.setLayout(l)

        self.setCentralWidget(w)
    def updateDial(self,a):

        dialValue =self.dials[a].itemAt(0).widget().value()
        valueLable =self.dials[a].itemAt(1).itemAt(1).widget()
        valueLable.setText(str(dialValue))
        pybullet_simulation.servoValues[a] = deg2rad(dialValue)
    def message(self, s):
        self.text.appendPlainText(s)

    def getData(self):
        a = pybullet_simulation.slider_values
        data.append(servoValues)
        self.message(str(a))
    
    def sendData(self):
        pybullet_simulation.a = 10
    def connectRobonva(self):
        pybullet_simulation.activeConnection = self.connectCB.isChecked()



app = QApplication(sys.argv)

w = MainWindow()
w.show()

app.exec_()