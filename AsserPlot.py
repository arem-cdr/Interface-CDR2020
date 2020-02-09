from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

from MyPlot import MyPlot


class AsserPlot(MyPlot):
    def __init__(self):
        MyPlot.__init__(self)

        self.posInLayout = [0, 1, 1, 1]
        self.plotPathfinding.getPlotItem().setTitle("Asservissement")

        # creation de la legende
        self.legend = pg.LegendItem(size=(100, 50), offset=(40, 10))

        # creation des variables receptrices des donnees

        # ajout des donnees au plot

        # dimensions du plot
        self.plotPathfinding.setXRange(0, 100)
        self.plotPathfinding.setYRange(0, 30)
