#!/usr/bin/env python3
# Written 2022 by Josh Cogliati
# This program is licensed under the terms of the GPL, version 2 or later

import sys,os
import glob
import struct
import PIL
import PIL.Image


def write_pack(format, file, data):
    pack = struct.pack(format, *data)
    file.write(pack)

if len(sys.argv) < 2:
    print(sys.argv[0], " pigfile")
    print("creates a pigfile from *.png and *.snd files in current directory")
    sys.exit(-1)

f = open(sys.argv[1], "wb")

image_files = glob.glob("*.png")
sound_files = glob.glob("*.snd")

images = []
for image_filename in image_files:
    image = PIL.Image.open(image_filename)
    images.append((image_filename, image))


f.write(b"PIG0") #Custom header
write_pack("<II", f, (len(image_files), len(sound_files)))

offset = struct.calcsize("<II") + struct.calcsize("<8sBBBBBI")*len(image_files) + struct.calcsize("<8sIII")*len(sound_files)

for image_filename, image in images:
    width, height = image.size
    write_pack("<8sBBBBBI", f, ((image_filename[:-4][:8]).encode(),
                                0, width, height, 0, 0, offset))
    offset += width*height

#xxx write sound file headers

for image_filename, image in images:
    width, height = image.size
    for x in range(width):
        for y in range(height):
            write_pack("B", f, (image.getpixel((x,y)),))
