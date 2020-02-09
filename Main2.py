# rappel : "python -m serial.tools.list_ports -v" pour lister les ports com disponibles, et remplacer "com8" ligne 14 par le port com dispo

import serial
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy
import time
from math import *

from App import App

# init serial
ser = serial.Serial('com8', 2000000)

app = App()

while True:
    QtGui.QApplication.processEvents()
    app.readInput(ser)
    app.processInputs()
    app.updatePlotsInfoRobot()
    app.refresh()

QtGui.QApplication.processEvents()
app.exec_()
