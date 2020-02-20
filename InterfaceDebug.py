
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

from PathfindingPlot import PathfindingPlot
from AsserPlot import AsserPlot
from RandomInfo import RandomInfo


class InterfaceDebug:
    def __init__(self):
        self.app = QtGui.QApplication([])
        self.win = QtGui.QWidget()
        self.win.setWindowTitle("Interface Debug")
        self.layout = QtGui.QGridLayout()
        self.win.setLayout(self.layout)

        # creation des graphiques
        self.pathfindingPlot = PathfindingPlot()
        self.asserPlot = AsserPlot()
        self.randomInfo = RandomInfo()

        self.pauseButton = QtGui.QPushButton("Pause")
        self.pauseButton.setCheckable(True)

        # ajout des graphiques au layout
        self.layout.addWidget(
            self.pathfindingPlot.plotWidget,
            self.pathfindingPlot.posInLayout[0],
            self.pathfindingPlot.posInLayout[1],
            self.pathfindingPlot.posInLayout[2],
            self.pathfindingPlot.posInLayout[3])
        self.layout.addWidget(
            self.asserPlot.plotWidget,
            self.asserPlot.posInLayout[0],
            self.asserPlot.posInLayout[1],
            self.asserPlot.posInLayout[2],
            self.asserPlot.posInLayout[3])
        self.layout.addWidget(
            self.randomInfo.tableWidget,
            self.randomInfo.posInLayout[0],
            self.randomInfo.posInLayout[1],
            self.randomInfo.posInLayout[2],
            self.randomInfo.posInLayout[3])

        self.layout.addWidget(self.pauseButton, 1, 1)

    def showWindow(self):
        self.win.showMaximized()

    def processInputs(self, inputs, debuggingApp):
        if (len(inputs) == 0):
            print("inputs est vide. id : InterfaceDebug.py")
            return

        current = inputs[-1]

        if current >= -100:
            print("erreur impossible. id : InterfaceDebug.py")
        elif current >= -200:
            self.pathfindingPlot.processInputs_Pathfinding(
                inputs, debuggingApp)
        elif current >= -300:
            self.asserPlot.processInputs_Asser(inputs, debuggingApp)
        elif current >= -400:
            self.randomInfo.processInputs_RandomInfo(inputs, debuggingApp)
        else:
            print("sequence de données inconnue. code de donnée : ", current)
            inputs.clear()

    def updatePlotsInfoRobot(self, infoRobot):
        self.pathfindingPlot.updateData(infoRobot)

    def refreshPlot(self):
        self.pathfindingPlot.refreshPlot()
        self.asserPlot.refreshPlot()
        self.randomInfo.refreshPlot()

    def reset(self):
        self.pathfindingPlot.reset()
        self.asserPlot.reset()
