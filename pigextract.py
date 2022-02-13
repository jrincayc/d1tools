#!/usr/bin/env python3
# Written 2022 by Josh Cogliati
# This program is licensed under the terms of the GPL, version 2 or later

#piggy.cpp is very useful for understanding pig files.

import sys,os
import struct

def read_unpack(format, file):
    size =struct.calcsize(format)
    data = file.read(size)
    return struct.unpack(format, data)

if len(sys.argv) < 2:
    print(sys.argv[0], " pigfile")
    print("extracts pigfile into current directory")
    sys.exit(-1)

f = open(sys.argv[1], "rb")

num_bitmaps, num_sounds = read_unpack("<II", f)

d1kind = True
print("bitmaps", num_bitmaps, "sounds", num_sounds)

bitmap_list = []
for i in range(num_bitmaps):
    if d1kind:
        name, dflags, width, height, flags, avg_color, offset = \
            read_unpack("<8sBBBBBI", f)
        print(name, dflags, width,"x",height, flags, avg_color,"offset", offset)
    else:
        name, dflags, width, height, wh_extra, flags, avg_color, offset = \
            read_unpack("<8sBBBBBBI", f)
        #XXX add wh_extra to width and height
        print(name, dflags, width,"x",height, wh_extra, flags, avg_color,"offset", offset)
    str_name = name.replace(b"\x00",b"_").decode()
    bitmap_list.append((str_name,offset))

sound_list = []
for i in range(num_sounds):
    name, length, data_length, offset = read_unpack("<8sIII", f)
    print(name, "length", length, "data_length", data_length, "offset", offset)
    str_name = name.replace(b"\x00",b"_").decode()
    sound_list.append((str_name,offset,data_length))

#Add dummy to always have offset in next
bitmap_list.append((None, sound_list[0][1]))
for i, bitmap_info in enumerate(bitmap_list[:-1]):
    name, start_offset = bitmap_info
    end_offset = bitmap_list[i+1][1]
    bitfile = open(name+".bit", "wb")
    bitfile.write(f.read(end_offset - start_offset))
    bitfile.close()


for sound_info in sound_list:
    name, offset,data_length = sound_info
    soundfile = open(name+".snd", "wb")
    soundfile.write(f.read(data_length))
    soundfile.close()
