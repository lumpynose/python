import sys

from PyQt6 import QtGui
from PyQt6 import QtWidgets
from PyQt6 import QtCore

import PromSensor
import PromWorker
import DateAndTime

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        date = DateAndTime.DateToday()
        self.threadpool = QtCore.QThreadPool()
        self.signals = PromWorker.WorkerSignals()

        self.signals.result.connect(self.process_result)

        self.prom_sensor = PromSensor.GetPromSensor()
        self.sensor_locations = { "prologue" : "garage", "accurite" : "outside", "oregon" : "attic" }
        self.widgets = { }

        frame_main = QtWidgets.QFrame()
        frame_main.setStyleSheet("background-color:gray")

        hbox_frame_main = QtWidgets.QHBoxLayout()
        frame_main.setLayout(hbox_frame_main)

        frame_temps  = QtWidgets.QFrame()

        frame_temps.setStyleSheet("background-color:DarkSeaGreen")

        self.vbox_temps = QtWidgets.QVBoxLayout()
        frame_temps.setLayout(self.vbox_temps)

        frame_summary = QtWidgets.QFrame()
        frame_summary.setStyleSheet("background-color:SkyBlue")

        vbox_summary = QtWidgets.QVBoxLayout()
        frame_summary.setLayout(vbox_summary)

        #frame_summary_date = QtWidgets.QFrame()
        #frame_summary_date.setStyleSheet("background-color:DarkKhaki; border: 1px solid; border-radius:6px")

        #hbox_summary_date = QtWidgets.QHBoxLayout()
        #frame_summary_date.setLayout(hbox_summary_date)

        #hbox_summary_date.setContentsMargins(0, 0, 0, 0);

        label_summary_date_dow = QtWidgets.QLabel()
        label_summary_date_dow.setText(date.dayOfWeek() + ", " + date.date())
        label_summary_date_dow.setAlignment(QtCore.Qt.Alignment.AlignCenter)
        label_summary_date_dow.setStyleSheet("background-color:PaleTurquoise; border: 1px solid; border-radius:4px;")

        #hbox_summary_date.addWidget(label_summary_date_dow)

        frame_summary_hilo = QtWidgets.QFrame()
        frame_summary_hilo.setStyleSheet("background-color:DarkKhaki; border: 1px solid; border-radius:6px")

        hbox_summary_hilo = QtWidgets.QHBoxLayout()
        frame_summary_hilo.setLayout(hbox_summary_hilo)

        label_summary_hilo_low = QtWidgets.QLabel("low")
        label_summary_hilo_low.setAlignment(QtCore.Qt.Alignment.AlignCenter)
        label_summary_hilo_low.setStyleSheet("border: 1px solid; border-radius:2px")

        label_summary_hilo_high = QtWidgets.QLabel("high")
        label_summary_hilo_high.setAlignment(QtCore.Qt.Alignment.AlignCenter)
        label_summary_hilo_high.setStyleSheet("border: 1px solid; border-radius:2px")

        hbox_summary_hilo.addWidget(label_summary_hilo_low)
        hbox_summary_hilo.addWidget(label_summary_hilo_high)

        label_summary_icon = QtWidgets.QLabel("icon")

        label_summary_rain = QtWidgets.QLabel("rain")
        label_summary_rain.setAlignment(QtCore.Qt.Alignment.AlignCenter)

        frame_summary_sun = QtWidgets.QFrame()
        frame_summary_sun.setStyleSheet("background-color:DarkKhaki; border: 2px solid; border-radius:6px")

        hbox_summary_sun = QtWidgets.QHBoxLayout()
        frame_summary_sun.setLayout(hbox_summary_sun)

        label_summary_sun_sunrise = QtWidgets.QLabel("sunrise")
        label_summary_sun_sunrise.setAlignment(QtCore.Qt.Alignment.AlignCenter)
        label_summary_sun_sunrise.setStyleSheet("border: 1px solid; border-radius:2px")

        label_summary_sun_sunset = QtWidgets.QLabel("sunset")
        label_summary_sun_sunset.setAlignment(QtCore.Qt.Alignment.AlignCenter)
        label_summary_sun_sunset.setStyleSheet("border: 1px solid; border-radius:2px")

        hbox_summary_sun.addWidget(label_summary_sun_sunrise)
        hbox_summary_sun.addWidget(label_summary_sun_sunset)

        #vbox_summary.addWidget(frame_summary_date)
        vbox_summary.addWidget(label_summary_date_dow)
        vbox_summary.addWidget(frame_summary_hilo)
        vbox_summary.addWidget(label_summary_icon)
        vbox_summary.addWidget(label_summary_rain)
        vbox_summary.addWidget(frame_summary_sun)
        vbox_summary.addStretch()

        hbox_frame_main.addWidget(frame_temps)
        hbox_frame_main.addWidget(frame_summary)

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

        frame_sensor.setStyleSheet("border: 2px solid; background-color:SkyBlue; border-radius:6px")

        self.vbox_temps.addWidget(frame_sensor)

        location = self.sensor_locations.get(sensor)

        label_title = QtWidgets.QLabel()

        if location:
            label_title.setText("{} ({})".format(location, sensor))
        else:
            label_title.setText(sensor)

        label_title.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        label_title.setStyleSheet("border: 1px solid; background-color:DarkKhaki; border-radius:2px")
        label_title.setAlignment(QtCore.Qt.Alignment.AlignCenter)
        label_title.setFont(QtGui.QFont("Cooper Lt BT", 12))

        label_value = QtWidgets.QLabel()

        label_value.setText("{:.1f}".format(float(value)))

        label_value.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        label_value.setStyleSheet("border: 1px solid; background-color:PaleTurquoise; border-radius:4px")
        label_value.setAlignment(QtCore.Qt.Alignment.AlignCenter)
        label_value.setFont(QtGui.QFont("Cooper Blk BT", 32))

        vbox_sensor = QtWidgets.QVBoxLayout(frame_sensor)

        vbox_sensor.addWidget(label_title)
        vbox_sensor.addWidget(label_value)

        frame_sensor.setLayout(vbox_sensor)

        self.widgets.update({ sensor : label_value })

    def closeEvent(self, event):
        event.accept()
        sys.exit()

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()

    app.exec()
