import time
import requests

LOCAL = "http://localhost:8000"

while True:
    time.sleep(1)
    temp = requests.get(
        "https://io.adafruit.com/api/v2/khanhad69/feeds/iot-dadn.house-temp/data").json()
    temp = temp[0]["value"]

    humid = requests.get(
        "https://io.adafruit.com/api/v2/khanhad69/feeds/iot-dadn.house-humid/data").json()
    humid = humid[0]["value"]

    response = requests.post(f'{LOCAL}/create-temp-and-humid',
                             json={'temp': float(temp), 'humid': float(humid)}).json()

    print(temp, humid, response)

    # f1 = requests.post(
    #     "https://io.adafruit.com/api/v2/khanhad69/feeds/iot-dadn.fan-status-1/data", headers={
    #         'X-AIO-Key': 'aio_NmDN7114NKG08q56uoHiKtBNLwWy'
    #     }, json={'value': 1}).json()

    # f2 = requests.post(
    #     "https://io.adafruit.com/api/v2/khanhad69/feeds/iot-dadn.fan-status-2/data", headers={
    #         'X-AIO-Key': 'aio_NmDN7114NKG08q56uoHiKtBNLwWy'
    #     }, json={'value': 1}).json(),

    # f3 = requests.post(
    #     "https://io.adafruit.com/api/v2/khanhad69/feeds/iot-dadn.fan-status-3/data", headers={
    #         'X-AIO-Key': 'aio_NmDN7114NKG08q56uoHiKtBNLwWy'
    #     }, json={'value': 1}).json()

    print(f1, f2, f3)
