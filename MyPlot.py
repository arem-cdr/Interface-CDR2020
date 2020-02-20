from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg


class MyPlot():
    def __init__(self):
        self.plotWidget = pg.PlotWidget()
        self.posInLayout = [0, 0, 1, 1]
        self.plotWidget.getPlotItem().setTitle("Default")
