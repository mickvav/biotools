#!/bin/bash
for i in *.reference.contig.fasta; do 
    ers=${i%%.reference.contig.fasta}
    mkdir found-errs/$ers
    errs=`grep $ers ~/err-ers | awk '{print $3;}'`
    for j in $errs; do 
	for f in /mnt/data/tara_ocean/$j*; do 
	     if [ -f $f ]; then
    	         ln -s $f found-errs/$ers/; 
	     fi
        done
    done
done
