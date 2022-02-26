#!/usr/bin/env python3
# Written 2022 by Josh Cogliati
# This program is licensed under the terms of the GPL, version 2 or later

# iff.cpp and iff_parse_bitmap is very useful for understanding bbm files.

import sys,os
import struct

def read_unpack(format, file):
    size =struct.calcsize(format)
    data = file.read(size)
    return struct.unpack(format, data)

if len(sys.argv) < 2:
    print(sys.argv[0], " bbmfile")
    print("converts bbmfile into ?")
    sys.exit(-1)

f = open(sys.argv[1], "rb")

sig, length = read_unpack(">4sL", f)

print("sig", sig, "length", length)

if sig != b"FORM":
    print("not a bbm file")
    sys.exit(-2)

form = read_unpack("4s", f)[0]

print("form", form)

if form in [b"PBM ", b"ILBM"]:
    #process
    pass
elif form == b"ANIM":
    #process
    pass
