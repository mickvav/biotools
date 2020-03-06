#!/usr/bin/env python3

from sys import argv
from os import system, fork
from os.path import basename, exists
import re

bowtie2="bowtie2-2.4.1-linux-x86_64/bowtie2"
metfile="--------"

system(f"{bowtie2}-build ERS477998.def.con.fasta ERS477998.def.con")



def process_pair(url1, url2):
    newpid = fork()
    if newpid == 0:
        # child
        fname1=basename(url1)
        fname2=basename(url2)
        dirname=fname1[:-11]
        print(f"I am child, processing 2 files: {fname1} {fname2}")
        print(f"Creating directory {dirname}")
        system(f"mkdir {dirname}")
        system(f"mv {fname1} {dirname}")
        system(f"mv {fname2} {dirname}")
        system(f"bowtie2 --align-paired-reads --met-file {metfile} --threads 1 -x ERS477998.def.con -1 {dirname}/{fname1} -2 {dirname}/{fname2} -b ERS477998.def.{dirname}.bam")
        system(f"samtools sort ERS477998.def.{dirname}.bam -o ERS477998.def.{dirname}.sorted.bam > samtools_sort_out_{dirname}")
        system(f"samtools coverage samtools_sort_out_{dirname} > samtools_coverage_{dirname}_smt.cov")


def process_single(url):
    newpid = fork()
    if newpid == 0:
        # child
        fname=basename(url)
        dirname=fname[:-9]
        print(f"I am child, processing 1 file: {fname}")
        print(f"Creating directory {dirname}")
        system(f"mkdir {dirname}")
        system(f"mv {fname} {dirname}")
        system(f"bowtie2 --align-paired-reads --met-file {metfile} --threads 1 -x ERS477998.def.con -U {dirname}/{fname1} -b ERS477998.def.{dirname}.bam")
        system(f"samtools sort ERS477998.def.{dirname}.bam -o ERS477998.def.{dirname}.sorted.bam > samtools_sort_out_{dirname}")
        system(f"samtools coverage samtools_sort_out_{dirname} > samtools_coverage_{dirname}_smt.cov")



with open(argv[1],"r") as f:
    is_pair = False
    first_file = ""
    for line in f.readlines():
        if exists(basename(line.strip())):
            print(f"File {line.strip()} exists. Skip download")
        else:
            system(f"wget {line.strip()}")
        if re.match(r".*_1.fastq.gz", line.strip()):
            is_pair=True
            first_file = line.strip()
            print(f"Using {first_file} as first file")
            continue
        if re.match(r".*_2.fastq.gz", line.strip()):
            process_pair(first_file, line.strip())
            continue
        process_single(line.strip())


