from PyQt5.QtWidgets import QApplication
from mainwindow import Ui
import sys

if __name__ == '__main__':
    #application initialisation
    app = QApplication(sys.argv)
    #initialisation of the ui
    ui = Ui()
    #application running
    app.exec_()