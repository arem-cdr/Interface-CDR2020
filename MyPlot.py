from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg


class MyPlot():
    def __init__(self):
        self.plotPathfinding = pg.PlotWidget()
        self.posInLayout = {0, 0, 1, 1}

        self.plotPathfinding.getPlotItem().setTitle("Default")

    def __getPlot__(self):
        return self.plotPathfinding

    def __getPosInLayout__(self):
        return self.posInLayout
