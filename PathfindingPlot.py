import pyqtgraph as pg

from MyPlot import MyPlot


class PathfindingPlot(MyPlot):
    def __init__(self):
        MyPlot.__init__(self)
        self.nodeCount = 0

        self.posInLayout = [0, 0, 1, 1]
        self.plotPathfinding.getPlotItem().setTitle("Pathfinding")

        # creation de la legende
        self.legend = pg.LegendItem(size=(100, 50), offset=(40, 10))
        self.legend.setParentItem(self.plotPathfinding.graphicsItem())
        self.legend.addItem(item=pg.ScatterPlotItem(pen=None, size=10, brush='g', symbol='o'),
                            name="Obstacles")
        self.legend.addItem(item=pg.ScatterPlotItem(pen=None, size=35, brush='r', symbol='o'),
                            name="Robot")
        self.legend.addItem(item=pg.ScatterPlotItem(pen=None, size=15, brush='w', symbol='x'),
                            name="Target")

        # creation des variables receptrices des donnees
        self.DataObstacles = pg.ScatterPlotItem(pen=None, symbol='o',
                                                symbolPen=None, symbolBrush='r')
        self.DataPositionRobot = pg.ScatterPlotItem(pen=None, symbol='o',
                                                    symbolPen=None, symbolBrush='r')
        self.DataTargetRobot = pg.ScatterPlotItem(pen=None, symbol='o',
                                                  symbolPen=None, symbolBrush='r')
        self.linesRRT = []
        self.previousLinesRRT = []
        self.linesPath = []
        self.previousLinesPath = []

        # ajout des donnees au plot
        self.plotPathfinding.addItem(self.DataObstacles)
        self.plotPathfinding.addItem(self.DataPositionRobot)
        self.plotPathfinding.addItem(self.DataTargetRobot)
        for i in range(0, len(self.linesPath)):
            self.plotPathfinding.addItem(self.linesPath[i])
        for i in range(0, len(self.linesRRT)):
            self.plotPathfinding.addItem(self.linesRRT[i])

        # dimensions du plot
        self.plotPathfinding.setXRange(0, 300)
        self.plotPathfinding.setYRange(0, 200)

    def processInputs_Pathfinding(self, inputs, debuggingApp):
        if len(inputs) == 0:
            return

        current = inputs.pop()

        if current == -101.0:
            if debuggingApp:
                print("reading obstacles")
            spots = []
            self.processInputs_Obstacles(inputs, debuggingApp, spots)

        elif current == -102.0:
            self.linesRRT = []
            if debuggingApp:
                print("reading RRT")
            self.processInputs_RRTBranches(inputs, debuggingApp)

        elif current == -103.0:
            if debuggingApp:
                print("reading node count")
            self.processInputs_NodeCount(inputs, debuggingApp)

        elif current == -104.0:
            self.linesPath = []
            if debuggingApp:
                print("reading path")
            self.processInputs_Path(inputs, debuggingApp)

        else:
            print("sequence de données inconnue. code de donnée : ", current)
            inputs.clear()

        if len(inputs) > 0:
            print("erreur : les donnees n'ont pas toutes été lues")
            inputs.clear()

    def processInputs_Obstacles(self, inputs, debuggingApp, spots):
        if len(inputs) == 0:
            print("erreur dans processInputs_Obstacles. ID error : 1")
            return

        current = inputs.pop()

        if current < 0 or len(inputs) == 0:
            if current == -1.0:  # fin de la séquence
                if debuggingApp:
                    print("fin de la séquence")
                self.DataObstacles.setData(spots)
            else:
                print("erreur dans processInputs_Obstacles. ID error : 2")
            return

        else:
            current2 = inputs.pop()
            if current2 < 0:
                print("erreur dans reading obstacles. ID error : 3")
                inputs.append(current2)
                return
            else:
                spots.append(
                    {'pos': (current, current2), 'size': 10, 'pen': None, 'brush': 'g', 'symbol': 'o'})
                self.processInputs_Obstacles(inputs, debuggingApp, spots)

    def processInputs_RRTBranches(self, inputs, debuggingApp):
        if len(inputs) == 0:
            print("erreur dans processInputs_RRTBranches. ID error : 1")
            return

        current = inputs.pop()

        if current < 0 or len(inputs) == 0:
            if current == -1.0:  # fin de la séquence
                if debuggingApp:
                    print("fin de la séquence")
            else:
                print("erreur dans processInputs_RRTBranches. ID error : 2")
            return

        if len(inputs) < 3:
            print("erreur dans reading RRT branches. ID error : 3")
            inputs.clear()
            return

        current2 = inputs.pop()
        if current2 < 0:
            inputs.append(current2)
            print("erreur dans reading RRT branches. ID error : 4")
            return

        current3 = inputs.pop()
        if current3 < 0:
            inputs.append(current3)
            print("erreur dans reading RRT branches. ID error : 4")
            return

        current4 = inputs.pop()
        if current4 < 0:
            inputs.append(current4)
            print("erreur dans reading RRT branches. ID error : 4")
            return

        self.linesRRT.append(pg.LineSegmentROI(
            [[current, current2], [current3, current4]], pen=pg.mkPen('g', width=1)))
        self.processInputs_RRTBranches(inputs, debuggingApp)

    def processInputs_NodeCount(self, inputs, debuggingApp):
        if len(inputs) == 0:
            print("erreur dans processInputs_NodeCount. ID error : 1")
            return

        current = inputs.pop()

        if current < 0 or len(inputs) == 0:
            if current == -1.0:  # fin de la séquence
                if debuggingApp:
                    print("fin de la séquence")
            else:
                print("erreur dans processInputs_NodeCount. ID error : 2")
            return

        else:
            self.nodeCount = current
            if debuggingApp:
                print("node count : ", self.nodeCount)
            self.processInputs_NodeCount(inputs, debuggingApp)

    def processInputs_Path(self, inputs, debuggingApp):
        if len(inputs) == 0:
            print("erreur dans processInputs_Path. ID error : 1")
            return

        current = inputs.pop()

        if current < 0 or len(inputs) == 0:
            if current == -1.0:  # fin de la séquence
                if debuggingApp:
                    print("fin de la séquence")
            else:
                print("erreur dans processInputs_Path. ID error : 2")
            return

        if len(inputs) < 3:
            print("erreur dans reading Path. ID error : 3")
            inputs.clear()
            return

        current2 = inputs.pop()
        if current2 < 0:
            inputs.append(current2)
            print("erreur dans reading Path. ID error : 4")
            return

        current3 = inputs.pop()
        if current3 < 0:
            inputs.append(current3)
            print("erreur dans reading Path. ID error : 4")
            return

        current4 = inputs.pop()
        if current4 < 0:
            inputs.append(current4)
            print("erreur dans reading Path. ID error : 4")
            return

        self.linesPath.append(pg.LineSegmentROI(
            [[current, current2], [current3, current4]], pen=pg.mkPen('r', width=1)))
        self.processInputs_Path(inputs, debuggingApp)

    def updateData(self, infoRobot):
        # update de la position du robot
        spots = []
        spots.append(
            {'pos': (infoRobot["position"][0],
                     infoRobot["position"][1]),
             'size': 35,
             'pen': None,
             'brush': 'r',
             'symbol': 'o'})
        self.DataPositionRobot.setData(spots)

        # update de la target du robot
        spots = []
        spots.append(
            {'pos': (infoRobot["target"][0],
                     infoRobot["target"][1]),
             'size': 15,
             'pen': None,
             'brush': 'w',
             'symbol': 'x'})
        self.DataTargetRobot.setData(spots)

    def refreshPlot(self):
        # refreshing path
        for i in range(0, len(self.previousLinesPath)):
            self.plotPathfinding.removeItem(self.previousLinesPath[i])
        for i in range(0, len(self.linesPath)):
            self.plotPathfinding.addItem(self.linesPath[i])
        self.previousLinesPath = self.linesPath

        # refreshing RRT
        for i in range(0, len(self.previousLinesRRT)):
            self.plotPathfinding.removeItem(self.previousLinesRRT[i])
        for i in range(0, len(self.linesRRT)):
            self.plotPathfinding.addItem(self.linesRRT[i])
        self.previousLinesRRT = self.linesRRT
