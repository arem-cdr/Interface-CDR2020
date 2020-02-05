# rappel : "python -m serial.tools.list_ports -v" pour lister les ports com disponibles, et remplacer "com8" ligne 14 par le port com dispo

import serial
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
from math import *

# init serial
ser = serial.Serial('com8', 115200)
L = []
# Always start by initializing Qt (only once per application)
app = QtGui.QApplication([])

# Define a top-level widget to hold everything
win = QtGui.QWidget()
win.setWindowTitle("Interface Debug")

plot = pg.PlotWidget()
layout = QtGui.QGridLayout()
win.setLayout(layout)
Data = pg.ScatterPlotItem(pen=None, symbol='o',
                          symbolPen=None, symbolBrush='r')
Curve = pg.PlotCurveItem()
plot.addItem(Data)

plot.setXRange(0, 300)  # dimensions de la taille
plot.setYRange(0, 200)

layout.addWidget(plot)  # plot goes on right side, spanning 3 rows
win.show()

spots = []  # tableau utilisé pour l'affichage des obstacles

while True:
    ser_bytes = ser.readline()
    decoded_byte = 0
    try:
        decoded_byte = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
    except ValueError:
        print("Failed to convert string to float")
    L.insert(0, decoded_byte)
    if (decoded_byte == -1.0):  # -1 : fin d'une séquence

        print("debut sequence reception")

        State = "INIT"
        linesRRT = []

        while len(L) > 0:
            # machine à etat sur la variable State
            if State == "INIT":
                current = L.pop()
                # print(current)
                if current < 0:
                    if current == -101.0:
                        State = "READING OBSTACLES"
                        print("reading obstacles")
                        spots = []
                    elif current == -102.0:
                        State = "READING RRT"
                        print("reading RRT")
                        plot.clear()
                        plot.addItem(Data)
            elif State == "READING OBSTACLES":
                current = L.pop()
                # print(current)
                if current == -1:
                    State = "INIT"
                    print("init state")
                else:
                    current2 = L.pop()
                    # print(current2)
                    if current2 < 0:
                        print("erreur dans reading obstacles")
                    else:
                        spots.append(
                            {'pos': (current2, current), 'size': 10, 'pen': None, 'brush': 'g', 'symbol': 'o'})
            elif State == "READING RRT":
                current = L.pop()
                print("debut lecture RRT")
                # print(current)
                if current == -1:
                    State = "INIT"
                    print("init state")
                else:
                    if len(L) < 3:
                        print("erreur dans reading RRT. ID error : 1")
                    else:
                        current2 = L.pop()
                        current3 = L.pop()
                        current4 = L.pop()
                        # print(current2)
                        # print(current3)
                        # print(current4)
                        if current2 < 0 or current3 < 0 or current4 < 0:
                            print("erreur dans reading RRT. ID error : 2")
                        else:
                            linesRRT.append(pg.LineSegmentROI(
                                [[current2, current], [current4, current3]], pen=(4, 9)))

        Data.setData(spots)  # affichage du contenu de spots sur le plot

        for i in range(0, len(linesRRT)):
            plot.addItem(linesRRT[i])
        L.clear()  # au cas où il ne soit pas vide, lais normalement c'est deja le cas
        linesRRT.clear()
    QtGui.QApplication.processEvents()

QtGui.QApplication.processEvents()
app.exec_()
