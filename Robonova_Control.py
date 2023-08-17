# Import other .py files of the program
import Robonova_GUI as gui

# Import PyQt
from PyQt5.QtWidgets import QApplication

app = QApplication([])
w = gui.MainWindow()
w.show()

app.exec_()