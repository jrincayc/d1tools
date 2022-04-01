#!/usr/bin/env python3
# Written 2022 by Josh Cogliati
# This program is licensed under the terms of the GPL, version 2 or later

#piggy.cpp is very useful for understanding pig files.

import sys,os
import struct
from utils import read_unpack

if len(sys.argv) < 2:
    print(sys.argv[0], " pigfile")
    print("extracts pigfile into current directory")
    sys.exit(-1)

DBM_FLAG_LARGE = 128 # add 256 to width
DBM_FLAG_ABM = 64 # animated bitmap
DBM_NUM_FRAMES = 63 # number of frames


BM_FLAG_TRANSPARENT = 1
BM_FLAG_SUPER_TRANSPARENT = 2
BM_FLAG_NO_LIGHTING = 4
BM_FLAG_RLE = 8 # run length encoded see common/2d/rle.cpp
BM_FLAG_PAGED_OUT = 16
BM_FLAG_RLE_BIG = 32
f = open(sys.argv[1], "rb")

num_bitmaps, num_sounds = read_unpack("<II", f)

if num_bitmaps > 0xfff: #Probably the offset to the real data
    junk = f.read(num_bitmaps - 8)
    print("skipping", num_bitmaps)
    num_bitmaps, num_sounds = read_unpack("<II", f)

d1kind = True
print("bitmaps", num_bitmaps, "sounds", num_sounds)

bitmap_list = []
for i in range(num_bitmaps):
    if d1kind:
        name, dflags, width, height, flags, avg_color, offset = \
            read_unpack("<8sBBBBBI", f)
        if dflags & DBM_FLAG_LARGE > 0:
            width += 256
        print(name, dflags, width,"x",height, flags, avg_color,"offset", offset)
        print(" LARGE", dflags & DBM_FLAG_LARGE, "ANIMATED", dflags & DBM_FLAG_ABM, "NUM_FRAMES", dflags & DBM_NUM_FRAMES, "RLE", flags & BM_FLAG_RLE, "RLE_BIG", flags & BM_FLAG_RLE_BIG )
    else:
        name, dflags, width, height, wh_extra, flags, avg_color, offset = \
            read_unpack("<8sBBBBBBI", f)
        #XXX add wh_extra to width and height
        print(name, dflags, width,"x",height, wh_extra, flags, avg_color,"offset", offset)
    str_name = name.split(b"\x00")[0].decode()
    if dflags & DBM_FLAG_ABM != 0:
        str_name += "_" + str(dflags & DBM_NUM_FRAMES)
    print(" ",str_name)
    bitmap_list.append((str_name,offset,(width, height, flags)))

sound_list = []
for i in range(num_sounds):
    name, length, data_length, offset = read_unpack("<8sIII", f)
    print(name, "length", length, "data_length", data_length, "offset", offset)
    str_name = name.replace(b"\x00",b"_").decode()
    sound_list.append((str_name,offset,data_length))


def decode_rle(orig_data, width, height):
    new_data = bytearray(width*height)
    RLE_CODE = 0xe0
    RLE_COUNT = 0x1f
    i = 0
    j = 0
    for h in range(0, height):
        while i < len(orig_data):
            data = orig_data[i]
            if data & RLE_CODE == RLE_CODE:
                count = data & RLE_COUNT
                if count == 0:
                    i += 1
                    break
                i += 1
                data = orig_data[i]
                for k in range(count):
                    new_data[j] = data
                    j += 1
            else:
                new_data[j] = data
                j += 1
            i += 1
        j = h*width
    if i >= len(orig_data):
        print("ERROR Ran out of data before terminator")
    return bytes(new_data)

#Add dummy to always have offset in next
bitmap_list.append((None, sound_list[0][1]))
for i, bitmap_info in enumerate(bitmap_list[:-1]):
    name, start_offset, (width, height, flags) = bitmap_info
    end_offset = bitmap_list[i+1][1]
    bitfile = open(name+".bit", "wb")
    if flags & BM_FLAG_RLE > 0:
        data = decode_rle(f.read(end_offset - start_offset)[4:], width, height)
    else:
        data = f.read(end_offset - start_offset)
    bitfile.write(data)
    bitfile.close()
    pnmfile = open(name+".pnm", "wb")
    pnmfile.write(b'P5\n#created by pigextract.py\n%d %d\n255\n' % (width, height))
    pnmfile.write(data)
    pnmfile.close()


for sound_info in sound_list:
    name, offset,data_length = sound_info
    soundfile = open(name+".snd", "wb")
    soundfile.write(f.read(data_length))
    soundfile.close()
