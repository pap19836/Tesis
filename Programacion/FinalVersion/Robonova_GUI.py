#!C:\Users\stefa\OneDrive - Universidad del Valle de Guatemala\UVG\Tesis\Programacion\tesis_env\Scripts\python.exe"
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QPlainTextEdit, QCheckBox, QDial, QLabel,
                             QWidget, QInputDialog, QFileDialog,
                             QVBoxLayout, QHBoxLayout, QGridLayout)
import sys
import csv
import threading
import pybullet_simulation
import GUI_Functions
import time
from math import ceil
from numpy import deg2rad
import os as os
import pandas as pd
pybullet_simulation.servoValues = deg2rad([0,0,-45,0,0,-60,0,0,0,0,45,0,0,-60,0,0])
t1 = threading.Thread(target=pybullet_simulation.pb,args=())
t1.start()
time.sleep(2)



global currentCoreo
currentCoreo = ""

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.p = None
        ########## SENDING AND RECEIVING POSITION BUTTONS ##########
        # Design
        self.GetDataBtn = QPushButton("Get Data")
        self.SendDataBtn = QPushButton("Send Data")
        self.connectCB = QCheckBox("Connect to Robonova")
        # Connect
        self.GetDataBtn.pressed.connect(self.getData)
        self.SendDataBtn.pressed.connect(self.sendData)
        self.connectCB.stateChanged.connect(self.connectRobonva)
        # Customize
        btnFont = self.GetDataBtn.font()
        btnFont.setPointSize(20)
        self.GetDataBtn.setFont(btnFont)
        self.SendDataBtn.setFont(btnFont)
        checkFont = self.GetDataBtn.font()
        checkFont.setPointSize(15)
        self.connectCB.setFont(checkFont)
        # Layout
        layout1 = QHBoxLayout()
        layout1.addWidget(self.GetDataBtn)
        layout1.addWidget(self.SendDataBtn)

        #################### DIALS ####################
        # Design & Customize 
        self.dials = GUI_Functions.creatDials(self,pybullet_simulation.joints_info)
        # Connect
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
        # Layout
        dialsLayout = GUI_Functions.dialsLayout(self.dials)
        #################### COREOGRAPHY BUTTONS ####################
        # Desing
        self.newCoreoBtn = QPushButton("New Coreography")
        self.loadCoreoBtn = QPushButton("Load Coreography")
        self.addCoreoBtn = QPushButton("Add current position\nto coreography")
        self.removeCoreoBtn = QPushButton("Remove last saved\nposition from coreography")
        self.clearCoreoBtn = QPushButton("Clear coreography")
        self.deleteCoreoBtn = QPushButton("Delete Coreography File")
        self.playCoreoBtn = QPushButton("Play coreography")
        global currentCoreoLabel
        currentCoreoLabel = QLabel("Current Coreography: "+ currentCoreo)
        # Customize
        self.newCoreoBtn.setFont(btnFont)
        self.loadCoreoBtn.setFont(btnFont)
        self.addCoreoBtn.setFont(btnFont)
        self.removeCoreoBtn.setFont(btnFont)
        self.clearCoreoBtn.setFont(btnFont)
        self.deleteCoreoBtn.setFont(btnFont)
        self.playCoreoBtn.setFont(btnFont)
        # Connect
        self.newCoreoBtn.pressed.connect(self.newCoreo)
        self.loadCoreoBtn.pressed.connect(self.loadCoreo)
        self.addCoreoBtn.pressed.connect(self.addCoreo)
        self.removeCoreoBtn.pressed.connect(self.removeCoreo)
        self.clearCoreoBtn.pressed.connect(self.clearCoreo)
        self.deleteCoreoBtn.pressed.connect(self.deleteCoreo)
        self.playCoreoBtn.pressed.connect(self.playCoreo)
        # Layout
        coreoLayout1 = QGridLayout()
        coreoLayout1.addWidget(self.newCoreoBtn, 0, 0)
        coreoLayout1.addWidget(self.loadCoreoBtn, 0, 1)
        coreoLayout1.addWidget(self.addCoreoBtn, 1, 0)
        coreoLayout1.addWidget(self.removeCoreoBtn, 1, 1)
        coreoLayout1.addWidget(self.clearCoreoBtn, 2, 0)
        coreoLayout1.addWidget(self.deleteCoreoBtn, 2, 1)
        coreoLayout1.setSpacing(15)
        coreoLabelsLayout = QHBoxLayout()
        coreoLabelsLayout.addWidget(currentCoreoLabel)
        mainCoreoLayout = QVBoxLayout()
        mainCoreoLayout.addLayout(coreoLayout1)
        mainCoreoLayout.addWidget(self.playCoreoBtn)
        mainCoreoLayout.addWidget(currentCoreoLabel)
        mainCoreoLayout.setSpacing(15)

        #################### TEXT BOX (OTPUTS) ####################
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        self.text.setFont(btnFont)
        tempLayout = QHBoxLayout()
        tempLayout.addLayout(mainCoreoLayout)
        tempLayout.addWidget(self.text)

        #################### MAIN LAYOUT ####################
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(layout1)
        mainLayout.addWidget(self.connectCB)
        mainLayout.addLayout(dialsLayout)
        mainLayout.addLayout(tempLayout)
        mainLayout.setSpacing(15)
        w = QWidget()
        w.setLayout(mainLayout)
        self.setCentralWidget(w)

    ######################### FUNCTIONS #########################
    # TEST FUNCTION (SEND, RECEIVE AND CONNECT)
    def getData(self):
        global b
        b = [n for n in pybullet_simulation.servoValues]
        self.message("Current postion saved!")
    def sendData(self):
        for i in range(len(b)):
            self.dials[i].itemAt(0).widget().setValue(int(b[i]))
        pybullet_simulation.servoValues = b
        self.message("Loaded saved position to simulation!")
    def connectRobonva(self):
        pybullet_simulation.activeConnection = self.connectCB.isChecked()

    # DIAL FUNCTIONS
    def updateDial(self,a):
        dialValue =self.dials[a].itemAt(0).widget().value()
        valueLabel =self.dials[a].itemAt(1).itemAt(1).widget()
        valueLabel.setText(str(dialValue))
        pybullet_simulation.servoValues[a] = deg2rad(dialValue)
    # COREOGRAPHY FUNCTIONS
    def newCoreo(self):
        self.x = QFileDialog()
        self.filename = self.x.getSaveFileName(filter="CSV Files (*.csv)")
        if self.filename[0] != "":
            global currentCoreo
            currentCoreo = os.path.basename(self.filename[0])
            global currentCoreoLabel
            currentCoreoLabel.setText("Current Coreography: " + currentCoreo)
        else:
            pass

    def loadCoreo(self):
        self.x = QFileDialog()
        self.filename = self.x.getOpenFileName()
        if self.filename[0] != "":
            global currentCoreo
            currentCoreo = os.path.basename(self.filename[0])
            global currentCoreoLabel
            currentCoreoLabel.setText("Current Coreography: " + currentCoreo)
        else:
            pass
    def addCoreo(self):
        with open(currentCoreo,"a") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(pybullet_simulation.servoValues)
        self.message("Position saved to coreography!")
        
    def removeCoreo(self):
        with open(currentCoreo,"r+") as csvfile:
            lines = csvfile.readlines()
            lines.pop()
            csvfile = open(currentCoreo, "w+")
            csvfile.truncate(0)
            csvfile.writelines(lines)
        self.message("Position removed from coreograhy!")
        
    def clearCoreo(self):
        with open(currentCoreo,"r+") as csvfile:
            lines = ""
            csvfile = open(currentCoreo, "w+")
            csvfile.truncate(0)
            csvfile.writelines(lines)
        self.message("Coreography cleared!")
    def deleteCoreo(self):
        if os.path.exists(currentCoreo):
            os.remove(currentCoreo)
            self.message("Coreography has been deleted!")
            currentCoreoLabel.setText("Current Coreography: ")
        else:
            self.message("No coreography selected")
    def playCoreo(self):
        self.message("Playing coreography...")
        with open(currentCoreo, "r+") as csvfile:
            reader = csv.reader(csvfile)
            rows = []
            for line in reader:
                if not line:
                    continue
                rows.append(line)
            for i in range(len(rows)):
                coreoPosition = [float(x) for x in rows[i] ]
                pybullet_simulation.servoValues = coreoPosition
                time.sleep(0.1)
        self.message("Coreography done!")
            
    # MISC FUNCTIONS
    def message(self, s):
        self.text.appendPlainText(s)

app = QApplication(sys.argv)

w = MainWindow()
w.show()

app.exec_()