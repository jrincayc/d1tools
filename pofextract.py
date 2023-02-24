#!/usr/bin/env python3
# Written 2022 by Josh Cogliati
# This program is licensed under the terms of the GPL, version 2 or later

#polyobj read_model_file is very useful for understanding pof files.
#similar/3d/interp.cpp is also useful
#common/include/maths.h
#common/include/vecmat.h

import sys,os, enum
import struct
import xml.etree.ElementTree as ET
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

def float_vec(v):
    return [x/2**16 for x in v]

def interp_IDTA(data, obj_elem):
    def get_short(data, index):
        return struct.unpack('<H', data[index:index+2])[0]
    def get_uint(data, index):
        return struct.unpack('<I', data[index:index+4])[0]
    def get_int(data, index):
        return struct.unpack('<i', data[index:index+4])[0]
    def get_vec(data, index):
        return struct.unpack('<3i', data[index:index+12])
    data_index = 0
    op = get_short(data, data_index)
    while data_index < len(data): #op != Op.EOF:
        op_num = get_short(data, data_index)
        op = Op(op_num)
        print(op)
        op_elem = ET.SubElement(obj_elem, str(op)[3:])
        if op == Op.DEFPOINTS:
            n = get_short(data, data_index + 2)
            record_size = n * (3*4) + 4 + 4
            print(n, record_size)
            op_elem.attrib["n"] = str(n)
            def_points = []
            for i in range(n):
                def_points.append(get_vec(data, data_index + 4 + i*12))
                def_point_elem = ET.SubElement(op_elem, "point")
                def_point_elem.text = str(def_points[-1])
            print(def_points)
        elif op == Op.DEFP_START:
            n = get_short(data, data_index + 2)
            record_size = n * (3*4) + 4 + 4
            print(n, record_size)
            op_elem.attrib["n"] = str(n)
            def_points = []
            for i in range(n):
                def_points.append(get_vec(data, data_index + 4 + i*12))
                def_point_elem = ET.SubElement(op_elem, "point")
                def_point_elem.text = str(def_points[-1])
            print(def_points)
        elif op == Op.FLATPOLY:
            n = get_short(data, data_index + 2)
            record_size = 30 + ((n & ~1) + 1) * 2
            print(n, record_size)
            op_elem.attrib["n"] = str(n)
            vec1 = get_vec(data, data_index + 4)
            vec2 = get_vec(data, data_index + 16)
            vec1_elem = ET.SubElement(op_elem, "vec1")
            vec1_elem.text = str(vec1)
            vec2_elem = ET.SubElement(op_elem, "vec2")
            vec2_elem.text = str(vec2)
            print(vec1, vec2)
            short1 = get_short(data, data_index + 28)
            print(short1)
            op_elem.attrib["short"] = str(short1)
            flat_shorts = []
            for i in range(n):
                flat_shorts.append(get_short(data, data_index + 30 + i * 2))
                f_short_elem = ET.SubElement(op_elem, "short")
                f_short_elem.text = str(flat_shorts[-1])
            print(flat_shorts)
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
            print(get_vec(data, data_index + 4),get_vec(data, data_index + 16))
            print(get_short(data, data_index + 28), get_short(data, data_index + 30))
        elif op == Op.RODBM:
            record_size = 36
            print(get_vec(data, data_index + 4),get_vec(data, data_index + 20))
            print(get_short(data, data_index + 2))
            print(get_int(data, data_index + 16),get_int(data, data_index + 32))
        elif op == Op.SUBCALL:
            record_size = 20
            print(get_short(data, data_index + 2))
            print(get_vec(data, data_index + 4))
            print(get_short(data, data_index + 16))
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
    print(sys.argv[0]," file.pof [dump.xml]")
    sys.exit(-1)

if len(sys.argv) > 2:
    xml_dump_filename = sys.argv[2]
else:
    xml_dump_filename = None

f = open(sys.argv[1],"rb")

