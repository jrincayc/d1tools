
import sys, os
import struct

def read_unpack(format, file):
    size =struct.calcsize(format)
    data = file.read(size)
    return struct.unpack(format, data)
