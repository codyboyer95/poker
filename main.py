
from Game import Game
#from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PySide2 import QtCore
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

# Only needed for access to command line arguments
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1300, 800)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # You need one (and only one) QApplication instance per application.
    # Pass in sys.argv to allow command line arguments for your app.
    # If you know you won't use command line arguments QApplication([]) works too.
    app = QApplication(sys.argv)

    window = QMainWindow()
    window.show()

    # Start the event loop.
    app.exec_()



