#!/usr/bin/env python3

import serial 
import time

ser = serial.Serial(
<<<<<<< HEAD
    port = '/dev/ttyAMA0',
=======
    port = '/dev/ttyUSB0',
>>>>>>> Upload all file run on pi
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = 100
)
print("Chay chuong trinh")
s = 0
s1 = "" # Dùng cho cộng ký tự
s2 = ""
k1 = 0
k2 = 0

testVelR = 1.23
testVelL = 2.54

try:
    while True:
        # Receive
        if ser.in_waiting: # Wait for data to arrive
            c = ser.read()
            c_decode = c.decode('utf-8')

            if k1 == 0:
                if c_decode != 'r':
                    s1 += c_decode
            if c_decode == 'r':
                k1 = 1
                k2 = 1
            if k2 == 1:
                if c_decode != 'r' and c_decode != 'l':
                    s2 += c_decode
            if c_decode == 'l':
                k2 = 0
            if c_decode == '\n':
                s = s1 + ' ' + s2
                print(s)
                k1 = 0
                s1 = ""
                s2 = ""
                s3 = ""
                s = ""

        # Transmit
        message = str(testVelR) + "r" + str(testVelL) + "l"
        ser.write(message.encode())
        ser.flush() # Xóa bộ nhớ đệm
<<<<<<< HEAD
        time.sleep(0.01) # Add a delay of 1 second
=======
        time.sleep(0.01) # Add a delay of 0.01 second
>>>>>>> Upload all file run on pi

except KeyboardInterrupt:
    # Đóng kết nối khi nhấn Ctrl+C
    ser.close()

