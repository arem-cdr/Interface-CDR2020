from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

from MyPlot import MyPlot


class AsserPlot(MyPlot):
    def __init__(self):
        MyPlot.__init__(self)

        self.posInLayout = [0, 2, 1, 1]
        self.plotWidget.getPlotItem().setTitle("Asservissement")

        # valeur servant à supprimer les données trop anciennes
        self.trimRange = 20
        self.plotXRange = 2

        # creation des variables receptrices des donnees
        self.time = []
        self.realRight = []
        self.realLeft = []
        self.commandRight = []
        self.commandLeft = []

        # ajout des donnees au plot avec leur couleur correspondante
        self.plotRealRight = self.plotWidget.plot(
            self.time, self.realRight, pen=(70, 70, 255))
        self.plotRealLeft = self.plotWidget.plot(
            self.time, self.realLeft, pen=(255, 70, 70))
        self.plotCommandRight = self.plotWidget.plot(
            self.time, self.commandRight, pen=(30, 30, 110))
        self.plotCommandLeft = self.plotWidget.plot(
            self.time, self.commandLeft, pen=(110, 30, 30))

        # creation de la legende
        self.legend = pg.LegendItem(size=(170, 0), offset=(45, 3))

        self.legend.setParentItem(self.plotWidget.graphicsItem())
        self.legend.addItem(self.plotRealRight, name="vitesse réelle droite")
        self.legend.addItem(self.plotCommandRight, name="commande droite")
        self.legend.addItem(self.plotRealLeft, name="vitesse réelle gauche")
        self.legend.addItem(self.plotCommandLeft, name="commande gauche")

        # dimensions du plot
        # self.plotAsser.setXRange(0, 100)
        # self.plotAsser.setYRange(0, 30)

    def processInputs_Asser(self, inputs, debuggingApp):
        if len(inputs) == 0:
            return

        current = inputs.pop()

        if current == -201:
            if debuggingApp:
                print("reading speeds")
            self.processInputs_Speeds(inputs, debuggingApp)

        else:
            print("sequence de données inconnue. code de donnée : ", current)
            inputs.clear()

        if len(inputs) > 0:
            print("erreur : les donnees n'ont pas toutes été lues")
            inputs.clear()

    def processInputs_Speeds(self, inputs, debuggingApp):
        if len(inputs) == 0:
            print("erreur dans processInputs_Speeds. ID error : 1")
            return

        # print(inputs)

        current = inputs.pop()

        if current < 0 or len(inputs) < 3:
            if current == -1:  # fin de la séquence
                if debuggingApp:
                    print("fin de la séquence")
            else:
                print("erreur dans processInputs_Speeds. ID error : 2")
            return

        current2 = inputs.pop()
        if current2 < 0:
            print("erreur dans processInputs_Speeds. ID error : 3")
            inputs.append(current2)
            return

        current3 = inputs.pop()
        if current3 < 0:
            print("erreur dans processInputs_Speeds. ID error : 3")
            inputs.append(current3)
            return

        current4 = inputs.pop()
        if current4 < 0:
            print("erreur dans processInputs_Speeds. ID error : 3")
            inputs.append(current4)
            return

        current5 = inputs.pop()
        if current5 < 0:
            print("erreur dans processInputs_Speeds. ID error : 3")
            inputs.append(current5)
            return

        self.time.append(current * 0.001)
        self.realRight.append(current2)
        self.realLeft.append(current3)
        self.commandRight.append(current4)
        self.commandLeft.append(current5)

        self.trimData()

        self.processInputs_Speeds(inputs, debuggingApp)

    def trimData(self):
        while self.time[-1] - self.time[0] > self.trimRange:
            self.time = self.time[1:]
            self.realRight = self.realRight[1:]
            self.realLeft = self.realLeft[1:]
            self.commandRight = self.commandRight[1:]
            self.commandLeft = self.commandLeft[1:]

    def refreshPlot(self):
        self.plotRealRight.setData(self.time, self.realRight)
        self.plotRealLeft.setData(self.time, self.realLeft)
        self.plotCommandRight.setData(self.time, self.commandRight)
        self.plotCommandLeft.setData(self.time, self.commandLeft)

        self.setXRangePlot()

    def setXRangePlot(self):
        if len(self.time) > 0 and self.time[-1] - self.time[0] > self.plotXRange and self.time[-1] - self.plotXRange > 0:
            self.plotWidget.setXRange(
                self.time[-1] - self.plotXRange, self.time[-1])

    def reset(self):
        self.time.clear()
        self.realRight.clear()
        self.realLeft.clear()
        self.commandRight.clear()
        self.commandLeft.clear()

        self.plotRealRight.setData(self.time, self.realRight)
        self.plotRealLeft.setData(self.time, self.realLeft)
        self.plotCommandRight.setData(self.time, self.commandRight)
        self.plotCommandLeft.setData(self.time, self.commandLeft)

        self.plotWidget.setXRange(0, self.plotXRange)
