#!/usr/bin/python -i
import serial
arduino = serial.Serial('/dev/ttyUSB0')

def readline():
    line = arduino.readline().lstrip(b'\x00')
    return chr(line[0]), line[1:]

def wait_reply():
    while True:
        family, content = readline()
        print(content)
        if family in 'IOE':
            break

def init():
    arduino.write(b'INIT\n')
    wait_reply()

def flush():
    print(arduino.read(1))

def read(blkid: int):
    arduino.write(f'READ\n{blkid}\n'.encode())
    res = arduino.read(1)
    if res == b'O':
        print(arduino.read(16))
        arduino.read()
    else:
        print(arduino.readline())

def write(blkid: int, data: bytes):
    assert len(data) == 16
    arduino.write(f'WRITE\n{blkid}\n'.encode())
    arduino.write(data + b'\n')
    print(arduino.readline())

def write_uid(data: bytes):
    assert len(data) == 4
    arduino.write(f'WRITE_UID\n'.encode())
    arduino.write(data + b'\n')
    print(arduino.readline())