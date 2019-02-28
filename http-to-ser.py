# This file runs an http server and sends some of what it gets over serial to the arduino

from flask import Flask
import serial
app = Flask(__name__)
ser = None
try:
    ser = serial.Serial("/dev/ttyACM0")
except:
    #ser = serial.Serial("/dev/ttyAMA0")
    print("Not connected")

@app.route("/<raw>")
def hello(raw):
    print(raw)
    str = "::w"
    try:
        w = raw.index("w")
        s = raw.index("s")
        h = raw.index("h")
        y = raw.index("y")
        str += chr(int(raw[w+1:s])) + "s" + chr(int(raw[s+1:h])) + "h" + chr(int(raw[h+1:y])) + "y" + chr(int(raw[y+1:]))
        #print(str.encode('utf-8'))
        print("Sending " + str)
        ser.write(str.encode('utf-8')) # send the command
        ser.flushInput()
        #print(raw.encode('utf-8'))
        #print(ser.read(100))
        print("complete\n")
        return "good"#raw# + " " + str(ser.outWaiting()) + " " + str(ser.inWaiting())
    except Exception as e:
        print(e)
        return "bad"

if __name__ == "__main__":
        app.run(host='0.0.0.0', port=80, debug=True)
