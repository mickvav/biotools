#!/bin/bash
 blastp -query data/animal.sequences.fasta -db CP009243.1 -outfmt "7 qseqid sseqid evalue bitscore" > animal.blast.CP009243.1

