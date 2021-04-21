from PyQt6 import QtGui
from PyQt6 import QtWidgets
from PyQt6 import QtCore
from sensor import GetPromSensor

import time

class WorkerSignals(QtCore.QObject):
    result = QtCore.pyqtSignal(float)

class Worker(QtCore.QRunnable):
    def __init__(self, prom_sensor):
        super(Worker, self).__init__()
        self.prom_sensor = prom_sensor
        self.signals = WorkerSignals()

    @QtCore.pyqtSlot()
    def run(self):
        while True:
            print("Thread start")
            self.signals.result.emit(float(self.prom_sensor.get_sensor_latest()))
            time.sleep(30)
            print("Thread complete")

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.threadpool = QtCore.QThreadPool()
        self.prom_sensor = GetPromSensor()

        self.previous = None

        layout = QtWidgets.QGridLayout()

        self.label = QtWidgets.QLabel("Start")
        self.label.setStyleSheet("background-color:rosybrown; border-radius:5px")
        self.label.setAlignment(QtCore.Qt.Alignment.AlignCenter)
        self.label.setFont(QtGui.QFont("Arial", 32))

        layout.addWidget(self.label)

        widget = QtWidgets.QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        self.show()

        self.start_worker()

    def start_worker(self):
        worker = Worker(prom_sensor = self.prom_sensor)
        worker.signals.result.connect(self.process_result)

        self.threadpool.start(worker)

    def process_result(self, temperature):
        if temperature == self.previous:
            return

        self.previous = temperature
        print("receiving:", temperature)
        self.label.setText(str(temperature))

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    app.exec()
