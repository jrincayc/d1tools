#!/usr/bin/env python3
# Written 2022 by Josh Cogliati
# This program is licensed under the terms of the GPL, version 2 or later

#This just generates a web-safe color palette and simple fade.
# An optimized palette and fade could be done much* better.
#
#* and by much better, I mean if you use this you will probably get an
# angry email from an artist trying to use this to actually produce
# cool graphics.

shades = [0x00, 0x33, 0x66, 0x99, 0xCC, 0xFF]

i = 0;
for r in shades:
    for g in shades:
        for b in shades:
            print(i,(r,g,b))
            i += 1
for i in range(i, 256):
    print(i,(i,i,i))

GR_FADE_LEVELS=34
k = 255//GR_FADE_LEVELS
for j in range(GR_FADE_LEVELS):
    for i in range(256):
        print(j,i,j*k)
