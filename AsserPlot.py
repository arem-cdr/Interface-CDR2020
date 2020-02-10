from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

from MyPlot import MyPlot


class AsserPlot(MyPlot):
    def __init__(self):
        MyPlot.__init__(self)

        self.posInLayout = [0, 1, 1, 1]
        self.plotWidget.getPlotItem().setTitle("Asservissement")
        # self.plotWidget.addItem(self.plotAsser)

        # creation des variables receptrices des donnees

        # ajout des donnees au plot
        self.xPlot = np.arange(100)
        self.yPlot = np.random.normal(size=(4, 100))

        self.plotRealRight = self.plotWidget.plot(
            self.xPlot, self.yPlot[0], pen=(0, 4))
        self.plotRealLeft = self.plotWidget.plot(
            self.xPlot, self.yPlot[1], pen=(1, 4))
        self.plotCommandRight = self.plotWidget.plot(
            self.xPlot, self.yPlot[2], pen=(2, 4))
        self.plotCommandLeft = self.plotWidget.plot(
            self.xPlot, self.yPlot[3], pen=(3, 4))

        # creation de la legende
        self.legend = pg.LegendItem(size=(100, 50), offset=(40, 10))

        self.legend.setParentItem(self.plotWidget.graphicsItem())
        self.legend.addItem(item=pg.ScatterPlotItem(pen=None, size=10, brush=(200, 200, 200), symbol='s'),
                            name="Test")

        # dimensions du plot
        # self.plotAsser.setXRange(0, 100)
        # self.plotAsser.setYRange(0, 30)

    def processInputs_Pathfinding(self, inputs, debuggingApp):
        if len(inputs) == 0:
            return

        current = inputs.pop()

        if current == -201.0:
            if debuggingApp:
                print("reading speeds")
            spots = []
            self.processInputs_Speeds(inputs, debuggingApp, spots)

        else:
            print("sequence de données inconnue. code de donnée : ", current)
            inputs.clear()

        if len(inputs) > 0:
            print("erreur : les donnees n'ont pas toutes été lues")
            inputs.clear()

    def processInputs_Speeds(self, inputs, debuggingApp, spots):
        if len(self.inputs) == 0:
            print("erreur dans processInputs_Speeds. ID error : 1")
            return

        current = self.inputs.pop()

        if current < 0 or len(self.inputs) == 0:
            if current == -1.0:  # fin de la séquence
                if self.debuggingApp:
                    print("fin de la séquence")
            else:
                print("erreur dans processInputs_Speeds. ID error : 2")
            return

        else:
            current2 = self.inputs.pop()
            if current2 < 0:
                print("erreur dans processInputs_Speeds. ID error : 3")
                self.inputs.append(current2)
                return
            else:
                #self.infoRobot["position"] = [current, current2]
                self.processInputs_RobotPosition()
