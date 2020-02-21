from pyqtgraph.Qt import QtGui, QtCore
import serial
import time
import sys

from InterfaceDebug import InterfaceDebug
FRAME_RATE2 = 100
FRAME_RATE = 5


class App:
    def __init__(self):
        # debuggingApp : variable utilisee pour print des infos sur l'app lors du debug
        self.debuggingApp = False
        self.doneLoop = True

        # remplacer "com8" ligne 10 par le port com utilise. rappel : "python -m serial.tools.list_ports -v" pour lister les ports com disponibles
        self.baudrate = 2000000
        self.timeout = 0.001

        # ouverture du port serie
        # print(self.availablePorts())
    
        self.ser = serial.Serial(
                '/dev/ttyACM0', self.baudrate, timeout=self.timeout)

        # creation de l'interface graphique et de ses variables
        self.interfaceDebug = InterfaceDebug()
        self.inputs = []
        self.infoRobot = {"position": [0, 0],
                          "target": [0, 0],
                          "vitesse": [0, 0],
                          "time": 0.0}

        self.creationTime = time.time() * 1000
        self.lastFrameTime = time.time() * 1000
        self.lastread = time.time() * 1000

        self.interfaceDebug.showWindow()


    def loop(self):
        if self.ser.is_open:
            
            
            if time.time() * 1000 - self.lastFrameTime > 1 / FRAME_RATE * 1000 and not(self.interfaceDebug.pauseButton.isChecked()):
                self.updatePlotsInfoRobot()
                self.refresh()
                self.lastFrameTime = time.time() * 1000
                self.ser.reset_input_buffer()
            if time.time() *1000 - self.lastread > 1 / FRAME_RATE2:
                
                self.readInput()
                self.processInputs()
                self.lastread = time.time() * 1000
 
            

    def readInput(self):
        ser_bytes = self.ser.readline()
        
        decoded_byte = 0
        if len(ser_bytes) > 1:
            try:
                decoded_byte = int(ser_bytes[0:len(ser_bytes)-1])
            except ValueError:
                if self.debuggingApp:
                    print("convertion Failed")
                    print(ser_bytes)
            self.inputs.insert(0, decoded_byte)

    def processInputs(self):
        if len(self.inputs) < 2:
            return

        if self.inputs[0] == -1:  # -1 marque la fin d'une séquence de donnees
            if self.debuggingApp:
                print(" ")
                print("debut sequence reception")
                print(self.inputs)

            while len(self.inputs) > 0:
                current = self.inputs[len(self.inputs) - 1]

                if current >= -1:
                    self.inputs.pop()
                else:
                    if current >= -100:
                        self.processInputs_GeneralInfo()
                    else:
                        self.interfaceDebug.processInputs(
                            self.inputs, self.debuggingApp)

    def processInputs_GeneralInfo(self):
        if len(self.inputs) == 0:
            return

        current = self.inputs.pop()

        if current == -1:
            return

        if current == -2:
            self.reset()

        if current == -3:
            self.processInputs_RobotPosition()

        elif current == -4:
            self.processInputs_RobotTarget()

        elif current == -5:
            self.processInputs_Time()

        else:
            self.inputs.clear()
        

    def processInputs_RobotPosition(self):
        if len(self.inputs) == 0:
            return

        current = self.inputs.pop()

        if current < 0 or len(self.inputs) == 0:
            return

        else:
            current2 = self.inputs.pop()
            if current2 < 0:
                self.inputs.append(current2)
                return
            else:
                self.infoRobot["position"] = [current, current2]
                self.processInputs_RobotPosition()

    def processInputs_RobotTarget(self):
        if len(self.inputs) == 0:
            return

        current = self.inputs.pop()

        if current < 0 or len(self.inputs) == 0:
            return

        current2 = self.inputs.pop()
        if current2 < 0:
            self.inputs.append(current2)
            return
        else:
            self.infoRobot["target"] = [current, current2]
            self.processInputs_RobotTarget()

    def processInputs_Time(self):
        if len(self.inputs) == 0:
            return

        current = self.inputs.pop()

        if current < 0 or len(self.inputs) == 0:
            return

        else:
            self.infoRobot["time"] = current
            self.processInputs_Time()

    def updatePlotsInfoRobot(self):
        self.interfaceDebug.updatePlotsInfoRobot(self.infoRobot)

    def refresh(self):
        self.interfaceDebug.refreshPlot()
        self.lastRefreshTime = time.time() * 1000

    def reset(self):
        print("reset")
        self.interfaceDebug.reset()
