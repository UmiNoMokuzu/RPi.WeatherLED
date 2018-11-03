import RPi.GPIO as gpio
import time
import request
import json
import urllib.request
import re

# 警告表示抑制
gpio.setwarnings(False)

# 使用するGPIOの設定
gpio.setmode(gpio.BCM)

gpio.setup(26, gpio.OUT) # blue   -> Rainy
gpio.setup(19, gpio.OUT) # whilte -> Cloudy
gpio.setup(13, gpio.OUT) # orange -> Sunny

# WebAPI URL
base_url  = "http://weather.livedoor.com/forecast/webservice/json/v1"

# +----------------------------------------------------------------------------+
# | Livedoor Weather Web Service / LWWS                                        |
# +----------------------------------------------------------------------------+
def get_livedoor_wh_api(area_code):

    url = base_url + "?city=%s" % (area_code)
    json_tree = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
    telop = json_tree['forecasts'][0]['telop']

    return telop

# +----------------------------------------------------------------------------+
# | Main                                                                       |
# +----------------------------------------------------------------------------+
if __name__ == '__main__':

    try:
        while True:
            weather = get_livedoor_wh_api("270000")

            print(weather)

            if re.search("晴.*", weather):
                gpio.output(13, gpio.HIGH)
            else:
                gpio.output(13, gpio.LOW)

            if re.search("曇.*", weather):
                gpio.output(19, gpio.HIGH)
            else:
                gpio.output(19, gpio.LOW)

            if re.search("雨.*", weather):
                gpio.output(26, gpio.HIGH)
            else:
                gpio.output(26, gpio.LOW)

            # interval 300sec(5min)
            time.sleep(300)

    except KeyboardInterrupt:
        gpio.cleanup()