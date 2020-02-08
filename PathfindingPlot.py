from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg


class PathfindingPlot:
    def __init__(self):
        self.plotPathfinding = pg.PlotWidget()

        self.plotPathfinding.getPlotItem().setTitle("Pathfinding")

        # creation de la legende
        self.legend = pg.LegendItem(size=(100, 50), offset=(40, 10))
        self.legend.setParentItem(self.plotPathfinding.graphicsItem())
        self.legend.addItem(item=pg.ScatterPlotItem(pen=None, size=10, brush='g', symbol='o'),
                            name="Obstacles")
        self.legend.addItem(item=pg.ScatterPlotItem(pen=None, size=35, brush='r', symbol='o'),
                            name="Robot")

        # creation des recepteurs de donnees
        self.DataObstacles = pg.ScatterPlotItem(pen=None, symbol='o',
                                                symbolPen=None, symbolBrush='r')
        self.DataPositionRobot = pg.ScatterPlotItem(pen=None, symbol='o',
                                                    symbolPen=None, symbolBrush='r')
        self.DataTargetRobot = pg.ScatterPlotItem(pen=None, symbol='o',
                                                  symbolPen=None, symbolBrush='r')
        self.linesRRT = []
        self.linesPath = []
