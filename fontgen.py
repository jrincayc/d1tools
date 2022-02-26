#!/usr/bin/env python3

#uses files from xfd and a screen capture
# ../../fontgen.py ../10x20.png 15 144 25 10 29 20
# ../../fontgen.py ../5x7.png 17 144 24 5 16 7
# ../../fontgen.py ../7x13B.png 16 144 24 7 22 13

import sys,os
import struct
import PIL
import PIL.Image

filename = sys.argv[1]

img = PIL.Image.open(filename)
#40,291, 49,307

x_begin = int(sys.argv[2]) #15
y_begin = int(sys.argv[3]) #144
dx = int(sys.argv[4]) #25
x_width = int(sys.argv[5]) #10
dy = int(sys.argv[6]) #29
y_height = int(sys.argv[7]) #20

i = 0
for y_start in range(y_begin, y_begin+int(dy*15.5), dy):
    for x_start in range(x_begin, x_begin+int(dx*15.5), dx):
        part = img.copy().crop((x_start,y_start,x_start+x_width,y_start+y_height))
        #print("mode", part.mode, part.getpixel((0,0)))
        new_part = PIL.Image.new("1", part.size)
        for x in range(0,part.size[0]):
            for y in range(0, part.size[1]):
                new_part.putpixel((x,y), part.getpixel((x,y))[0] == 0)
        new_part.save("%03i.png" % i)
        i += 1
