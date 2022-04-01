#!/usr/bin/env python3
# Written 2022 by Josh Cogliati
# This program is licensed under the terms of the GPL, version 2 or later

#palette.cpp is useful for understanding this format

import sys,os
import struct
from utils import read_unpack

if len(sys.argv) < 2:
    print(sys.argv[0], " palette.256 palette.txt")
    print("extracts palette.256 into palette.txt")
    sys.exit(-1)

f = open(sys.argv[1], "rb")

t = open(sys.argv[2], "w")

for i in range(256):
    t.write(str(i)+" ")
    t.write(str(read_unpack("BBB", f)))
    t.write("\n")

GR_FADE_LEVELS=34

for j in range(GR_FADE_LEVELS):
    for i in range(256):
        t.write(str(j)+" "+str(i)+" ")
        t.write(str(read_unpack("B", f)[0]))
        t.write("\n")
t.close()
