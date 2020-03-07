#!/bin/bash

wget https://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.4.1/bowtie2-2.4.1-linux-x86_64.zip/download
sudo apt-get update ; sudo apt-get install build-essential
sudo apt install unzip
mv download bowtie2.zip
unzip bowtie2.zip 

wget https://github.com/samtools/samtools/releases/download/1.10/samtools-1.10.tar.bz2
tar -xvjf samtools-1.10.tar.bz2 
sudo apt-get install ncurses-dev
udo apt-get install zlib1g-dev
udo apt-get install libbz2-dev
sudo apt-get install liblzma-dev
sudo apt-get install libcurl4-openssl-dev
sudo apt-get install libssl-dev
cd samtools-1.10/
./configure --prefix=/usr/local
make && sudo make install
cd ..

