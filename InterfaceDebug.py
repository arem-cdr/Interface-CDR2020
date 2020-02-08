
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg


class InterfaceDebug:
    def __init__(self):
        self.app = QtGui.QApplication([])
        self.win = QtGui.QWidget()
        self.win.setWindowTitle("Interface Debug")
        self.layout = QtGui.QGridLayout()
        self.win.setLayout(self.layout)
