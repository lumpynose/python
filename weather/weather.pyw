#import sys
#import time

from PyQt6 import QtGui
from PyQt6 import QtWidgets
from PyQt6 import QtCore

from PromSensor import GetPromSensor

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.threadpool = QtCore.QThreadPool()

        self.signals = WorkerSignals()

        self.signals.result.connect(self.process_result)

        self.prom_sensor = GetPromSensor()
        self.sensor_locations = { "prologue" : "garage", "accurite" : "outside", "oregon" : "attic" }
        self.widgets = { }

        self.layout_top_hbox = QtWidgets.QHBoxLayout()
        self.layout_top_hbox.setObjectName("layout_top_hbox")

        self.layout_temps_vbox = QtWidgets.QVBoxLayout()
        self.layout_temps_vbox.setObjectName("layout_temps_vbox")

        self.frame_main = QtWidgets.QFrame()

        self.frame_main.setStyleSheet("background-color:gray")
        self.frame_main.setParent(self)
        self.frame_main.setObjectName("frame_main")
        self.frame_main.setLayout(self.layout_top_hbox)

        self.frame_temps  = QtWidgets.QFrame()

        self.frame_temps.setStyleSheet("background-color:DarkSeaGreen")
        self.frame_temps.setParent(self.frame_main)
        self.frame_temps.setObjectName("frame_temps")
        self.frame_temps.setLayout(self.layout_temps_vbox)

        self.frame_summary = QtWidgets.QFrame()

        self.frame_summary.setStyleSheet("background-color:Peru")
        self.frame_summary.setParent(self.frame_main)
        self.frame_summary.setObjectName("frame_summary")

        self.layout_top_hbox.addWidget(self.frame_temps)
        self.layout_top_hbox.addWidget(self.frame_summary)

        self.layout_temps_vbox.setParent(self.frame_temps)

        self.setCentralWidget(self.frame_main)

        self.show()

        self.request_data()

    def request_data(self):
        worker = Worker(prom_sensor = self.prom_sensor, signals = self.signals)

        self.threadpool.start(worker)
        QtCore.QTimer.singleShot(30 * 1000, self.request_data)
    
    @QtCore.pyqtSlot(dict)
    def process_result(self, sensors):
        for sensor in sensors.keys():
            if self.widgets.get(sensor):
                self.update_sensor(sensor, sensors.get(sensor))
            else:
                self.add_sensor(sensor, sensors.get(sensor))

    def update_sensor(self, sensor, value):
        label = self.widgets.get(sensor)
        label.setText("{:.1f}".format(float(value)))

    def add_sensor(self, sensor, value):
        frame_sensor = QtWidgets.QFrame()

        frame_sensor.setParent(self.frame_temps)
        frame_sensor.setStyleSheet("border: 2px solid black; background-color:SkyBlue; border-radius:6px")
        frame_sensor.setObjectName("frame_sensor")

        self.layout_temps_vbox.addWidget(frame_sensor)

        location = self.sensor_locations.get(sensor)

        if location:
            label_title = QtWidgets.QLabel()
            label_title.setText("{} ({})".format(location, sensor))
        else:
            label_title = QtWidgets.QLabel()
            label_title.setText(sensor)

        label_title.setParent(frame_sensor)
        label_title.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        label_title.setStyleSheet("border: 1px solid black; background-color:DarkKhaki; border-radius:2px")
        label_title.setAlignment(QtCore.Qt.Alignment.AlignCenter)
        label_title.setFont(QtGui.QFont("Cooper Lt BT", 12))
        label_title.setObjectName("label_title")

        label_value = QtWidgets.QLabel()

        label_value.setText("{:.1f}".format(float(value)))

        label_value.setParent(frame_sensor)
        label_value.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        label_value.setStyleSheet("border: 1px solid black; background-color:PaleTurquoise; border-radius:4px")
        label_value.setAlignment(QtCore.Qt.Alignment.AlignCenter)
        label_value.setFont(QtGui.QFont("Cooper Blk BT", 32))
        label_value.setObjectName("label_value")

        layout_vbox = QtWidgets.QVBoxLayout(frame_sensor)

        layout_vbox.setObjectName("layout_vbox")
        layout_vbox.addWidget(label_title)
        layout_vbox.addWidget(label_value)

        frame_sensor.setLayout(layout_vbox)

        self.widgets.update({ sensor : label_value })

    def closeEvent(self, event):
        event.accept()
        sys.exit()

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

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()

    app.exec()
