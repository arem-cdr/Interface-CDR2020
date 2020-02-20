from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

from MyPlot import MyPlot


class PathfindingPlot(MyPlot):
    def __init__(self):
        MyPlot.__init__(self)
        self.nodeCount = 0
        self.plotWidget.invertY(True)

        # .scaled(self._img_res[0],self._img_res[1],
        img = QtGui.QImage("Terrain.png")
        img = img.scaledToWidth(3000)
        # img.invertPixels()

        # thats essential for pg.imageToArray(img)
        img = img.convertToFormat(QtGui.QImage.Format_RGBA8888_Premultiplied)
        imgArray = pg.imageToArray(img, copy=True)
        self._img = pg.ImageItem(imgArray)

        #self.background = pg.ImageItem("soloIcon.png")
        self.plotWidget.addItem(self._img)
        self.posInLayout = [0, 0, 1, 1]
        self.plotWidget.getPlotItem().setTitle("Pathfinding")

        # creation de la legende
        self.legend = pg.LegendItem(size=(100, 50), offset=(40, 10))
        self.legend.setParentItem(self.plotWidget.graphicsItem())
        self.legend.addItem(item=pg.ScatterPlotItem(pen=None, size=18, brush='g', symbol='o'),
                            name="Obstacles")
        self.legend.addItem(item=pg.ScatterPlotItem(pen=None, size=35, brush='r', symbol='o'),
                            name="Robot")
        self.legend.addItem(item=pg.ScatterPlotItem(pen=None, size=18, brush=(0, 0, 0), symbol='x'),
                            name="Target")

        # creation des variables receptrices des donnees
        self.DataObstacles = pg.ScatterPlotItem(pen=(0, 0, 0), symbol='o',
                                                symbolPen=None, symbolBrush='r')
        self.DataPositionRobot = pg.ScatterPlotItem(pen=(0, 0, 0), symbol='o',
                                                    symbolPen=None, symbolBrush='r')
        self.DataTargetRobot = pg.ScatterPlotItem(pen=(0, 0, 0), symbol='o',
                                                  symbolPen=None, symbolBrush='r')
        self.linesRRT = []
        self.previousLinesRRT = []
        self.linesPath = []
        self.previousLinesPath = []

        # ajout des donnees au plot
        self.plotWidget.addItem(self.DataObstacles)
        self.plotWidget.addItem(self.DataPositionRobot)
        self.plotWidget.addItem(self.DataTargetRobot)
        for i in range(0, len(self.linesPath)):
            self.plotWidget.addItem(self.linesPath[i])
        for i in range(0, len(self.linesRRT)):
            self.plotWidget.addItem(self.linesRRT[i])

        # dimensions du plot
        self.plotWidget.setXRange(0, 3000)
        self.plotWidget.setYRange(0, 2000)

    def processInputs_Pathfinding(self, inputs, debuggingApp):
        if len(inputs) == 0:
            return

        current = inputs.pop()

        if current == -101:
            spots = []
            self.processInputs_Obstacles(inputs, debuggingApp, spots)

        elif current == -102.0:
            self.linesRRT = []
            self.processInputs_RRTBranches(inputs, debuggingApp)

        elif current == -103:
            self.processInputs_NodeCount(inputs, debuggingApp)

        elif current == -104.0:
            self.linesPath = []
            self.processInputs_Path(inputs, debuggingApp)

        else:
            inputs.clear()

        if len(inputs) > 0:
            inputs.clear()

    def processInputs_Obstacles(self, inputs, debuggingApp, spots):
        if len(inputs) == 0:
            return

        current = inputs.pop()

        if current < 0 or len(inputs) == 0:
            if current == -1:  # fin de la séquence
                self.DataObstacles.setData(spots)
            return

        current2 = inputs.pop()
        if current2 < 0:
            inputs.append(current2)
            return

        current3 = inputs.pop()
        if current3 < 0:
            inputs.append(current3)
            return

        if current == 1:  # gobelet vert
            spots.append(
                {'pos': (current2, current3), 'size': 18, 'pen': (0, 0, 0), 'brush': 'g', 'symbol': 'o'})
        elif current == 2:  # gobelet rouge
            spots.append(
                {'pos': (current2, current3), 'size': 18, 'pen': (0, 0, 0), 'brush': 'r', 'symbol': 'o'})
        elif current == 3:  # robot
            spots.append(
                {'pos': (current2, current3), 'size': 40, 'pen': (0, 0, 0), 'brush': 'w', 'symbol': 'o'})
        else:
            print("id objet inconnue")
        self.processInputs_Obstacles(inputs, debuggingApp, spots)

    def processInputs_RRTBranches(self, inputs, debuggingApp):
        if len(inputs) == 0:
            return

        current = inputs.pop()

        if current < 0 or len(inputs) == 0:
            return

        if len(inputs) < 3:
            inputs.clear()
            return

        current2 = inputs.pop()
        if current2 < 0:
            inputs.append(current2)
            return

        current3 = inputs.pop()
        if current3 < 0:
            inputs.append(current3)
            return

        current4 = inputs.pop()
        if current4 < 0:
            inputs.append(current4)
            return

        self.linesRRT.append(pg.LineSegmentROI(
            [[current, current2], [current3, current4]], pen=pg.mkPen('g', width=1)))
        self.processInputs_RRTBranches(inputs, debuggingApp)

    def processInputs_NodeCount(self, inputs, debuggingApp):
        if len(inputs) == 0:
            return

        current = inputs.pop()

        if current < 0 or len(inputs) == 0:
            return

        else:
            self.nodeCount = current
            #print("node count : ", current)
            self.processInputs_NodeCount(inputs, debuggingApp)

    def processInputs_Path(self, inputs, debuggingApp):
        if len(inputs) == 0:
            return

        current = inputs.pop()

        if current < 0 or len(inputs) == 0:
            return

        if len(inputs) < 3:
            inputs.clear()
            return

        current2 = inputs.pop()
        if current2 < 0:
            inputs.append(current2)
            return

        current3 = inputs.pop()
        if current3 < 0:
            inputs.append(current3)
            return

        current4 = inputs.pop()
        if current4 < 0:
            inputs.append(current4)
            return

        self.linesPath.append(pg.LineSegmentROI(
            [[current, current2], [current3, current4]], pen=pg.mkPen(color=(100, 50, 50), width=2, style=None)))
        self.processInputs_Path(inputs, debuggingApp)

    def updateData(self, infoRobot):
        # update de la position du robot
        spots = []
        spots.append(
            {'pos': (infoRobot["position"][0],
                     infoRobot["position"][1]),
             'size': 85,
             'pen': None,
             'brush': 'r',
             'symbol': 'o'})
        self.DataPositionRobot.setData(spots)

        # update de la target du robot
        spots = []
        spots.append(
            {'pos': (infoRobot["target"][0],
                     infoRobot["target"][1]),
             'size': 18,
             'pen': None,
             'brush': (0, 0, 0),
             'symbol': 'x'})
        self.DataTargetRobot.setData(spots)

    def refreshPlot(self):
        # refreshing path
        for i in range(0, len(self.previousLinesPath)):
            self.plotWidget.removeItem(self.previousLinesPath[i])
        for i in range(0, len(self.linesPath)):
            self.plotWidget.addItem(self.linesPath[i])
        self.previousLinesPath = self.linesPath

        # refreshing RRT
        for i in range(0, len(self.previousLinesRRT)):
            self.plotWidget.removeItem(self.previousLinesRRT[i])
        for i in range(0, len(self.linesRRT)):
            self.plotWidget.addItem(self.linesRRT[i])
        self.previousLinesRRT = self.linesRRT

    def reset(self):
        for i in range(0, len(self.previousLinesPath)):
            self.plotWidget.removeItem(self.previousLinesPath[i])

        for i in range(0, len(self.previousLinesRRT)):
            self.plotWidget.removeItem(self.previousLinesRRT[i])

        self.DataObstacles.clear()
        self.DataPositionRobot.clear()
        self.DataTargetRobot.clear()
        self.linesRRT.clear()
        self.previousLinesRRT.clear()
        self.linesPath.clear()
        self.previousLinesPath.clear()
