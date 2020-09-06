from .app import MainWindow
from PyQt5 import QtWidgets
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    app.exec_()