all: txt2txb txb2txt hogextract hogcreate

txt2txb : txt2txb.o

txb2txt : txb2txt.o

hogextract : hogextract.o

hogcreate : hogcreate.o

new_hog/descent.txb : txt2txb nd.txt
	./txt2txb nd.txt new_hog/descent.txb
