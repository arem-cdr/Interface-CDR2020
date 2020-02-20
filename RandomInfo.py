from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np


class RandomInfo():
    def __init__(self):
        self.tableWidget = pg.TableWidget()
        self.posInLayout = [2, 2, 1, 1]
        self.tableWidget.setWindowTitle("Random Info")
        self.isOn = False

        self.label = []
        self.data = np.array([[0], [0], [0], [0], [0], [0], [0], [0]])

        self.tableWidget.setData(self.data)

    def processInputs_RandomInfo(self, inputs, debuggingApp):
        if len(inputs) <= 1:
            return

        current = inputs.pop()

        if current == -301:  # entree des donnees
            inputs.reverse()

            self.data = np.array([[inputs[0]]])

            for i in inputs[1:-1]:
                self.data = np.append(self.data, np.array([[i]]), axis=0)

            inputs.clear()
        else:
            inputs.clear()

    def refreshPlot(self):
        self.tableWidget.setData(self.data)
