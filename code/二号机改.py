import sensor, image, time

from pyb import UART

from pyb import Pin, Timer,LED

import json

red_threshold  = (5, 69, 62, 22, 71, -50)  #(73, 20, -8, 8, 69, 14)
blue_threshold  = (26, 92, -33, 69, -51, -13)
sensor.reset() # Initialize the camera sensor.

sensor.set_pixformat(sensor.RGB565) # use RGB565.

sensor.set_framesize(sensor.QVGA) # use QQVGA for speed.

sensor.skip_frames(10) # Let new settings take affeOpenMV_Xct.

sensor.set_auto_whitebal(False) # turn this off.

clock = time.clock() # Tracks FPS.

uart = UART(3, 115200)


uart.init(115200, bits=8, parity=None, stop=1)  #8位数据位，无校验位，1位停止位

led1 = LED(1)
led1.on()
led2 = LED(2)
led2.on()
led3 = LED(3)
led3.on()

def find_max(blobs):

    max_size=0

    for blob in blobs:

        if blob[2]*blob[3] > max_size:

            max_blob=blob

            max_size = blob[2]*blob[3]

    return max_blob

A = 0
while(True):

    clock.tick() # Track elapsed milliseconds between snapshots().
    if uart.any():
        data = uart.read(1)  # 读取1个字节
        print("Received: ", data)
        if data == b'\x01':
            A = 1
    img = sensor.snapshot() # Take a picture and return the image.


    if A == 0:
        blobs = img.find_blobs([blue_threshold])
        if blobs:

           max_blob = find_max(blobs)

           img.draw_cross(max_blob.cx(),max_blob.cy())

           img.draw_circle(max_blob.cx(),max_blob.cy(),max_blob.cx()-max_blob.x(), color = (255, 255, 255))
        #img.draw_rectangle()

           if max_blob.area()>400 :
          #  FH = bytearray([0xb3,0xb3])

          #  uart.write(FH)     #打印帧头

                X =int(max_blob.cx())

                Y =int(max_blob.cy())

           else:
                X = 0xff
                Y = 0xff


        else:
             X = 0xff
             Y = 0xff
    elif A == 1:

        blobs = img.find_blobs([red_threshold])
        if blobs:

            max_blob = find_max(blobs)

            img.draw_cross(max_blob.cx(),max_blob.cy())

            img.draw_circle(max_blob.cx(),max_blob.cy(),max_blob.cx()-max_blob.x(), color = (255, 255, 255))
            #img.draw_rectangle()

            if max_blob.area()>400 :
          #  FH = bytearray([0xb3,0xb3])

          #  uart.write(FH)     #打印帧头

                 X =int(max_blob.cx())

                 Y =int(max_blob.cy())

            else:
                 X = 0xff
                 Y = 0xff


        else:
             X = 0xff
             Y = 0xff
    print("X轴偏移坐标 : ",X)
    print("Y轴偏移坐标 : ",Y)
    print("帧率 : ",clock.fps())
    xx="%d" % (X)
    yy="%d" % (Y)
    uart.write("#")
    uart.write(xx)
    uart.write("g")
    uart.write(yy)
    uart.write("!")
#sending_data(blob.X,blob.Y)
