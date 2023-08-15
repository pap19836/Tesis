from PyQt5.QtWidgets import QApplication, QWidget

# You need one (and only one) QApplication instance per application.
app = QApplication([])

# Create a Qt widget, which will be our window.
window = QWidget()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()

