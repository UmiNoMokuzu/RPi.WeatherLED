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
gpio.setup(21, gpio.OUT) # green  -> Snowy
gpio.setup(19, gpio.OUT) # whilte -> Cloudy
gpio.setup(13, gpio.OUT) # orange -> Sunny

# WebAPI 設定
base_url           = "http://weather.livedoor.com/forecast/webservice/json/v1"
receive_interval   = 300                   # sec
err_blink_interval = receive_interval - 2  # sec

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

            if re.search("雪.*", weather):
                gpio.output(21, gpio.HIGH)
            else:
                gpio.output(21, gpio.LOW)
           
            # 通信異常等で天気が正常受信できない場合は
            # 全LEDを1.0sec間隔で点滅させる
            err_blink_count = 0

            if re.search("[^晴|曇|雨|雪].*", weather):
               while True:

                   # 指定秒数経過したらエラー通知点滅OFF
                   if err_blink_count == err_blink_interval:
                       break

                   time.sleep(0.5)

                   gpio.output(13, gpio.HIGH)
                   gpio.output(19, gpio.HIGH)
                   gpio.output(21, gpio.HIGH)
                   gpio.output(26, gpio.HIGH)
                   
                   time.sleep(0.5)
                   
                   gpio.output(13, gpio.LOW)
                   gpio.output(19, gpio.LOW)
                   gpio.output(21, gpio.LOW)
                   gpio.output(26, gpio.LOW)

                   err_blink_count = err_blink_count + 1

            # 指定秒数待ってからAPIへリクエストする
            time.sleep(receve_interval)

    except KeyboardInterrupt:
        gpio.cleanup()
