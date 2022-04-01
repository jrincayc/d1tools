#!/usr/bin/env python3
# Written 2022 by Josh Cogliati
# This program is licensed under the terms of the GPL, version 2 or later

#See similar/2d/font.cpp and grs_font_read for format info

#Starts after "PSFN" and 4 byte int.

import sys,os
import struct
import PIL
import PIL.Image
from utils import read_unpack

def write_1_bit_font(data, width, height, filename):
    img = PIL.Image.new("1", (width,height))
    for h in range(height):
        l = data[h]
        for w in range(width):
            bit = (l&0x80)>>7
            if bit == 1:
                print("\u2588",end="")
            else:
                print(" ",end="")
            img.putpixel((w,h),bit)
            l = l << 1
        print()
    img.save(filename)

def write_color_font(data, width, height, filename):
    img = PIL.Image.new("L", (width, height))
    i = 0
    for h in range(height):
        for w in range(width):
            img.putpixel((w,h), data[i])
            i += 1
    img.save(filename)

if len(sys.argv) < 2:
    print(sys.argv[0], " fontfile")
    print("extracts fontfile into current directory")
    sys.exit(-1)

f = open(sys.argv[1], "rb")

psfn, length = read_unpack("<4sI", f)

if psfn != b"PSFN":
    print("not a descent PSFN font")
    sys.exit(-2)

print(psfn, length)

width, height, flags, baseline, minchar, maxchar = read_unpack("<HHHHBB", f)

print("width", width, "height", height, "flags", flags, "baseline", baseline, "minchar", minchar, "maxchar", maxchar)

FT_COLOR = 1
FT_PROPORTIONAL = 2
FT_KERNED = 4
print("flags", "COLOR", FT_COLOR & flags, "PROPORTIONAL", FT_PROPORTIONAL & flags, "KERNED", FT_KERNED & flags)

unknown1, data_offset, unknown2, widths_offset, kerndata_offset = read_unpack("<HIIII", f)

GRS_FONT_SIZE = 28
data_offset -= GRS_FONT_SIZE
widths_offset -= GRS_FONT_SIZE
kerndata_offset -= GRS_FONT_SIZE
print("unknown1", unknown1, "unknown2", unknown2, "do", data_offset, "wo", widths_offset, "ko", kerndata_offset)

width_sum = 0
width_array = []
for i in range(minchar, maxchar+1):
    cwidth = read_unpack("<H", f)[0]
    width_array.append(cwidth)
    width_sum += cwidth
    print('"'+chr(i)+'"', cwidth, end=",")

print("width_sum", width_sum)

if FT_COLOR & flags == 0:
    for i in range(minchar, maxchar+1):
        cwidth = width_array[i - minchar]
        data = f.read(height)
        print(repr(data))
        write_1_bit_font(data, cwidth, height, str(i)+".png")
else:
    for i in range(minchar, maxchar+1):
        cwidth = width_array[i - minchar]
        data = f.read(height*cwidth)
        write_color_font(data, cwidth, height, str(i)+".png")


#print("Kern data")
kerning_file = open("kerning_info.txt","w")
kern_first = f.read(1)
while kern_first != b'\xff':
    kern_first = ord(kern_first)+minchar
    kern_second = ord(f.read(1))+minchar
    kern_width = ord(f.read(1))
    print(kern_first, kern_second, kern_width, "#"+repr(chr(kern_first))+" "+repr(chr(kern_second)),file=kerning_file)
    kern_first = f.read(1)
#print(kern_first)
