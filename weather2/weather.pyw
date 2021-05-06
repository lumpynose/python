import sys

from PyQt6 import QtGui
from PyQt6 import QtWidgets
from PyQt6 import QtCore

import PromSensor
import PromWorker

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.threadpool = QtCore.QThreadPool()

        self.signals = PromWorker.WorkerSignals()

        self.signals.result.connect(self.process_result)

        self.prom_sensor = PromSensor.GetPromSensor()
        self.sensor_locations = { "prologue" : "garage", "accurite" : "outside", "oregon" : "attic" }
        self.widgets = { }

        layout_top_hbox = QtWidgets.QHBoxLayout()
        layout_top_hbox.setObjectName("layout_top_hbox")

        self.layout_temps_vbox = QtWidgets.QVBoxLayout()
        self.layout_temps_vbox.setObjectName("layout_temps_vbox")

        frame_main = QtWidgets.QFrame()

        frame_main.setStyleSheet("background-color:gray")
        frame_main.setParent(self)
        frame_main.setObjectName("frame_main")
        frame_main.setLayout(layout_top_hbox)

        self.frame_temps  = QtWidgets.QFrame()

        self.frame_temps.setStyleSheet("background-color:DarkSeaGreen")
        self.frame_temps.setParent(frame_main)
        self.frame_temps.setObjectName("frame_temps")
        self.frame_temps.setLayout(self.layout_temps_vbox)

        frame_summary = QtWidgets.QFrame()

        frame_summary.setStyleSheet("border: 2px solid black; border-radius:3px; background-color:Peru")
        frame_summary.setParent(frame_main)
        frame_summary.setObjectName("frame_summary")

        layout_summary_vbox = QtWidgets.QVBoxLayout()
        layout_summary_vbox.setObjectName("layout_summary_vbox")

        frame_summary.setLayout(layout_summary_vbox)

        frame_summary_date = QtWidgets.QFrame()
        frame_summary_date.setObjectName("frame_summary_date")
        
        layout_summary_date_hbox = QtWidgets.QHBoxLayout()
        layout_summary_date_hbox.setObjectName("layout_summary_date_hbox")

        frame_summary_date.setLayout(layout_summary_date_hbox)

        label_date_dow = QtWidgets.QLabel()
        label_date_dow.setText("Mon")

        label_date_dom = QtWidgets.QLabel()
        label_date_dom.setText("6 May")

        layout_summary_date_hbox.addWidget(label_date_dow)
        layout_summary_date_hbox.addWidget(label_date_dom)

        frame_summary_hilo = QtWidgets.QFrame()
        frame_summary_hilo.setObjectName("frame_summary_hilo")

        layout_summary_hilo_hbox = QtWidgets.QHBoxLayout()
        layout_summary_hilo_hbox.setObjectName("layout_summary_hilo_hbox")

        frame_summary_hilo.setLayout(layout_summary_hilo_hbox)

        frame_summary_icon = QtWidgets.QFrame()
        frame_summary_icon.setObjectName("frame_summary_icon")

        frame_summary_rain = QtWidgets.QFrame()
        frame_summary_rain.setObjectName("frame_summary_rain")

        frame_summary_sun = QtWidgets.QFrame()
        frame_summary_sun.setObjectName("frame_summary_sun")

        layout_summary_vbox.addWidget(frame_summary_date)
        layout_summary_vbox.addWidget(frame_summary_hilo)
        layout_summary_vbox.addWidget(frame_summary_icon)
        layout_summary_vbox.addWidget(frame_summary_rain)
        layout_summary_vbox.addWidget(frame_summary_sun)

        layout_top_hbox.addWidget(self.frame_temps)
        layout_top_hbox.addWidget(frame_summary)

        self.layout_temps_vbox.setParent(self.frame_temps)

        self.setCentralWidget(frame_main)

        self.show()

        self.request_data()

    def request_data(self):
        worker = PromWorker.Worker(prom_sensor = self.prom_sensor, signals = self.signals)

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

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()

    app.exec()
