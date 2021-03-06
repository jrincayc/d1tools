/* Written 1999 Jan 29 by Josh Cogliati
   I grant this program to public domain.
*/
#include<stdio.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<fcntl.h>
#include<dirent.h>
#include<string.h>
#include<stdlib.h>

void main(int argc, char *argv[]){
  FILE * hogfile, * readfile;
  DIR * dp;
  struct dirent *ep;
  int fp, len, fseekret=0;
  char filename[13];
  char * buf;
  struct stat statbuf;
  if(argc != 2){
    printf("Usage: hogcreate hogfile\n"
	   "creates hogfile using all the files in the current directory\n"
	   );
    exit(0);
  }
  hogfile = fopen(argv[1],"w"); 
  buf = (char *)malloc(3);
  strncpy(buf,"DHF",3);
  fwrite(buf,3,1,hogfile);
  printf("Creating: %s\n",argv[1]);
  free(buf);
  dp = opendir("./");
  if (dp != NULL) {
    while (ep = readdir(dp)) {
      strcpy(filename, ep->d_name);
      stat(filename,&statbuf);
      if(! S_ISDIR(statbuf.st_mode)) {
	printf("Filename: %s \tLength: %i\n",filename,statbuf.st_size);
	readfile = fopen(filename,"r");
	buf = (char *)malloc(statbuf.st_size);
	if(buf == NULL) {
	  printf("Unable to allocate memery\n");
	} else {
	  fwrite(filename, 13,1,hogfile);
	  fwrite(&statbuf.st_size, sizeof(int),1,hogfile);
	  fread(buf,statbuf.st_size, 1 , readfile);
	  fwrite(buf,statbuf.st_size, 1 , hogfile);
	}
	fclose(readfile);

      }
    }
    closedir(dp);
  }
  fclose(hogfile);
}


