import time

from InterfaceDebug import InterfaceDebug


class App:
    def __init__(self):
        # debuggingApp : variable utilisee pour print des infos sur l'app lors du debug
        self.debuggingApp = False

        self.interfaceDebug = InterfaceDebug()
        self.inputs = []
        self.state = "INIT"
        self.infoRobot = {"position": [0, 0],
                          "target": [0, 0],
                          "vitesse": [0, 0],
                          "time": 0.0}

        self.creationTime = time.time()*1000
        self.lastRefreshTime = time.time()*1000

        self.interfaceDebug.showWindow()

    def readInput(self, serial):
        ser_bytes = serial.readline()
        decoded_byte = 0
        try:
            decoded_byte = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        except ValueError:
            if self.debuggingApp:
                print("Failed to convert string to float")
        self.inputs.insert(0, decoded_byte)

    def processInputs(self):
        if len(self.inputs) == 0:
            return

        if self.inputs[0] == -1:  # -1 marque la fin d'une séquence de donnees
            if self.debuggingApp:
                print(" ")
                print("debut sequence reception")
                print(self.inputs)

            while len(self.inputs) > 0:
                current = self.inputs[len(self.inputs) - 1]

                if current >= 0:
                    print("erreur : sequence de donnee non definie. id : App.py l.38")
                    self.inputs.pop()
                else:
                    if current >= -100:
                        self.processInputs_InfoRobot()
                    else:
                        self.interfaceDebug.processInputs(
                            self.inputs, self.debuggingApp)

    def processInputs_InfoRobot(self):
        if len(self.inputs) == 0:
            print("erreur dans processInputs_InfoRobot : input vide")
            return

        current = self.inputs.pop()

        if current == -2.0:
            if self.debuggingApp:
                print("reading current position")
            self.processInputs_RobotPosition()

        elif current == -3.0:
            if self.debuggingApp:
                print("reading current target")
            self.processInputs_RobotTarget()

        elif current == -4.0:
            if self.debuggingApp:
                print("reading time")
            self.processInputs_Time()

        else:
            print("sequence de données inconnue. code de donnée : ", current)
            self.inputs.clear()

    def processInputs_RobotPosition(self):
        if len(self.inputs) == 0:
            print("erreur dans processInputs_RobotPosition. ID error : 1")
            return

        current = self.inputs.pop()

        if current < 0 or len(self.inputs) == 0:
            if current == -1.0:  # fin de la séquence
                if self.debuggingApp:
                    print("fin de la séquence")
            else:
                print("erreur dans processInputs_RobotPosition. ID error : 2")
            return

        else:
            current2 = self.inputs.pop()
            if current2 < 0:
                print("erreur dans processInputs_RobotPosition. ID error : 3")
                self.inputs.append(current2)
                return
            else:
                self.infoRobot["position"] = [current, current2]
                self.processInputs_RobotPosition()

    def processInputs_RobotTarget(self):
        if len(self.inputs) == 0:
            print("erreur dans processInputs_RobotTarget. ID error : 1")
            return

        current = self.inputs.pop()

        if current < 0 or len(self.inputs) == 0:
            if current == -1.0:  # fin de la séquence
                if self.debuggingApp:
                    print("fin de la séquence")
            else:
                print("erreur dans processInputs_RobotTarget. ID error : 2")
            return

        else:
            current2 = self.inputs.pop()
            if current2 < 0:
                print("erreur dans processInputs_RobotTarget. ID error : 3")
                self.inputs.append(current2)
                return
            else:
                self.infoRobot["target"] = [current, current2]
                self.processInputs_RobotTarget()

    def processInputs_Time(self):
        if len(self.inputs) == 0:
            print("erreur dans processInputs_Time. ID error : 1")
            return

        current = self.inputs.pop()

        if current < 0 or len(self.inputs) == 0:
            if current == -1.0:  # fin de la séquence
                if self.debuggingApp:
                    print("fin de la séquence")
            else:
                print("erreur dans processInputs_RobotTarget. ID error : 2")
            return

        else:
            self.infoRobot["time"] = current
            if self.debuggingApp:
                print("current time : ", self.infoRobot["time"])
            self.processInputs_Time()

    def updatePlotsInfoRobot(self):
        self.interfaceDebug.updatePlotsInfoRobot(self.infoRobot)

    def refresh(self, QtGui):
        if time.time()*1000 - self.lastRefreshTime > 80:
            self.interfaceDebug.refreshPlot()
            QtGui.QApplication.processEvents()
            self.lastRefreshTime = time.time()*1000
