#!/usr/bin/env python3
# Written 2022 by Josh Cogliati
# This program is licensed under the terms of the GPL, version 2 or later

#polyobj read_model_file is very useful for understanding pof files.
#similar/3d/interp.cpp is also useful

import sys,os, enum
import struct
from utils import read_unpack

class Op(enum.Enum):
    EOF = 0
    DEFPOINTS = 1
    FLATPOLY = 2
    TMAPPOLY = 3
    SORTNORM = 4
    RODBM = 5
    SUBCALL = 6
    DEFP_START = 7
    GLOW = 8


def interp_IDTA(data):
    def get_short(data, index):
        return struct.unpack('<H', data[index:index+2])[0]
    def get_int(data, index):
        return struct.unpack('<I', data[index:index+4])[0]
    def get_vec(data, index):
        return struct.unpack('<3I', data[index:index+12])
    data_index = 0
    op = get_short(data, data_index)
    while data_index < len(data): #op != Op.EOF:
        op_num = get_short(data, data_index)
        op = Op(op_num)
        print(op)
        if op == Op.DEFPOINTS:
            n = get_short(data, data_index + 2)
            record_size = n * (3*4) + 4 + 4
            print(n, record_size)
        elif op == Op.DEFP_START:
            n = get_short(data, data_index + 2)
            record_size = n * (3*4) + 4 + 4
            print(n, record_size)
        elif op == Op.FLATPOLY:
            n = get_short(data, data_index + 2)
            record_size = 30 + ((n & ~1) + 1) * 2
            print(n, record_size)
        elif op == Op.TMAPPOLY:
            n = struct.unpack('<H', data[data_index+2:data_index+4])[0]
            record_size = 30 + ((n & ~1) + 1) * 2 + n * 12
            print(n, record_size)
            print(get_vec(data, data_index + 4), get_vec(data, data_index + 16))
            print(get_short(data, data_index + 28))
            tmap_shorts = []
            for i in range(n):
                tmap_shorts.append(get_short(data, data_index + 30 + i * 2))
            print(tmap_shorts)
            tmap_ints = []
            for i in range(n):
                tmap_ints.append((get_int(data, data_index + 30+((n&~1)+1)*2+ i * 8),get_int(data, data_index + 30+((n&~1)+1)*2+ i * 8 + 4)))
            print(tmap_ints)
        elif op == Op.SORTNORM:
            record_size = 32
        elif op == Op.RODBM:
            record_size = 36
        elif op == Op.SUBCALL:
            record_size = 20
        elif op == Op.GLOW:
            record_size = 4
            glow_num = get_short(data, data_index + 2)
            print(glow_num, record_size)
        elif op == Op.EOF:
            record_size = 2
        else:
            record_size = 2
            print("Unknown Op", op_num)
        print(data[data_index:data_index + record_size][:18])
        data_index += record_size
        #print(data[data_index-4:data_index + 40])
    pass

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
        print("kind", kind, length)
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
    elif kind == b'SOBJ':
        n, submodule_parents = read_unpack("<HH", f)
        norms = read_vecs(1, f)
        pnts = read_vecs(1, f)
        offsets = read_vecs(1, f)
        rads, ptrs = read_unpack("<II", f)
        print(n, submodule_parents, norms, pnts, offsets, rads, ptrs)
    elif kind == b'GUNS':
        n_guns = read_unpack("<I", f)[0]
        print('n_guns', n_guns)
        for ni in range(n_guns):
            gun_id, submodel = read_unpack("<HH", f)
            gun_points = read_vecs(1, f)
            print(ni, gun_id, submodel, gun_points)
            if version >= 7:
                gun_dir = read_vecs(1, f)
                print(gun_dir)
    elif kind == b'ANIM':
        n_frames = read_unpack("<H",f)[0]
        for model in range(0, n_models):
            for frame in range(0, n_frames):
                angles = read_unpack("<HHH", f)
                print("angles", model, frame, angles)
    elif kind == b'IDTA':
        data = f.read(length)
        print(kind, length, data[:60])
        interp_IDTA(data)
    else:
        data = f.read(length)
        print(kind, length, data[:60])
