# rappel : "python -m serial.tools.list_ports -v" pour lister les ports com disponibles, et remplacer "com8" ligne 14 par le port com dispo

import serial
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import cProfile  # lib utilisee pour le profiling

from App import App

ser = serial.Serial('com5', 2000000)

app = App()

QtGui.QApplication.processEvents()

while True:
    # for i in range(0, 10000): # pour profiling dans cmd : "python -m cProfile -s cumtime Main2.py" et pour clear terminal : "cls"
    app.readInput(ser)
    app.processInputs()
    app.updatePlotsInfoRobot()
    app.refresh(QtGui)

QtGui.QApplication.processEvents()
# app.exec_()
