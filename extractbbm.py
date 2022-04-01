#!/usr/bin/env python3
# Written 2022 by Josh Cogliati
# This program is licensed under the terms of the GPL, version 2 or later

# iff.cpp and iff_parse_bitmap is very useful for understanding bbm files.

import sys,os
import struct
from utils import read_unpack

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
    subsig, s_length = read_unpack(">4sL", f)
    print("subsig", subsig, s_length)
    if subsig == b"BMHD":
        w, h, x, y, nplanes, masking, compression, unknown, transparent_color, xaspect, yaspect, pagewidth, pageheight = read_unpack(">4h4Bh2B2h", f)
        print(w, h, x, y, nplanes, masking, compression, unknown, transparent_color, xaspect, yaspect, pagewidth, pageheight)
    pass
elif form == b"ANIM":
    #process
    pass
