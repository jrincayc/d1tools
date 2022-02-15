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

