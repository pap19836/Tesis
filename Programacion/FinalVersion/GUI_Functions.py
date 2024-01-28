from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QPlainTextEdit, QCheckBox, QDial, QLabel,
                             QWidget,
                             QVBoxLayout, QHBoxLayout, QGridLayout)
from PyQt5.QtCore import (Qt)
from PyQt5.QtGui import QImage, QPixmap
from numpy import rad2deg, ceil, reshape
import pybullet_simulation as pb_sim
import pybullet
import time
import cv2
def addDial(self, name, lower_limit, upper_limit, initial_value, num):
    # Dial Widget
    self.dial = QDial()
    self.dial.setRange(lower_limit, upper_limit)
    self.dial.setValue(initial_value)
    # Limits layout/widget
    self.LowerLimitLabel = QLabel(str(lower_limit))
    self.UpperLimitLabel = QLabel(str(upper_limit))
    self.ValueLabel = QLabel(str(self.dial.value()))

    labelFont = self.LowerLimitLabel.font()
    labelFont.setPointSize(12)
    self.LowerLimitLabel.setFont(labelFont)
    self.UpperLimitLabel.setFont(labelFont)
    self.ValueLabel.setFont(labelFont)

    LabelsLayout = QHBoxLayout()
    LabelsLayout.addWidget(self.LowerLimitLabel)
    LabelsLayout.addWidget(self.ValueLabel)
    LabelsLayout.addWidget(self.UpperLimitLabel)
    LabelsLayout.setAlignment(Qt.AlignHCenter)
    LabelsLayout.setSpacing(32)

    # Name Widget
    self.dial_name = QLabel(name)
    nameFont = self.dial_name.font()
    nameFont.setPointSize(15)
    self.dial_name.setFont(nameFont)
    self.dial_name.setAlignment(Qt.AlignHCenter)
    
    # Main Layout
    dial_layout = QVBoxLayout()
    dial_layout.addWidget(self.dial)
    dial_layout.addLayout(LabelsLayout)
    dial_layout.addWidget(self.dial_name)

    return dial_layout

def creatDials(self, info:list):
    dial_list = []
    for i in range(len(info)):
        dial = addDial(self,str(info[i][1],"utf-8"),
                       round(rad2deg(info[i][8])),
                       round(rad2deg(info[i][9])),
                       int(rad2deg(pb_sim.servoValues[i])),
                       i)
        dial_list.append(dial)
    return dial_list

def dialsLayout(LayoutList):
    layout = QGridLayout()
    i = 0
    rows = 2
    columns = int(ceil(len(LayoutList)/2))
    for j in range(rows):
        for i in range(columns):
            if j < 1:
                layout.addLayout(LayoutList[i],j,i)
            else:
                layout.addLayout(LayoutList[i+columns],j,i)
    return layout

def repeatCoreo(self,rows,stop_event,smooth,dt):
    while True:
        pb_sim.controlFlag = False
        for i in range(len(rows)):
            coreoPosition = [float(x) for x in rows[i] ]
            pb_sim.servoValues = coreoPosition
            for i in range(pb_sim.numJoints):
                x = pb_sim.servoValues[i]
                pb_sim.servo2.append(x)
            pb_sim.old_servo_values = pb_sim.servo2
            if smooth:
                time.sleep(dt/10)
            else:
                time.sleep(0.1)
        if stop_event.is_set():
            for a in range(len(coreoPosition)):
                dialValue =self.dials[a].setValue(int(rad2deg(coreoPosition[a])))
            for i in range(pb_sim.numJoints):
                x = pb_sim.servoValues[i]
                pb_sim.servo2.append(x)
            pb_sim.old_servo_values = pb_sim.servo2
            pb_sim.controlFlag = True
            #self.currentStepNum = len(rows)
            break

def renderImg(self):
    w = 480
    h = 360
    ch = 4
    vm = pb_sim.vm
    pm = pb_sim.pm
    images = pybullet.getCameraImage(w, h, viewMatrix=vm,
                                        projectionMatrix=pm)
    rgbSave = reshape(images[2],(h,w,ch))
    imgName = self.currentCoreoDir+"/step"+str(self.currentStepNum)+".png"
    cv2.imwrite(imgName,cv2.cvtColor(rgbSave,cv2.COLOR_RGBA2BGRA))
    showImg(self)

def showImg(self):
    imgName = self.currentCoreoDir+"/step"+str(self.currentStepNum)+".png"
    stepImg = cv2.imread(imgName)
    stepImg = cv2.cvtColor(stepImg, cv2.COLOR_BGRA2RGBA)
    w = stepImg.shape[1]
    h = stepImg.shape[0]
    ch = stepImg.shape[2]
    bpl = w*ch
    stepImg = QImage(stepImg, w, h, bpl, QImage.Format_RGBA8888)
    stepPixMap = QPixmap(stepImg)
    self.stepImg.setPixmap(stepPixMap.scaled(480,360))
    self.currentImgNumLabel.setText("{} of {}".format(str(self.currentStepNum),str(self.totalSteps)))
    enableImgBtns(self)

def enableImgBtns(self):
    if (self.currentStepNum==1) or (self.currentStepNum==0):
        self.prevImgBtn.setEnabled(False)
    else:
        self.prevImgBtn.setEnabled(True)
    if (self.currentStepNum==self.totalSteps) or (self.totalSteps==0):
        self.nextImgBtn.setEnabled(False)
    else:
        self.nextImgBtn.setEnabled(True)