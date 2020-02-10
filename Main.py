import serial
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import cProfile  # lib utilisee pour le profiling

from App import App

# remplacer "com8" ligne 10 par le port com utilise. rappel : "python -m serial.tools.list_ports -v" pour lister les ports com disponibles
ser = serial.Serial('com8', 2000000)

app = App()

QtGui.QApplication.processEvents()

while app.isOpen:
    # for i in range(0, 10000): # pour profiling dans cmd : "python -m cProfile -s cumtime Main2.py" et pour clear terminal : "cls"
    app.readInput(ser)
    app.processInputs()
    app.updatePlotsInfoRobot()
    app.refresh(QtGui)

QtGui.QApplication.processEvents()
