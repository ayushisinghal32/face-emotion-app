from PyQt5 import QtWidgets
import sys
import os

from ui import Ui_MainWindow


if __name__ == "__main__":  
    #deleteOldFiles() 
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()   
    ui.app = app   
    app.exec_()
    print("Main End")

