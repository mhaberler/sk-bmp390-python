import sys, json, threading
import board
import adafruit_bmp3xx


def outputSk():
    global n
    skData = {
        "updates": [
            {
                "values": [
                    {"path": "environment.bmp390.pressure", "value": bmp.pressure},
                    {"path": "environment.bmp390.temperature", "value": bmp.temperature},
                ]
            }
        ]
    }
    sys.stdout.write(json.dumps(skData))
    sys.stdout.write("\n")
    sys.stdout.flush()
    threading.Timer(1.0, outputSk).start()


# I2C setup
i2c = board.I2C()  # uses board.SCL and board.SDA
bmp = adafruit_bmp3xx.BMP3XX_I2C(i2c)
bmp.pressure_oversampling = 8
bmp.temperature_oversampling = 2

threading.Timer(1.0, outputSk).start()

for line in iter(sys.stdin.readline, b""):
    try:
        data = json.loads(line)
        sys.stderr.write(json.dumps(data))
    except:
        sys.stderr.write("error parsing json\n")
        sys.stderr.write(line)