root = ET.Element('pof')
head, version = read_unpack("<4sH", f)
print(head, version)
if head != b"PSPO":
    print("not a pof file")
    sys.exit(-2)
root.attrib['head'] = head.decode()
root.attrib['version'] = str(version)

def read_vecs(num, file):
    vecs = []
    for i in range(num):
        vecs.append(read_unpack("<3i", file))
    return vecs

while True:
    try:
        kind, length = read_unpack("<4sI", f)
        print("kind", kind, length)
    except struct.error:
        break
    obj_elem = ET.SubElement(root, 'object')
    obj_elem.attrib['kind'] = kind.decode()
    if kind == b'TXTR':
        num_str = read_unpack("<H", f)[0]
        data = f.read(length - 2)
        textures = data.split(b'\x00')[:num_str]
        print("textures", textures)
        for texture in textures:
            texture_elem = ET.SubElement(obj_elem, "texture")
            texture_elem.text = texture.decode()
    elif kind == b'OHDR':
        n_models, rad = read_unpack("<II", f)
        pmmin = read_vecs(1, f)
        pmmax = read_vecs(1, f)
        print("object header", n_models, rad, pmmin, pmmax)
        obj_elem.attrib.update({"n_models": str(n_models), "rad": str(rad), "pmmin": str(pmmin), "pmmax": str(pmmax)})
    elif kind == b'SOBJ':
        n, submodule_parents = read_unpack("<HH", f)
        norms = read_vecs(1, f)
        pnts = read_vecs(1, f)
        offsets = read_vecs(1, f)
        rads, ptrs = read_unpack("<II", f)
        print(n, submodule_parents, norms, pnts, offsets, rads, ptrs)
        obj_elem.attrib.update({"n": str(n),"submodule_parents": str(submodule_parents), "rads": str(rads), "ptrs": str(ptrs)})
        norms_elem = ET.SubElement(obj_elem, "norms")
        norms_elem.text = str(norms[0])
        pnts_elem = ET.SubElement(obj_elem, "pnts")
        pnts_elem.text = str(pnts[0])
        offsets_elem = ET.SubElement(obj_elem, "offsets")
        offsets_elem.text = str(offsets[0])
    elif kind == b'GUNS':
        n_guns = read_unpack("<I", f)[0]
        print('n_guns', n_guns)
        obj_elem.attrib['n_guns'] = str(n_guns)
        for ni in range(n_guns):
            gun_elem = ET.SubElement(obj_elem, "gun")
            gun_id, submodel = read_unpack("<HH", f)
            gun_elem.attrib.update({"gun_id":str(gun_id), "submodel": str(submodel)})
            gun_points = read_vecs(1, f)
            points_elem = ET.SubElement(gun_elem, "gun_points")
            points_elem.text = str(gun_points[0])
            print(ni, gun_id, submodel, gun_points)
            if version >= 7:
                gun_dir = read_vecs(1, f)
                print(gun_dir)
                gun_dir_elem = ET.SubElement(gun_elem, "gun_dir")
                gun_dir_elem.text = str(gun_dir[0])
    elif kind == b'ANIM':
        n_frames = read_unpack("<H",f)[0]
        obj_elem.attrib["n_frames"] = str(n_frames)
        for model in range(0, n_models):
            for frame in range(0, n_frames):
                angles = read_unpack("<HHH", f)
                print("angles", model, frame, angles)
                anim_elem = ET.SubElement(obj_elem, "angles")
                anim_elem.attrib.update({"model": str(model), "frame": str(frame), "angles": str(angles)})
    elif kind == b'IDTA':
        data = f.read(length)
        print(kind, length, data[:60])
        interp_IDTA(data, obj_elem)
    else:
        data = f.read(length)
        print(kind, length, data[:60])

if xml_dump_filename is not None:
    tree = ET.ElementTree(root)
    ET.indent(tree)
    tree.write(open(xml_dump_filename,"wb"))
