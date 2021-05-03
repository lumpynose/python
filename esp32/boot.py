import network
import esp32

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

        print('network config:', self.wlan.ifconfig())

if __name__ == '__main__':
    password = bytearray(9)
    nvs = esp32.NVS('password')
    nvs.get_blob('password', password)

    wifi = WiFi(ssid = 'TPI 2.4g', password = password.decode())
    wifi.connect()
