#!C:\Users\stefa\OneDrive - Universidad del Valle de Guatemala\UVG\Tesis\Programacion\tesis_env\Scripts\python.exe"
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QPlainTextEdit, QCheckBox, QDial, QLabel,
                             QWidget, QInputDialog, QFileDialog,
                             QVBoxLayout, QHBoxLayout, QGridLayout)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import cv2
import sys
import csv
import threading
import pybullet_simulation as pb_sim
import GUI_Functions
import time
from numpy import deg2rad,rad2deg, arange
import os as os
from functools import partial
from scipy import interpolate
pb_sim.servoValues = deg2rad([0,0,-45,0,0,
                                           -60,0,0,0,0,
                                           45,0,0,-60,0,0])
t1 = threading.Thread(target=pb_sim.pb,args=())
t1.start()
time.sleep(2)



global currentCoreo
currentCoreo = ""

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        #self.showMaximized()
        self.dt = 0.05
        ########## SENDING AND RECEIVING POSITION BUTTONS ##########
        # Design
        # Obsolete SendData & GetData
        # self.GetDataBtn = QPushButton("Get Data")
        # self.SendDataBtn = QPushButton("Send Data")
        self.connectCB = QCheckBox("Connect to Robonova")
        # Connect
        # self.GetDataBtn.pressed.connect(self.getData)
        # self.SendDataBtn.pressed.connect(self.sendData)
        self.connectCB.stateChanged.connect(self.connectRobonva)
        # Customize
        # btnFont = self.GetDataBtn.font()
        # btnFont.setPointSize(20)
        # self.GetDataBtn.setFont(btnFont)
        # self.SendDataBtn.setFont(btnFont)
        btnFont = self.connectCB.font()
        btnFont.setPointSize(20)
        self.connectCB.setFont(btnFont)
        # # Layout
        # Obsolete SendData & GetData
        # layout1 = QHBoxLayout()
        # layout1.addWidget(self.GetDataBtn)
        # layout1.addWidget(self.SendDataBtn)

        #################### DIALS ####################
        # Design & Customize 
        self.dialSubLayout = GUI_Functions.creatDials(self,
                                            pb_sim.joints_info)
        self.dials = []
        for i in range(len(self.dialSubLayout)):
            x = self.dialSubLayout[i].itemAt(0).widget()
            self.dials.append(x)
        # Connect
        for i in range(len(self.dials)):
            self.dials[i].valueChanged.connect(partial(self.updateDial,i))
        # Layout
        dialsLayout = GUI_Functions.dialsLayout(self.dialSubLayout)
        #################### choreography BUTTONS ####################
        # Desing
        self.newCoreoBtn = QPushButton("New choreography")
        self.loadCoreoBtn = QPushButton("Load choreography")
        self.addCoreoBtn = QPushButton(
            "Add current position\nto choreography")
        self.removeCoreoBtn = QPushButton(
            "Remove last saved\nposition from choreography")
        self.clearCoreoBtn = QPushButton("Clear choreography")
        self.deleteCoreoBtn = QPushButton("Delete choreography File")
        self.playCoreoBtn = QPushButton("Play choreography")
        self.uploadCoreoBtn = QPushButton("Upload choregraphy")

        self.smoothTrajectoryCB = QCheckBox("Smooth trajectory")
        self.dtlabel = QLabel("dt")
        self.dtvalue = QPlainTextEdit()
        self.dtbutton = QPushButton("Set")
        self.repeatCoreoCB = QCheckBox("Repeat choreography")
        self.currentCoreoLabel = QLabel(
            "Current choreography: "+ currentCoreo)
        # Customize
        self.newCoreoBtn.setFont(btnFont)
        self.loadCoreoBtn.setFont(btnFont)
        self.addCoreoBtn.setFont(btnFont)
        self.removeCoreoBtn.setFont(btnFont)
        self.clearCoreoBtn.setFont(btnFont)
        self.deleteCoreoBtn.setFont(btnFont)
        self.playCoreoBtn.setFont(btnFont)
        self.uploadCoreoBtn.setFont(btnFont)
        self.uploadCoreoBtn.setFixedSize(270,40)
        self.uploadCoreoBtn.setEnabled(False)
        self.dtvalue.setFixedSize(50,25)
        self.dtbutton.setFixedSize(50,25)
        # Connect
        self.newCoreoBtn.pressed.connect(self.newCoreo)
        self.loadCoreoBtn.pressed.connect(self.loadCoreo)
        self.addCoreoBtn.pressed.connect(self.addCoreo)
        self.removeCoreoBtn.pressed.connect(self.removeCoreo)
        self.clearCoreoBtn.pressed.connect(self.clearCoreo)
        self.deleteCoreoBtn.pressed.connect(self.deleteCoreo)
        self.playCoreoBtn.pressed.connect(
            partial(self.playCoreo, buttonPressed = True))
        self.uploadCoreoBtn.pressed.connect(self.uploadCoreo)
        self.repeatCoreoCB.stateChanged.connect(
            partial(self.playCoreo, buttonPressed = False))
        self.dtbutton.pressed.connect(self.setdt)
        # Layout
        coreoLayout1 = QGridLayout()
        coreoLayout1.addWidget(self.newCoreoBtn, 0, 0)
        coreoLayout1.addWidget(self.loadCoreoBtn, 0, 1)
        coreoLayout1.addWidget(self.addCoreoBtn, 1, 0)
        coreoLayout1.addWidget(self.removeCoreoBtn, 1, 1)
        coreoLayout1.addWidget(self.clearCoreoBtn, 2, 0)
        coreoLayout1.addWidget(self.deleteCoreoBtn, 2, 1)
        coreoLayout1.setSpacing(15)
        coreoLayout2 = QHBoxLayout()
        coreoLayout2.addWidget(self.playCoreoBtn)
        coreoLayout2.addWidget(self.uploadCoreoBtn)
        mainCoreoLayout = QVBoxLayout()
        mainCoreoLayout.addLayout(coreoLayout1)
        mainCoreoLayout.addLayout(coreoLayout2)
        dtLayout = QHBoxLayout()
        dtLayout.addWidget(self.dtlabel)
        dtLayout.addWidget(self.dtvalue)
        dtLayout.addWidget(self.dtbutton)
        dtLayout.setContentsMargins(20,0,300,0)
        coreoLayout3 = QHBoxLayout()
        coreoLayout3.addWidget(self.smoothTrajectoryCB)
        coreoLayout3.addLayout(dtLayout)
        coreoLayout3.addWidget(self.repeatCoreoCB)
        mainCoreoLayout.addLayout(coreoLayout3)
        mainCoreoLayout.addWidget(self.currentCoreoLabel)
        mainCoreoLayout.setSpacing(15)

        #################### TEXT BOX (OTPUTS) ####################
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)
        self.text.setFont(btnFont)
        coreoAndTextLayout = QVBoxLayout()
        coreoAndTextLayout.addLayout(mainCoreoLayout)
        coreoAndTextLayout.addWidget(self.text)

        #################### IMAGES ####################
        imgTitle = QLabel("Current step preview:")
        prevImgBtn = QPushButton("<<")
        currentImg = QLabel("x of x")

        nextImgBtn = QPushButton(">>")
        
        self.imgW = 480
        self.imgH = 360
        # Step images
        stepImg = cv2.imread("Programacion\FinalVersion\RobonovaWalking.png")
        stepImg = cv2.cvtColor(stepImg, cv2.COLOR_BGR2RGB)
        h, w, ch = stepImg.shape
        bpl = w*ch
        qImg = QImage(stepImg.data, w, h, bpl, QImage.Format_RGB888)
        stepImg = QLabel()
        stepImg.setPixmap(QPixmap(qImg).scaled(self.imgW,self.imgH))
        
        imgBtnLayout = QHBoxLayout()
        imgBtnLayout.addWidget(prevImgBtn,2)
        imgBtnLayout.addWidget(currentImg,1)
        imgBtnLayout.addWidget(nextImgBtn,2)
        imgLayout = QVBoxLayout()
        imgLayout.addWidget(imgTitle)
        imgLayout.addWidget(stepImg)
        imgLayout.addLayout(imgBtnLayout)

        imgAndCoreoLayout = QHBoxLayout()
        imgAndCoreoLayout.addLayout(coreoAndTextLayout)
        imgAndCoreoLayout.addLayout(imgLayout)

        #################### MAIN LAYOUT ####################
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.connectCB)
        mainLayout.addLayout(dialsLayout)
        mainLayout.addLayout(imgAndCoreoLayout)
        mainLayout.setSpacing(15)

        w = QWidget()
        w.setLayout(mainLayout)
        self.setCentralWidget(w)

    ######################### FUNCTIONS #########################
    # TEST FUNCTION (SEND, RECEIVE AND CONNECT)
    # ***Funciones obsoletas***
    # def getData(self):
    #     global b
    #     b = [n for n in pb_sim.servoValues]
    #     self.message("Current postion saved!")
    # def sendData(self):
    #     for i in range(len(b)):
    #         self.dialSubLayout[i].itemAt(0).widget().setValue(int(rad2deg(b[i])))
    #     pb_sim.servoValues = b
    #     self.message("Loaded saved position to simulation!")
    # ***Fin de funciones obsoletas***
    def connectRobonva(self):
        self.uploadCoreoBtn.setEnabled(True)
        pb_sim.activeConnection = self.connectCB.isChecked()

    # DIAL FUNCTIONS
    def updateDial(self,a):
        dialValue =self.dialSubLayout[a].itemAt(0).widget().value()
        valueLabel =self.dialSubLayout[a].itemAt(1).itemAt(1).widget()
        valueLabel.setText(str(dialValue))
        pb_sim.servoValues[a] = deg2rad(dialValue)
        
        #self.lableSim.setPixmap(simPixMap.scaled(640,680))
    # choreography FUNCTIONS
    def newCoreo(self):
        parentPath = os.getcwd()
        self.x = QFileDialog()
        self.filename = self.x.getSaveFileName(filter="CSV Files (*.csv)")
        f = open(self.filename[0], "a")
        f.close()
        dirName = os.path.basename(self.filename[0]).split(".")[0]
        self.dirPath = os.path.join(parentPath,dirName)
        os.makedirs(self.dirPath)
        self.newFilePath = self.dirPath+"\\"+os.path.basename(self.filename[0])
        os.rename(self.filename[0],self.newFilePath)
        if self.newFilePath != "":
            global currentCoreo
            currentCoreo = os.path.basename(self.newFilePath)
            self.currentCoreoLabel.setText(
                "Current choreography: " + currentCoreo)
        else:
            pass

    def loadCoreo(self):
        self.x = QFileDialog()
        self.filename = self.x.getOpenFileName(filter="CSV Files (*.csv)")
        if self.filename[0] != "":
            global currentCoreo
            currentCoreo = os.path.basename(self.filename[0])
            self.currentCoreoLabel.setText(
                "Current choreography: " + currentCoreo)
        else:
            pass
    def addCoreo(self):
        try:
            with open(currentCoreo,"a") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(pb_sim.servoValues)
            self.message("Position saved to choreography!")
        except FileNotFoundError:
            self.message("Choreography does not exist or has not been selected")
    def removeCoreo(self):
        try:
            with open(currentCoreo, "r+") as csvfile:
                lines = csvfile.readlines()
                updatedlines = []
                for line in lines:
                    if line == "\n":
                        continue
                    updatedlines.append(line)
                updatedlines.pop()
                lines = ""
                csvfile.truncate(0)
                csvfile.writelines(lines)
            with open(currentCoreo, "w+") as csvfile:
                csvfile.writelines(updatedlines)
            self.message("Position removed from coreograhy!")
        except (FileNotFoundError, IndexError) as err:
            if isinstance(err,FileNotFoundError):
                self.message("Choreography does not exist or has not been selected")
            elif isinstance(err,IndexError):
                self.message("Choreography is already empty!")
            else:
                self.message("Unknown Error")
    def clearCoreo(self):
        try:
            with open(currentCoreo,"r+") as csvfile:
                lines = ""
                csvfile.truncate(0)
                csvfile.writelines(lines)
            self.message("Choreography cleared!")
        except FileNotFoundError:
            self.message("Choreography does not exist or has not been selected")
    def deleteCoreo(self):
        try:
            os.remove(currentCoreo)
            self.message("Choreography has been deleted!")
            self.currentCoreoLabel.setText("Current choreography: ")
        except FileNotFoundError:
            self.message("Choreography does not exist or has not been selected")
    
    t2stop = threading.Event()
    repeating = False
    def playCoreo(self, **buttonPressed):
        #self.dt = 0.05
        try:
            with open(currentCoreo, "r+") as csvfile:
                reader = csv.reader(csvfile)
                self.coreoPositions = []
                for line in reader:
                    if not line:
                        continue
                    self.coreoPositions.append(line)
            
            if self.smoothTrajectoryCB.isChecked():
                t = len(self.coreoPositions)-1
                x = range(len(self.coreoPositions))
                y = self.coreoPositions
                cs = interpolate.make_interp_spline(x,y, 1)
                xs = arange(0,t,self.dt)
                self.coreoPositions = cs(xs)
            self.t2 = threading.Thread(target=GUI_Functions.repeatCoreo,
                    args=(self,self.coreoPositions,self.t2stop,self.smoothTrajectoryCB.isChecked(),self.dt))

            if buttonPressed["buttonPressed"] == True:
                if (self.repeatCoreoCB.isChecked() 
                    and not(self.t2.is_alive())) == True:
                    self.message("Playing choreography...")
                    self.repeating = True
                    self.t2stop.clear()
                    self.t2.start()
                else:
                    self.message("Playing choreography...")
                    self.t2stop.set()
                    self.t2.start()
                    self.message("Choreography done!")

            if (not(self.repeatCoreoCB.isChecked()) 
                and self.repeating) == True:
                self.repeating = False
                self.t2stop.set()
                self.message("Choreography done!")
        except (FileNotFoundError,IndexError) as err:
            if(isinstance(err,FileNotFoundError)):
                self.message("Choreography does not exist or has not been selected")
            elif(isinstance(err,IndexError)):
                self.message("Cannot play empty choreography")

    def uploadCoreo(self):
        try:
            with open(currentCoreo, "r+") as csvfile:
                reader = csv.reader(csvfile)
                self.coreoPositions = []
                for line in reader:
                    if not line:
                        continue
                    self.coreoPositions.append(line)
            
            if self.smoothTrajectoryCB.isChecked():
                t = len(self.coreoPositions)-1
                x = range(len(self.coreoPositions))
                y = self.coreoPositions
                cs = interpolate.make_interp_spline(x,y, 1)
                xs = arange(0,t,self.dt)
                self.coreoPositions = cs(xs)
            pb_sim.realCoreo = self.coreoPositions
            pb_sim.uploadCoreo = True
        except (AttributeError, FileNotFoundError):
            self.message("Choreography does not exist or has not been selected")


    def setdt(self):
        try:
            self.dt = float(self.dtvalue.toPlainText())
        except ValueError:
            self.message("dt not specified or invalid, setting default value dt = 0.05")
            self.dt = 0.05

    # MISC FUNCTIONS
    def message(self, s):
        self.text.appendPlainText(s)

app = QApplication(sys.argv)

w = MainWindow()
w.show()

app.exec_()