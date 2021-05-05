from PyQt6 import QtCore

class Worker(QtCore.QRunnable):
    def __init__(self, prom_sensor, signals):
        super(Worker, self).__init__()
        self.prom_sensor = prom_sensor
        self.signals = signals

    def run(self):
        values = self.prom_sensor.get_sensor_latest()
        self.signals.result.emit(values)

class WorkerSignals(QtCore.QObject):
    result = QtCore.pyqtSignal(dict)
