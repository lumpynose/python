import network
import esp32

from machine import RTC
import ntptime

import micropython

class GetPassword:
    def __init__(self):
        pass

    def getPassword(self):
        password = bytearray(32)
        nvs = esp32.NVS('password')
        nvs.get_blob('password', password)

        return password.decode()

class WiFi:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password

        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

    def connect(self):
        if not self.wlan.isconnected():
           print('\nconnecting to network...')
           self.wlan.connect(self.ssid, self.password)

           while not self.wlan.isconnected():
                pass

        return self.wlan

class SetTime:
    def __init__(self, pool = 'us.pool.ntp.org'):
        self.pool = pool
        self.rtc = RTC()

    def setTime(self):
        # synchronize with ntp
        # need to be connected to wifi
        ntptime.host = self.pool
        ntptime.settime() # set the rtc datetime from the remote server
        self.rtc.datetime()    # get the date and time in UTC

if __name__ == '__main__':
    getPassword = GetPassword()
    password = getPassword.getPassword()

    wifi = WiFi(ssid = 'TPI 2.4g', password = password)
    wlan = wifi.connect()
    print('network config:', wlan.ifconfig())

    setTime = SetTime()
    setTime.setTime()

    print("Memory Info - micropython.mem_info()")
    print("------------------------------------")
    micropython.mem_info()
    print("------------------------------------")

