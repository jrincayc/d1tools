#!/usr/bin/env python3
# Written 2022 by Josh Cogliati
# This program is licensed under the terms of the GPL, version 2 or later

#See similar/2d/font.cpp and grs_font_read for format info

#Starts after "PSFN" and 4 byte int.

import sys,os
import struct

def read_unpack(format, file):
    size =struct.calcsize(format)
    data = file.read(size)
    return struct.unpack(format, data)

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
for i in range(minchar, maxchar+1):
    cwidth = read_unpack("<H", f)[0]
    width_sum += cwidth
    print('"'+chr(i)+'"', cwidth, end=",")

print("width_sum", width_sum)
