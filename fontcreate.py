#!/usr/bin/env python3
# Written 2022 by Josh Cogliati
# This program is licensed under the terms of the GPL, version 2 or later

#See similar/2d/font.cpp and grs_font_read for format info

import sys,os
import glob
import struct
import PIL
import PIL.Image

def write_pack(format, file, data):
    pack = struct.pack(format, *data)
    file.write(pack)

if len(sys.argv) < 2:
    print(sys.argv[0]," fontfile")
    print("creates fontfile from png files in current directory")
    sys.exit(-1)


image_files = glob.glob("*.png")

font_images = {}
minheight = None
maxheight = None
minwidth = None
maxwidth = None
width_sum = 0
for image_filename in image_files:
    num = int(image_filename[:-4])
    char_image = PIL.Image.open(image_filename)
    font_images[num] = char_image
    width, height = char_image.size
    width_sum += width
    if minheight is None:
        minwidth = width
        maxwidth = minwidth
        minheight = height
        maxheight = minheight
    else:
        minwidth = min(width, minwidth)
        maxwidth = max(width, maxwidth)
        minheight = min(height, minheight)
        maxheight = max(height, maxheight)

print("width",minwidth,maxwidth,"height", minheight, maxheight)
if minheight != maxheight:
    print("different heights, can't create font", minheight, maxheight)
    sys.exit(-2)

font_height = minheight

minchar = min(font_images)
maxchar = max(font_images)
print("character range", minchar, maxchar)
all_in = True
mode = font_images[minchar].mode
same_mode = True
for i in range(minchar, maxchar+1):
    if i not in font_images:
        all_in = False
        print("missing", i, chr(i))
    else:
        if mode != font_images[i].mode:
            same_mode = False
if not all_in:
    print("missing characters, quiting")
    sys.exit(-3)
if not same_mode:
    print("images not same mode")
    sys.exit(-4)
print("mode", mode)
if mode not in ["1", "L", "P"]:
    print("unsupported mode")
    sys.exit(-5)

f = open(sys.argv[1], "wb")

char_num = maxchar - minchar + 1
f.write(b"PSFN")
GRS_FONT_SIZE = 28
if mode == "1":
    # 28 bytes header, char_num*font_height image data, char_num*2 width info, 1 byte to say no kerning info
    length = GRS_FONT_SIZE + char_num*(font_height + 2) + 1
else:
    length = GRS_FONT_SIZE + font_height*width_sum + char_num*2 + 1

write_pack("<I", f, (length,))

FT_COLOR = 1
FT_PROPORTIONAL = 2
FT_KERNED = 4


write_pack("<HHHHBB", f, (maxwidth, font_height,
                          FT_PROPORTIONAL | FT_KERNED | (mode != "1"),
                          font_height, #XXX fix baseline
                          minchar, maxchar))

write_pack("<HIIII", f, (0, GRS_FONT_SIZE + char_num*2, 0,
                         GRS_FONT_SIZE, length - 1))

for i in range(minchar, maxchar +1):
    cwidth = font_images[i].size[0]
    write_pack("<H", f, (cwidth,))

for i in range(minchar, maxchar + 1):
    img = font_images[i]
    cwidth = img.size[0]
    if mode == "1":
        for h in range(font_height):
            l = 0
            k = 128
            for w in range(cwidth):
                if img.getpixel((w,h))>0:
                    l = l | k
                k = k >> 1
                #print(img.getpixel((w,h)), l)
            #print("l", l, bin(l))
            write_pack("B",f, (l,))
    else:
        for h in range(font_height):
            for w in range(cwidth):
                write_pack("B", f, (img.getpixel((w,h)),))

f.write(b"\xff") #XXX write actual kerning info
