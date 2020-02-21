from pyqtgraph.Qt import QtGui, QtCore
import cProfile  # lib utilisee pour le profiling
# pour profiling dans cmd : "python -m cProfile -s cumtime Main.py" et pour clear terminal : "cls"

from App import App

app = App()

QtGui.QApplication.processEvents()

# Update data display
timer = QtCore.QTimer()
timer.timeout.connect(app.loop)
timer.start(0.0001)

if __name__ == '__main__':
    QtGui.QApplication.instance().exec_()
