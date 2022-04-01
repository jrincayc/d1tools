#!/usr/bin/env python3
# Written 2022 by Josh Cogliati
# This program is licensed under the terms of the GPL, version 2 or later

#polyobj read_model_file is very useful for understanding pof files.

import sys,os
import struct
from utils import read_unpack

if len(sys.argv) < 2:
    print(sys.argv[0]," file.pof")
    sys.exit(-1)

f = open(sys.argv[1],"rb")

head, version = read_unpack("<4sH", f)
print(head, version)
if head != b"PSPO":
    print("not a pof file")
    sys.exit(-2)

def read_vecs(num, file):
    vecs = []
    for i in range(num):
        vecs.append(read_unpack("<3I", file))
    return vecs

while True:
    try:
        kind, length = read_unpack("<4sI", f)
    except struct.error:
        break
    if kind == b'TXTR':
        num_str = read_unpack("<H", f)[0]
        data = f.read(length - 2)
        textures = data.split(b'\x00')[:num_str]
        print("textures", textures)
    elif kind == b'OHDR':
        n_models, rad = read_unpack("<II", f)
        pmmin = read_vecs(1, f)
        pmmax = read_vecs(1, f)
        print("object header", n_models, rad, pmmin, pmmax)
    else:
        data = f.read(length)
        print(kind, length, data[:60])
