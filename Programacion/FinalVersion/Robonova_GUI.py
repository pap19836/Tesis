#!C:\Users\stefa\OneDrive - Universidad del Valle de Guatemala\UVG\Tesis\Programacion\tesis_env\Scripts\python.exe"
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QPlainTextEdit, QCheckBox, QDial, QLabel,
                             QWidget, QInputDialog, QFileDialog,
                             QVBoxLayout, QHBoxLayout, QGridLayout,
                             QMessageBox, QButtonGroup, QRadioButton)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
import sys
import csv
import threading
import pybullet_simulation as pb_sim
import GUI_Functions
import time
from numpy import deg2rad,rad2deg, arange, fromstring, round
import os as os
from functools import partial
from scipy import interpolate
from shutil import rmtree
pb_sim.servoValues = round(deg2rad([0,0,-45,0,0,
                                           -60,0,0,0,0,
                                           45,0,0,-60,0,0]),3)
t1 = threading.Thread(target=pb_sim.pb,args=())
t1.start()
time.sleep(2)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Programa de Control - Robonova-1")
        self.dt = 0.05
        ########## SENDING AND RECEIVING POSITION BUTTONS ##########
        # Design
        # Obsolete SendData & GetData
        # self.GetDataBtn = QPushButton("Get Data")
        # self.SendDataBtn = QPushButton("Send Data")
        self.connectCB = QCheckBox("Connect to Robonova")
        self.checkConnectionTimer = QTimer()
        # Connect
        # self.GetDataBtn.pressed.connect(self.getData)
        # self.SendDataBtn.pressed.connect(self.sendData)
        self.connectCB.stateChanged.connect(self.connectRobonva)
        self.checkConnectionTimer.timeout.connect(self.checkConnection)
        
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
        self.replacePositionBtn = QPushButton("Replace current position")
        self.removePositionBtn = QPushButton("Remove current position")
        self.addNextPositionBtn = QPushButton("Add as next position")
        self.clearCoreoBtn = QPushButton("Clear choreography")
        self.deleteCoreoBtn = QPushButton("Delete choreography File")
        self.playCoreoBtn = QPushButton("Play choreography")
        self.uploadCoreoBtn = QPushButton("Upload choreography")

        self.whereBtnGroupWidget =QWidget()
        self.simCoreoBtn = QRadioButton("Only on simulation")
        self.playRealCoreoFlag = False
        self.simCoreoBtn.setChecked(True)
        self.bothCoreoBtn = QRadioButton("Both Simulation and Robot")
        self.smoothTrajectoryCB = QCheckBox("Smooth trajectory")
        self.dtlabel = QLabel("dt")
        self.dtvalue = QPlainTextEdit()
        self.dtbutton = QPushButton("Set")
        self.repeatCoreoCB = QCheckBox("Repeat choreography")
        self.currentCoreoLabel = QLabel("Current choreography:")
        # Customize
        self.newCoreoBtn.setFont(btnFont)
        self.loadCoreoBtn.setFont(btnFont)
        self.replacePositionBtn.setFont(btnFont)
        self.removePositionBtn.setFont(btnFont)
        self.addNextPositionBtn.setFont(btnFont)
        self.clearCoreoBtn.setFont(btnFont)
        self.deleteCoreoBtn.setFont(btnFont)
        self.playCoreoBtn.setFont(btnFont)
        self.uploadCoreoBtn.setFont(btnFont)
        self.uploadCoreoBtn.setFixedSize(270,40)
        self.uploadCoreoBtn.setEnabled(False)
        self.simCoreoBtn.setCheckable(True)
        self.bothCoreoBtn.setCheckable(True)
        self.dtvalue.setFixedSize(50,25)
        self.dtbutton.setFixedSize(50,25)
        self.whereBtnGroup = QButtonGroup(self.whereBtnGroupWidget)
        self.whereBtnGroup.addButton(self.simCoreoBtn,1)
        self.whereBtnGroup.addButton(self.bothCoreoBtn,2)
        # Connect
        self.newCoreoBtn.pressed.connect(self.newCoreo)
        self.loadCoreoBtn.pressed.connect(self.loadCoreo)
        self.replacePositionBtn.pressed.connect(self.replacePosition)
        self.removePositionBtn.pressed.connect(self.removePosition)
        self.addNextPositionBtn.pressed.connect(self.addPosition)
        self.clearCoreoBtn.pressed.connect(self.clearCoreo)
        self.deleteCoreoBtn.pressed.connect(self.deleteCoreo)
        self.playCoreoBtn.pressed.connect(
            partial(self.playCoreo, buttonPressed = True))
        self.uploadCoreoBtn.pressed.connect(self.uploadCoreo)
        self.repeatCoreoCB.stateChanged.connect(
            partial(self.playCoreo, buttonPressed = False))
        # self.simCoreoBtn.pressed.connect(self.whereToPlay)
        # self.bothCoreoBtn.pressed.connect(self.whereToPlay)
        self.dtbutton.pressed.connect(self.setdt)
        self.whereBtnGroup.buttonClicked.connect(self.whereToPlay)

        # Layout
        coreoLayout1 = QGridLayout()
        coreoLayout1.addWidget(self.newCoreoBtn, 0, 0)
        coreoLayout1.addWidget(self.loadCoreoBtn, 0, 1)
        coreoLayout1.addWidget(self.addNextPositionBtn, 1, 0, 1, 2)
        coreoLayout1.addWidget(self.replacePositionBtn, 2, 0)
        coreoLayout1.addWidget(self.removePositionBtn, 2, 1)
        coreoLayout1.addWidget(self.clearCoreoBtn, 3, 0)
        coreoLayout1.addWidget(self.deleteCoreoBtn, 3, 1)
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
        coreoLayout3 = QHBoxLayout()
        coreoLayout3.addWidget(self.simCoreoBtn)
        coreoLayout3.addWidget(self.bothCoreoBtn)
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
        #Widgets
        imgTitle = QLabel("Current step preview:")
        self.stepImg = QLabel()
        self.prevImgBtn = QPushButton("<<")
        self.currentImgNumLabel = QLabel("x of x")
        self.nextImgBtn = QPushButton(">>")
        # Customize
        try:
            if self.currentStepNum==1:
                self.prevImgBtn.setEnabled(False)
            if self.currentStepNum==self.totalSteps:
                self.nextImgBtn.setEnabled(False)
        except(AttributeError):
            self.stepImg.setText("No Preview")
            self.stepImg.setFont(btnFont)
            self.prevImgBtn.setEnabled(False)
            self.nextImgBtn.setEnabled(False)
        # Connect
        self.prevImgBtn.pressed.connect(self.prevImg)
        self.nextImgBtn.pressed.connect(self.nextImg)
        # Step images
        # stepImg = cv2.imread("Programacion\FinalVersion\RobonovaWalking.png")
        # stepImg = cv2.cvtColor(stepImg, cv2.COLOR_BGR2RGB)
        # h, w, ch = stepImg.shape
        # bpl = w*ch
        # qImg = QImage(stepImg.data, w, h, bpl, QImage.Format_RGB888)
        # self.stepImg = QLabel()
        # self.stepImg.setPixmap(QPixmap(qImg).scaled(self.imgW,self.imgH))
        
        # Layout
        imgBtnLayout = QHBoxLayout()
        imgBtnLayout.addWidget(self.prevImgBtn,2)
        imgBtnLayout.addWidget(self.currentImgNumLabel,1)
        imgBtnLayout.addWidget(self.nextImgBtn,2)
        imgLayout = QVBoxLayout()
        imgLayout.addWidget(imgTitle)
        imgLayout.addWidget(self.stepImg,alignment=Qt.AlignCenter)
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
        if self.connectCB.isChecked():
            self.uploadCoreoBtn.setEnabled(True)
            self.bothCoreoBtn.setEnabled(True)
        else:
            self.uploadCoreoBtn.setEnabled(False)
            self.bothCoreoBtn.setEnabled(False)
        pb_sim.activeConnection = self.connectCB.isChecked()
        self.checkConnectionTimer.start(1000)
    def checkConnection(self):
        if(self.connectCB.isChecked()) & (pb_sim.connected !=True):
            self.connectCB.setChecked(False)
            self.message("Robonova disconnected, try reconnecting")
        self.checkConnectionTimer.start(1000)
    # DIAL FUNCTIONS
    def updateDial(self,a):
        dialValue =self.dialSubLayout[a].itemAt(0).widget().value()
        valueLabel =self.dialSubLayout[a].itemAt(1).itemAt(1).widget()
        valueLabel.setText(str(dialValue))
        pb_sim.servoValues[a] = round(deg2rad(dialValue),3)

    # choreography FUNCTIONS
    def newCoreo(self):
        parentPath = os.getcwd()
        parentPath = parentPath+'/Rutinas'
        self.x = QFileDialog()
        self.filename = self.x.getSaveFileName(filter="CSV Files (*.csv)")
        try:
            f = open(self.filename[0], "a")
            f.close()
            dirName = os.path.basename(self.filename[0]).split(".")[0]
            self.currentCoreoDir = os.path.join(parentPath,dirName)
            os.makedirs(self.currentCoreoDir)
            self.newFilePath = self.currentCoreoDir+"/"+os.path.basename(self.filename[0])
            self.newFilePath = self.newFilePath.replace("\\","/")
            os.rename(self.filename[0],self.newFilePath)
            if self.newFilePath != "":
                self.currentCoreoName = os.path.basename(self.newFilePath)
                self.currentCoreoFile = self.newFilePath
                self.totalSteps = 0
                self.currentStepNum = 0
                self.stepImg.setText("No Preview")
                GUI_Functions.enableImgBtns(self)
                self.currentImgNumLabel.setText("{} of {}".format(str(self.currentStepNum),str(self.totalSteps)))
                self.currentCoreoLabel.setText(
                    "Current choreography: " + self.currentCoreoName)
            else:
                pass
        except:
            pass

    def loadCoreo(self):
        self.x = QFileDialog()
        self.filename = self.x.getOpenFileName(filter="CSV Files (*.csv)")
        if self.filename[0] != "":
            self.currentCoreoFile = self.filename[0]
            with open(self.currentCoreoFile,"r+") as csvfile:
                lines = csvfile.readlines()
                self.coreoPositions = []
                updatedlines = []
                for line in lines:
                    if line == "\n":
                        continue
                    updatedlines.append(line)
                self.coreoPositions = updatedlines
                for i in range(len(self.coreoPositions)):
                    self.coreoPositions[i] = fromstring(self.coreoPositions[i],sep=",")
            self.totalSteps = len(updatedlines)
            self.currentStepNum = self.totalSteps
            self.currentCoreoDir = self.currentCoreoFile.replace("\\","/").rsplit("/",1)[0]
            try:
                GUI_Functions.showImg(self)
            except:
                self.stepImg.setText("No Preview")  
                self.currentImgNumLabel.setText("{} of {}".format(str(self.currentStepNum),str(self.totalSteps)))  
            self.currentCoreoName = os.path.basename(self.filename[0])
            self.currentCoreoLabel.setText(
                "Current choreography: " + self.currentCoreoName)
        else:
            pass
    def addPosition(self):
        try:
            with open(self.currentCoreoFile, "r+") as csvfile:
                lines = csvfile.readlines()
                updatedlines = []
                for line in lines:
                    if line == "\n":
                        continue
                    line = list(line.split('\n')[0].split(','))
                    updatedlines.append(line)
                newValues = pb_sim.servoValues
                newValues = [str(x) for x in newValues]
                updatedlines.insert(self.currentStepNum,newValues)
                lines = ""
                csvfile.truncate(0)
                csvfile.writelines(lines)
            with open(self.currentCoreoFile, "w+",newline='') as csvfile:
                writer = csv.writer(csvfile)
                for line in updatedlines:
                    writer.writerow(line)
                self.totalSteps = len(updatedlines)
            with open(self.currentCoreoFile, "r+") as csvfile:
                reader = csv.reader(csvfile)
                self.coreoPositions = []
                for line in reader:
                    if not line:
                        continue
                    self.coreoPositions.append(line)
            self.currentStepNum += 1
            for i in reversed(range(self.currentStepNum,self.totalSteps)):
                oldName = self.currentCoreoDir+"/step"+str(i)+".png"
                newName = self.currentCoreoDir+"/step"+str(i+1)+".png"
                os.rename(oldName,newName)
            GUI_Functions.renderImg(self)

            self.message("Position saved to choreography!")
        except (FileNotFoundError, AttributeError) as err:
            print(err)
            self.message("Choreography does not exist or has not been selected")
    def removePosition(self):
        try:
            with open(self.currentCoreoFile, "r+") as csvfile:
                lines = csvfile.readlines()
                updatedlines = []
                for line in lines:
                    if line == "\n":
                        continue
                    updatedlines.append(line)
                updatedlines.pop(self.currentStepNum-1) #starts at 0
                lines = ""
                csvfile.truncate(0)
                csvfile.writelines(lines)
            with open(self.currentCoreoFile, "w+") as csvfile:
                csvfile.writelines(updatedlines)
                self.totalSteps = len(updatedlines)
            with open(self.currentCoreoFile, "r+") as csvfile:
                reader = csv.reader(csvfile)
                self.coreoPositions = []
                for line in reader:
                    if not line:
                        continue
                    self.coreoPositions.append(line)
            os.remove(self.currentCoreoDir+"/step"+str(self.currentStepNum)+".png")
            if self.currentStepNum < self.totalSteps:
                for i in range(self.currentStepNum,self.totalSteps+1):
                    oldName = self.currentCoreoDir+"/step"+str(i+1)+".png"
                    newName = self.currentCoreoDir+"/step"+str(i)+".png"
                    os.rename(oldName,newName)
            else:
                self.currentStepNum -= 1
            if self.totalSteps == 0:
                self.stepImg.setText("No Preview")
            else:
                GUI_Functions.showImg(self)
            self.currentImgNumLabel.setText("{} of {}".format(str(self.currentStepNum),str(self.totalSteps)))
            self.message("Position removed from coreograhy!")
        except (FileNotFoundError, IndexError) as err:
            if isinstance(err,FileNotFoundError):
                self.message("Choreography does not exist or has not been selected")
            elif isinstance(err,IndexError) or isinstance(err,PermissionError):
                self.message("Choreography is already empty!")
            else:
                self.message("Unknown Error")
    def replacePosition(self):
        try:
            with open(self.currentCoreoFile, "r+") as csvfile:
                lines = csvfile.readlines()
                updatedlines = []
                for line in lines:
                    if line == "\n":
                        continue
                    line = list(line.split('\n')[0].split(','))
                    updatedlines.append(line)
                newValues = pb_sim.servoValues
                newValues = [str(x) for x in newValues]
                updatedlines[self.currentStepNum-1] = newValues
                lines = ""
                csvfile.truncate(0)
                csvfile.writelines(lines)
            with open(self.currentCoreoFile, "w+",newline='') as csvfile:
                writer = csv.writer(csvfile)
                for line in updatedlines:
                    writer.writerow(line)
                self.totalSteps = len(updatedlines)
            with open(self.currentCoreoFile, "r+") as csvfile:
                reader = csv.reader(csvfile)
                self.coreoPositions = []
                for line in reader:
                    if not line:
                        continue
                    self.coreoPositions.append(line)
            GUI_Functions.renderImg(self)
            self.message("Position has been replaced!")
        except (FileNotFoundError, IndexError, PermissionError, AttributeError) as err:
            if isinstance(err,FileNotFoundError)or isinstance(err,AttributeError):
                self.message("Choreography does not exist or has not been selected")
            elif isinstance(err,IndexError) or isinstance(err,PermissionError):
                self.message("Choreography is already empty!")
            else:
                self.message("Unknown Error")
    def clearCoreo(self):
        reply = QMessageBox.warning(self, 'Clear Choreography',
        'Are you sure you want clear all steps in this choreography?',
        QMessageBox.Ok | QMessageBox.Cancel)
        
        if reply == QMessageBox.Ok:
            try:
                with open(self.currentCoreoFile,"r+") as csvfile:
                    lines = ""
                    csvfile.truncate(0)
                    csvfile.writelines(lines)
                for i in range(self.totalSteps):
                    os.remove(self.currentCoreoDir+"/step"+str(i+1)+".png")
                self.totalSteps = 0
                self.currentStepNum = 0
                self.stepImg.setText("No Preview")
                self.currentImgNumLabel.setText("{} of {}".format(str(self.currentStepNum),str(self.totalSteps)))
                self.message("Choreography cleared!")
            except (FileNotFoundError, AttributeError):
                self.message("Choreography does not exist or has not been selected")
    def deleteCoreo(self):
        reply = QMessageBox.warning(self, 'Clear Choreography', 
                'Are you sure you want to delete this choreography?',
                QMessageBox.Ok | QMessageBox.Cancel)
        if reply == QMessageBox.Ok:
            try:
                rmtree(self.currentCoreoDir)
                self.message("Choreography has been deleted!")
                self.currentCoreoLabel.setText("Current choreography: ")
                self.totalSteps = 0
                self.currentStepNum = 0
                self.stepImg.setText("No Preview")
                self.currentImgNumLabel.setText("{} of {}".format(str(self.currentStepNum),str(self.totalSteps)))
            except (FileNotFoundError, AttributeError):
                self.message("Choreography does not exist or has not been selected")
        
    t2stop = threading.Event()
    repeating = False
    def playCoreo(self, **buttonPressed):
        #self.dt = 0.05
        try:
            with open(self.currentCoreoFile, "r+") as csvfile:
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
                pb_sim.controlFlag = False
                if (self.repeatCoreoCB.isChecked() 
                    and not(self.t2.is_alive())) == True:
                    self.message("Playing choreography...")
                    self.repeating = True
                    pb_sim.repeatCB = True
                    self.t2stop.clear()
                    self.t2.start()
                else:
                    self.message("Playing choreography...")
                    self.t2stop.set()
                    self.t2.start()
                    self.message("Choreography done!")
                if self.playRealCoreoFlag:
                    pb_sim.playRealCoreo = True


            if (not(self.repeatCoreoCB.isChecked()) 
                and self.repeating) == True:
                self.repeating = False
                pb_sim.repeatCB = False
                self.t2stop.set()
                self.message("Choreography done!")
        except (FileNotFoundError,IndexError) as err:
            if(isinstance(err,FileNotFoundError)):
                self.message("Choreography does not exist or has not been selected")
            elif(isinstance(err,IndexError)):
                self.message("Cannot play empty choreography")
    def whereToPlay(self):
        if (self.simCoreoBtn.isChecked()) and not(self.bothCoreoBtn.isChecked()):
            #pass
            self.playRealCoreoFlag = False
        else:
            #pass
            if pb_sim.coreoExists:
                self.playRealCoreoFlag = True
            else:
                self.simCoreoBtn.setChecked(True)
                self.message("No choreography in robot. Try Upload choreography")
    def uploadCoreo(self):
    
        try:
            with open(self.currentCoreoFile, "r+") as csvfile:
                reader = csv.reader(csvfile)
                self.coreoPositions = []
                for line in reader:
                    if not line:
                        continue
                    self.coreoPositions.append(line)
                l = len(self.coreoPositions)
            
            if self.smoothTrajectoryCB.isChecked():
                t = len(self.coreoPositions)-1
                x = range(len(self.coreoPositions))
                y = self.coreoPositions
                cs = interpolate.make_interp_spline(x,y, 1)
                xs = arange(0,t,self.dt)
                self.coreoPositions = cs(xs)
                l = len(self.coreoPositions)
            
            if (l > 200):
                reply = QMessageBox.critical(self, 'Too Long', 
                    'The choreography is too long! Try increasing "dt" or decresing the amount of steps in the choreography',
                    QMessageBox.Ok)
            else:
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

    # Image Functions
    def nextImg(self):
        self.currentStepNum += 1
        GUI_Functions.showImg(self)
        currentPosition = [float(x) for x in self.coreoPositions[self.currentStepNum-1]]
        for a in range(len(self.dials)):
                dialValue =self.dials[a].setValue(int(rad2deg(currentPosition[a])))
    def prevImg(self):
        self.currentStepNum -= 1
        GUI_Functions.showImg(self)
        currentPosition = [float(x) for x in self.coreoPositions[self.currentStepNum-1]]
        for a in range(len(self.dials)):
                dialValue =self.dials[a].setValue(int(rad2deg(currentPosition[a])))
    # MISC FUNCTIONS
    def message(self, s):
        self.text.appendPlainText(s)

app = QApplication(sys.argv)

w = MainWindow()
w.show()

app.exec_()