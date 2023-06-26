import sensor, image, time
from pyb import UART
from pyb import Pin, Timer,LED
import json
red_threshold  = (24, 71, 75, -60, 11, 77)
blue_threshold  = (24, 71, -11, 1, -46, -23)
green_threshold= (20, 93, -67, -39, 31, 69)
byellow_threshold = (16, 65, -6, 14, 25, 67)
orange_threshold = (24, 96, 62, 15, 12, 65)
myellow_threshold = (61, 100, -35, 48, 28, 83)
uart = UART(3, 115200)
uart.init(115200, bits=8, parity=None, stop=1)
import sensor, image, time
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
uart = UART(3, 115200)
uart.init(115200, bits=8, parity=None, stop=1)
clock = time.clock()
roi = (0,47,208,238)
def find_max(blobs):
    max_size=0
    for blob in blobs:
        if blob[2]*blob[3] > max_size:
            max_blob=blob
            max_size = blob[2]*blob[3]
    return max_blob
A = 0
while(True):
    clock.tick()
    if uart.any():
        data = uart.read(1)
        print("Received: ", data)
        if data == b'\x01':
            A = 1
    img = sensor.snapshot()
    if A == 0:
        blobs = img.find_blobs([(61, 100, -35, 48, 28, 83)])
        if blobs:
           max_blob = find_max(blobs)
           if abs(max_blob.w()-max_blob.h())<max_blob.w()*0.3:
               img.draw_cross(max_blob.cx(),max_blob.cy())
               img.draw_circle(max_blob.cx(),max_blob.cy(),max_blob.cx()-max_blob.x(), color = (255, 255, 255))
               if max_blob.area()>400 :
                    X =int(max_blob.cx())
                    Y =int(max_blob.cy())
               else:
                    X = 0xff
                    Y = 0xff
           else:
                X = 0xff
                Y = 0xff
        else:
             X = 0xff
             Y = 0xff
    elif A == 1:
        img.mean(3, threshold=True, offset=5, invert=True)
        circles = img.find_circles(roi=roi,r_min=24, r_max=30, threshold=6000, r_margin=10)
        if circles:
            c_max = circles[0]
            for c in circles:
                if c.magnitude()>c_max.magnitude():
                    c_max = c
            img.draw_circle(c_max.x(), c_max.y(), c_max.r(), color=(0,255,0), size=10)
            print(c_max)
            X = int(c_max.x())
            Y = int(c_max.y())
        else:
            X = 0xff
            Y = 0xff
    print(clock.fps())
    xx = "%d" % (X)
    yy = "%d" % (Y)
    uart.write("#")
    uart.write(xx)
    uart.write("g")
    uart.write(yy)
    uart.write("!")
