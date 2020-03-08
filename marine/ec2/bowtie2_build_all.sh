#!/bin/bash
for i in *.reference.contig.fasta; do 
   if [ ! -f ${i%%.fasta}.1.bt2 ]; then
     ~/bowtie2-2.4.1-linux-x86_64/bowtie2-build $i ${i%%.fasta}
   fi
done
