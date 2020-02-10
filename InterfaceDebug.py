
from pyqtgraph.Qt import QtGui, QtCore

from PathfindingPlot import PathfindingPlot
from AsserPlot import AsserPlot


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

        # ajout des graphiques au layout
        self.layout.addWidget(
            self.pathfindingPlot.__getPlot__(),
            self.pathfindingPlot.__getPosInLayout__()[0],
            self.pathfindingPlot.__getPosInLayout__()[1],
            self.pathfindingPlot.__getPosInLayout__()[2],
            self.pathfindingPlot.__getPosInLayout__()[3])
        self.layout.addWidget(
            self.asserPlot.__getPlot__(),
            self.asserPlot.__getPosInLayout__()[0],
            self.asserPlot.__getPosInLayout__()[1],
            self.asserPlot.__getPosInLayout__()[2],
            self.asserPlot.__getPosInLayout__()[3])

    def showWindow(self):
        self.win.show()

    def processInputs(self, inputs, debuggingApp):
        if (len(inputs) == 0):
            print("inputs est vide. id : InterfaceDebug.py l.30")
            return

        current = inputs[len(inputs) - 1]

        if current >= -100:
            print("erreur impossible. id : InterfaceDebug.py l.35")
        elif current >= -200:
            self.pathfindingPlot.processInputs_Pathfinding(
                inputs, debuggingApp)
        else:
            print("sequence de données inconnue. code de donnée : ", current)
            inputs.clear()

    def updatePlotsInfoRobot(self, infoRobot):
        self.pathfindingPlot.updateData(infoRobot)

    def refreshPlot(self):
        self.pathfindingPlot.refreshPlot()
