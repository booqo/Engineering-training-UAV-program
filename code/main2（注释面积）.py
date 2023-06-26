import sensor, image, time

from pyb import UART
from pyb import Pin, Timer,LED

import json

first_threshold  = (34, 58, -128, -17, -24, -2)
#(30, 64, -1, 79, -13, 36)#红色
#(5, 69, 62, 22, 71, -50)#(73, 20, -8, 8, 69, 14)
secend_threshold  = (57, 5, -21, 18, -56, -6)#蓝色
zimu_threshold = (57, 94, -18, -4, -5, 19)

sensor.reset() # Initialize the camera sensor.

sensor.set_pixformat(sensor.RGB565) # use RGB565.

sensor.set_framesize(sensor.QQVGA) # use QQVGA for speed.

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
#def sending_data(cx_max,cy_max):

 #   global uart;

 #   data = ustruct.pack("<bbbb",              #格式为俩个字符俩个短整型(2字节)

 #                  0xff,

  ##                 0xfe,

  #                 int(cx_max),

  #                 int(cy_max));
#
                                                   #数据1

                                    # up sample by 4#数据2LCD_ShowStringLCD_ShowString

 #   uart.write(data);   #必须要传入一个字节数组

while(True):

    clock.tick() # Track elapsed milliseconds between snapshots().

    if uart.any():
            data = uart.read(1)  # 读取1个字节
            print("Received: ", data)
            if data == b'\x01':  #接受信息
                A = 1
            if data == b'\x02':
                A = 2
    img = sensor.snapshot() # Take a picture and return the image.





    if A == 0:
        blobs = img.find_blobs([first_threshold])

        if blobs:
                max_blob = find_max(blobs)
            #if 1100<max_blob.area():
                img.draw_cross(max_blob.cx(),max_blob.cy())

                img.draw_circle(max_blob.cx(),max_blob.cy(),max_blob.cx()-max_blob.x(), color = (255, 255, 255))
            #img.draw_rectangle()

            #X =int(max_blob.cx()-img.width()/2)

            #Y =int(max_blob.cy()-img.height()/2)
                X =int(max_blob.cx())
                Y =int(max_blob.cy())
          #  FH = bytearray([0xb3,0xb3])

          #  uart.write(FH)     #打印帧头

                data = bytearray([0x2c,0x12,X,Y,0x01,0x5b])

                uart.write(data)    #打印XY轴的偏移坐标

                print("X轴偏移坐标 : ",X)

                print("Y轴偏移坐标 : ",Y)

                print("帧率 : ",clock.fps())
                s = max_blob.area()
                print("角度：",s)

        else:
            data = bytearray([0x2c,0x12,0x00,0x00,0x00,0x5b])

            uart.write(data)
    if A == 1:
        blobs = img.find_blobs([secend_threshold])
        if blobs:
                max_blob = find_max(blobs)
            #if 1300<max_blob.area():
                img.draw_cross(max_blob.cx(),max_blob.cy())

                img.draw_circle(max_blob.cx(),max_blob.cy(),max_blob.cx()-max_blob.x(), color = (255, 255, 255))
            #img.draw_rectangle()

            #X =int(max_blob.cx()-img.width()/2)

            #Y =int(max_blob.cy()-img.height()/2)
                X =int(max_blob.cx())
                Y =int(max_blob.cy())
          #  FH = bytearray([0xb3,0xb3])

          #  uart.write(FH)     #打印帧头

                data = bytearray([0x2c,0x12,X,Y,0x01,0x5b])

                uart.write(data)    #打印XY轴的偏移坐标

                print("X轴偏移坐标 : ",X)

                print("Y轴偏移坐标 : ",Y)

                print("帧率 : ",clock.fps())
                s = max_blob.area()
                print("角度：",s)

        else:
            data = bytearray([0x2c,0x12,0x00,0x00,0x00,0x5b])

            uart.write(data)
    if A == 2:
        blobs = img.find_blobs([zimu_threshold])
        if blobs:
            max_blob = find_max(blobs)
            if 4000 <max_blob.area():
                img.draw_cross(max_blob.cx(),max_blob.cy())

                img.draw_circle(max_blob.cx(),max_blob.cy(),max_blob.cx()-max_blob.x(), color = (255, 255, 255))
            #img.draw_rectangle()

            #X =int(max_blob.cx()-img.width()/2)

            #Y =int(max_blob.cy()-img.height()/2)
                X =int(max_blob.cx())
                Y =int(max_blob.cy())
          #  FH = bytearray([0xb3,0xb3])

          #  uart.write(FH)     #打印帧头

                data = bytearray([0x2c,0x12,X,Y,0x01,0x5b])

                uart.write(data)    #打印XY轴的偏移坐标

                print("X轴偏移坐标 : ",X)

                print("Y轴偏移坐标 : ",Y)

                print("帧率 : ",clock.fps())
                s = max_blob.area()
                print("角度：",s)

        else:
            data = bytearray([0x2c,0x12,0x00,0x00,0x00,0x5b])

            uart.write(data)


#sending_data(blob.X,blob.Y)
