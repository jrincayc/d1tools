#!/usr/bin/env python3
# Written 2022 by Josh Cogliati
# This program is licensed under the terms of the GPL, version 2 or later

#palette.cpp is useful for understanding this format

import sys,os
import struct

if len(sys.argv) < 2:
    print(sys.argv[0], " palette.txt palette.256")
    print("extracts palette.txt into palette.256")
    sys.exit(-1)

t = open(sys.argv[1], "r")
f = open(sys.argv[2], "wb")

for i in range(256):
    line = t.readline()
    line = line.strip().split("#")[0] #Strip comments starting with #
    nums = line.split(maxsplit=1)[1].strip()[1:-1].split(",")
    for j in nums:
        f.write(struct.pack("B",int(j)))

GR_FADE_LEVELS=34
for j in range(GR_FADE_LEVELS):
    for i in range(256):
        line = t.readline()
        line = line.strip().split("#")[0] #Strip comments starting with #
        num = line.split()[2]
        f.write(struct.pack("B",int(num)))
