#!C:\Users\stefa\OneDrive - Universidad del Valle de Guatemala\UVG\Tesis\Programacion\tesis_env\Scripts\python.exe"
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QPlainTextEdit, QCheckBox,
                                QVBoxLayout, QWidget)
from PyQt5.QtCore import QProcess
import sys
import re
def GUI():
    global servoValues
    servoValues = None
    global data
    data = []
    class MainWindow(QMainWindow):

        def __init__(self):
            super().__init__()

            self.p = None

            self.StartSimulationBtn = QPushButton("Start Simulation")
            self.StartSimulationBtn.pressed.connect(self.start_process)
            self.GetDataBtn = QPushButton("Get Data")
            self.GetDataBtn.pressed.connect(self.saveData)
            self.connectCB = QCheckBox("Connect to Robonova")
            self.connectCB.stateChanged.connect(self.connectRobonva)
            self.text = QPlainTextEdit()
            self.text.setReadOnly(True)

            l = QVBoxLayout()
            l.addWidget(self.StartSimulationBtn)
            l.addWidget(self.GetDataBtn)
            l.addWidget(self.connectCB)
            l.addWidget(self.text)

            w = QWidget()
            w.setLayout(l)

            self.setCentralWidget(w)

        def message(self, s):
            self.text.appendPlainText(s)

        def start_process(self):
            if self.p is None:  # No process running.
                self.message("Executing process")
                self.p = QProcess()  # Keep a reference to the QProcess (e.g. on self) while it's running.
                self.p.readyReadStandardOutput.connect(self.handle_stdout)
                self.p.readyReadStandardError.connect(self.handle_stderr)
                self.p.stateChanged.connect(self.handle_state)
                self.p.finished.connect(self.process_finished)  # Clean up once complete.
                self.p.start("python.exe", ['Programacion/FinalVersion/pybullet_simulation.py'])

        def handle_stderr(self):
            data = self.p.readAllStandardError()
            stderr = bytes(data).decode("utf8")
            self.message(stderr)

        def handle_stdout(self):
            data = self.p.readAllStandardOutput()
            stdout = bytes(data).decode("utf8")
            stdout2 = re.search('(?<=split).*',stdout)
            if stdout2 != None:
                stdout2 = stdout2.group()
                stdout2_list= list(stdout2.strip().strip('][').split(", "))
                global servoValues
                servoValues = [eval(i) for i in stdout2_list]

        def handle_state(self, state):
            states = {
                QProcess.NotRunning: 'Not running',
                QProcess.Starting: 'Starting',
                QProcess.Running: 'Running',
            }
            state_name = states[state]
            self.message(f"State changed: {state_name}")

        def process_finished(self):
            self.message("Process finished.")
            self.p = None

        def saveData(self):
            global data
            data.append(servoValues)
            self.message(str(servoValues))
        def connectRobonva(self):
            robonova = self.connectCB.isChecked()
            a = self.p.write(b"robonova\n")
            b = 1



    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    app.exec_()
global a
a = 5
def pb():
    import pybullet
    import pybullet_data
    import math
    from numpy import rad2deg
    # IP Socket Config
    import socket
    from time import sleep
    import json
    s = socket.socket()
    ip = '192.168.122.32'
    port = 8091

    # isConnected = input("testing")
    # if isConnected=="robonova":
    s.connect((ip,port))

    # Connect to simulation
    pybullet.connect(pybullet.GUI)
    pybullet.resetSimulation()

    # Set plane in simulation
    pybullet.setAdditionalSearchPath(pybullet_data.getDataPath())
    plane = pybullet.loadURDF("plane.urdf")


    # Load robot URDF
    robot = pybullet.loadURDF("Programacion/FinalVersion/robonova/robot.urdf",[0,0,0.3],useFixedBase=1)

    # Get Robot info and set sliders
    position, orientation = pybullet.getBasePositionAndOrientation(robot)
    numJoints = pybullet.getNumJoints(robot)
    joints_info = []
    slider_parameters = []
    for i in range(numJoints):
        x = pybullet.getJointInfo(robot,i)
        joints_info.append(x)
        y = pybullet.addUserDebugParameter(' '+str(joints_info[i][1], 'utf-8'),joints_info[i][8],joints_info[i][9], 0)
        slider_parameters.append(y)
    joint_number = list(range(numJoints))

    joint_dict = {}
    for i in joint_number:
        joint_dict[joints_info[i][1].decode("utf-8")] = None
    # Initialize Simulation
    pybullet.setGravity(0,0,-9.81)
    pybullet.setTimeStep(0.0001)
    pybullet.setRealTimeSimulation(1)
    old_slider_values = 0
    # Run Simulation
    while True:
        pybullet.stepSimulation()
        slider_values = []
        for i in range(numJoints):
            x = pybullet.readUserDebugParameter(i)
            slider_values.append(x)
        pybullet.setJointMotorControlArray(robot,joint_number,pybullet.POSITION_CONTROL, slider_values)
        global a
        print(a)
        if slider_values != old_slider_values:
            old_slider_values = slider_values
            joint_dict.update({'LeftShoulder1':int(rad2deg(slider_values[0]))+90,
            'LeftShoulder2':int(rad2deg(slider_values[1]))+90,
            'RightShoulder1':int(rad2deg(slider_values[2]))+90,
            'RightShoulder2':int(rad2deg(slider_values[3]))+90,
            'LeftWaist':int(rad2deg(slider_values[4]))+90,
            'LeftHip1':int(rad2deg(slider_values[5]))+90,
            'LeftHip2':int(rad2deg(slider_values[6]))+90,
            'LeftKnee':int(rad2deg(slider_values[7]))+90,
            'LeftAnkle1':int(rad2deg(slider_values[8]))+90,
            'LeftAnkle2':int(rad2deg(slider_values[9]))+90,
            'RightWaist':int(rad2deg(slider_values[10]))+90,
            'RightHip1':int(rad2deg(slider_values[11]))+90,
            'RightHip2':int(rad2deg(slider_values[12]))+90,
            'RightKnee':int(rad2deg(slider_values[13]))+90,
            'RightAnkle1':int(rad2deg(slider_values[14]))+90,
            'RightAnkle2':int(rad2deg(slider_values[15]))+90})

            data_json = json.dumps(joint_dict)
        
        
            s.sendall(bytes(data_json, "utf-8"))
            print('split'+str(slider_values))