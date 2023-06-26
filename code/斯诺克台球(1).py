import sensor, image, time

from pyb import UART

import json

red_threshold  = (63, 26, -60, 72, 62, -62)  #(73, 20, -8, 8, 69, 14)

sensor.reset() # Initialize the camera sensor.

sensor.set_pixformat(sensor.RGB565) # use RGB565.

sensor.set_framesize(sensor.QQVGA) # use QQVGA for speed.

sensor.skip_frames(10) # Let new settings take affeOpenMV_Xct.

sensor.set_auto_whitebal(False) # turn this off.

clock = time.clock() # Tracks FPS.

uart = UART(3, 115200)

uart.init(115200, bits=8, parity=None, stop=1)  #8位数据位，无校验位，1位停止位

def find_max(blobs):

    max_size=0

    for blob in blobs:

        if blob[2]*blob[3] > max_size:

            max_blob=blob

            max_size = blob[2]*blob[3]

    return max_blob

    def sending_data(cx_max,cy_max):

        global uart;

        data = ustruct.pack("<bbbb",              #格式为俩个字符俩个短整型(2字节)

                   0xff,

                   0xfe,

                   int(cx_max),

                   int(cy_max));

                                                   #数据1

                                    # up sample by 4#数据2LCD_ShowStringLCD_ShowString

        uart.write(data);   #必须要传入一个字节数组

while(True):

    clock.tick() # Track elapsed milliseconds between snapshots().

    img = sensor.snapshot() # Take a picture and return the image.



    blobs = img.find_blobs([red_threshold])

    if blobs:

        max_blob = find_max(blobs)

        img.draw_cross(max_blob.cx(),max_blob.cy())

        img.draw_circle(max_blob.cx(),max_blob.cy(),max_blob.cx()-max_blob.x(), color = (255, 255, 255))
        #img.draw_rectangle()

        X =int(max_blob.cx()-img.width()/2)

        Y =int(max_blob.cy()-img.height()/2)

      #  FH = bytearray([0xb3,0xb3])

      #  uart.write(FH)     #打印帧头

        data = bytearray([0xb3,0xb3,X,Y,0x5b])

        uart.write(data)    #打印XY轴的偏移坐标

        print("X轴偏移坐标 : ",X)

        print("Y轴偏移坐标 : ",Y)

        print("帧率 : ",clock.fps())

sending_data(blob.X,blob.Y)
