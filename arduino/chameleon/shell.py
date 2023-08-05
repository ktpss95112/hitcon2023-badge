#!/usr/bin/python -i
import serial
arduino = serial.Serial('/dev/ttyUSB0')

def __readline():
    line = arduino.readline().lstrip(b'\x00')
    return chr(line[0]), line[1:]

def __wait_reply():
    while True:
        family, content = __readline()
        print(content)
        if family in 'IOE':
            break

def init():
    arduino.write(b'INIT\n')
    __wait_reply()

def flush_serial():
    print(arduino.read(1))

def read(blkid: int):
    arduino.write(f'READ\n{blkid}\n'.encode())
    res = arduino.read(1)
    if res == b'O':
        print(arduino.read(16))
        arduino.read()
    else:
        print(arduino.readline())

def read_uid():
    arduino.write(b'READ_UID\n')
    res = arduino.read(1)
    if res == b'O':
        print(arduino.read(4))
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

def example():
    init()
    read(1)
    write(1, b'cafebabedeadbeef')
    write_uid(b'\xde\xca\xf0\xa0')

if __name__ == '__main__':
    import sys
    args_to_python = sys.orig_argv[:len(sys.argv)+1]

    if '-i' not in args_to_python:
        print(f'Usage: python3 -i {__file__}', file=sys.stderr)
        print(f'Usage: {__file__}')
        exit(1)