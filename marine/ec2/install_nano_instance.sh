#!/bin/bash

wget https://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.4.1/bowtie2-2.4.1-linux-x86_64.zip/download
sudo apt-get update 
sudo apt-get -y install build-essential unzip
mv download bowtie2.zip
unzip bowtie2.zip 

wget https://github.com/samtools/samtools/releases/download/1.10/samtools-1.10.tar.bz2
tar -xvjf samtools-1.10.tar.bz2 
sudo apt-get -y install ncurses-dev zlib1g-dev libbz2-dev liblzma-dev libcurl4-openssl-dev libssl-dev
cd samtools-1.10/
./configure --prefix=/usr/local
make && sudo make install
cd ..

