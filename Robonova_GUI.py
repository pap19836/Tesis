from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QPlainTextEdit,
                                QVBoxLayout, QWidget)
from PyQt5.QtCore import QProcess
import sys
import re

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
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)

        l = QVBoxLayout()
        l.addWidget(self.StartSimulationBtn)
        l.addWidget(self.GetDataBtn)
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
            self.p.start("python3", ['pybullet_simulation.py'])

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
            stdout2_list= list(stdout2.strip('][').split(", "))
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



app = QApplication(sys.argv)

w = MainWindow()
w.show()

app.exec_()