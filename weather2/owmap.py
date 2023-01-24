import json
import time

class OwMap():
    def __init__(self):
        now = time.mktime(time.localtime())
        pass

    def low_hourly_from_loads(self, onecall_loads):
        if onecall_loads['hourly']:
            low = 100
            hourly = onecall_loads["hourly"]

            for k in hourly:
                date = time.localtime(int(k["dt"]))

                # go 12 hours in the past and
                # 12 hours in the future?

                temp = k["temp"]
                if temp < low:
                    low = temp

            return int("{:.0f}".format(low))

    def hourly_from_loads(self, onecall_loads):
        if onecall_loads['hourly']:
            temps = { }
            hourly = onecall_loads["hourly"]

            for k in hourly:
                temp = k["temp"]
                time = k["dt"]
                temps.update({ time : temp })

            return temps

    def secs_to_date(self, secs):
        return time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(secs))
    
if __name__ == '__main__':
    owmap = OwMap()
    
    with open("onecall.json", "r") as onecall:
        json_data = onecall.read()

    print("data type", type(json_data))
        
    # turns string / json into dict
    onecall_loads = json.loads(json_data)
    print("loads type", type(onecall_loads))
    #print("loads", onecall_loads)
    print("loads min:", owmap.low_hourly_from_loads(onecall_loads))

    print("loads:")
    temps = owmap.hourly_from_loads(onecall_loads)
    for key in temps.keys():
        print(owmap.secs_to_date(key), "  ", temps.get(key))
