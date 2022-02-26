all: txt2txb txb2txt hogextract hogcreate

txt2txb : txt2txb.o

txb2txt : txb2txt.o

hogextract : hogextract.o

hogcreate : hogcreate.o

new_hog/descent.txb : txt2txb base_files/nd.txt
	./txt2txb base_files/nd.txt new_hog/descent.txb

new_hog/palette.256 : base_files/palette.txt palcreate.py
	./palcreate.py base_files/palette.txt new_hog/palette.256

base_files/palette.txt : palgen.py
	./palgen.py > base_files/palette.txt

#This causes crashes because the font is too big
#new_hog/font1-1.fnt : x11_pd_fonts/10x20.png fontgen.py
#	(mkdir x11_pd_fonts/10x20 && cd x11_pd_fonts/10x20 &&  ../../fontgen.py ../10x20.png 15 144 25 10 29 20 && ../../fontcreate.py ../../new_hog/font1-1.fnt )

new_hog/font3-1.fnt : x11_pd_fonts/5x7.png
	(mkdir x11_pd_fonts/5x7 && cd x11_pd_fonts/5x7 &&  ../../fontgen.py ../5x7.png 17 144 24 5 16 7  && ../../fontcreate.py ../../new_hog/font3-1.fnt )

new_hog/font2-1.fnt : new_hog/font1-1.fnt
	cp $< $@

new_hog/font2-2.fnt : new_hog/font1-1.fnt
	cp $< $@

new_hog/font2-3.fnt : new_hog/font1-1.fnt
	cp $< $@

new_hog/font1-1.fnt : new_hog/font3-1.fnt
	cp $< $@

descent.hog : hogcreate new_hog/font3-1.fnt new_hog/font2-1.fnt new_hog/font2-2.fnt new_hog/font2-3.fnt new_hog/font1-1.fnt new_hog/palette.256 new_hog/descent.txb
	(cd new_hog && ../hogcreate ../descent.hog)
