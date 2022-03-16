#!/usr/bin/env python3
# Written 2022 by Josh Cogliati
# This program is licensed under the terms of the GPL, version 2 or later

#text.cpp is useful for understanding this

import sys,os

def encode_rotate_left(x):
    return 0xff & ((x >> 7) | (x << 1))

def get_char(x):
    return chr(encode_rotate_left(encode_rotate_left(x) ^ 0xd3))


if len(sys.argv) < 2:
    print(sys.argv[0], "bitmaps.bin")
    sys.exit(-1)


f = open(sys.argv[1], "rb")

while True:
    a = f.read(1)
    if len(a) > 0:
        print(get_char(ord(a)),end="")
    else:
        break
