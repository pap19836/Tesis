from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton,
                             QPlainTextEdit, QCheckBox, QDial, QLabel,
                             QWidget,
                             QVBoxLayout, QHBoxLayout, QGridLayout)
from PyQt5.QtCore import (Qt)
from numpy import rad2deg, ceil
def addDial(self, name, lower_limit, upper_limit):
    # Dial Widget
    self.dial = QDial()
    self.dial.setRange(lower_limit, upper_limit)

    # Limits layout/widget
    self.LowerLimitLabel = QLabel(str(lower_limit))
    self.UpperLimitLabel = QLabel(str(upper_limit))
    self.ValueLabel = QLabel(str(self.dial.value()))

    labelFont = self.LowerLimitLabel.font()
    labelFont.setPointSize(10)
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
    
    # Layout
    dial_layout = QVBoxLayout()
    dial_layout.addWidget(self.dial)
    dial_layout.addLayout(LabelsLayout)
    dial_layout.addWidget(self.dial_name)

    def updateDialValue(self):
        print("a")

    return dial_layout

def creatDials(self, info:list):
    dial_list = []
    for i in range(len(info)):
        dial = addDial(self,str(info[i][1],"utf-8"),
                       round(rad2deg(info[i][8])),
                       round(rad2deg(info[i][9])))
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