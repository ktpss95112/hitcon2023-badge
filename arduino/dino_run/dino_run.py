import serial
import time

port = '/dev/ttyUSB0'

s = serial.Serial(port)
print(s)
while True:
    data = s.readline().strip()
    print(data)

s.close()