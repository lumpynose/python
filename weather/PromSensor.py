import requests
import json
import time
import datetime

class GetPromSensor():
    def __init__(self):
        self.promUrl = "http://192.168.1.7:9090/api/v1"
        pass

    def hourstosecs(self, hours):
        return(hours * 60 * 60)

    def hoursago(self, hours, time):
        return(time - self.hourstosecs(hours))

    def get_sensor_range(self, hours):
        endsecs = time.time()
        startsecs = self.hoursago(hours, endsecs)

        query = self.promUrl + "/query_range?query=prologue_temperature&start={}&end={}&step=60s".format(startsecs, endsecs)

        req = requests.get(query)

        parsed = json.loads(req.text)

        #
        # FIX THIS
        #
        for temp in parsed["data"]["result"][0]["values"]:
            print("{}, {}".format(time.ctime(temp[0]), temp[1]))

        return(None)

    def get_sensor_latest(self):
        sensors = ( "prologue", "accurite", "oregon" )

        result = { }

        for sensor in sensors:
            query = self.promUrl + "/query?query=" + sensor + "_temperature"

            req = requests.get(query)

            parsed = json.loads(req.text)

            value = parsed["data"]["result"][0]["value"]

            result[sensor] = value[1]

        return(result)

if __name__ == '__main__':
    getSensor = GetPromSensor()

    # print("range: {}".format(getSensor.get_sensor_range(12)))

    sensors = getSensor.get_sensor_latest()
    print(sensors)
    for sensor in list(sensors.keys()):
        print("sensor: {}, {}".format(sensor, sensors[sensor]))
    #print("latest: {}".format(getSensor.get_sensor_latest()))
