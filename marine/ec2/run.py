#!/usr/bin/env python3

from sys import argv
from os import system, fork
from os.path import basename, exists
from typing import Dict, List
from collections import defaultdict
import re

bowtie2="/home/ubuntu/bowtie2-2.4.1-linux-x86_64/bowtie2"
stop_flag="/home/ubuntu/stop"

def read_erserr(filename) -> Dict[str, List[str]]:
    result = defaultdict(list)
    with open(filename,"r") as r:
        for line in r:
            (ers,tara,err) = line.strip().split("\t")
            result[ers].append(err)
    return result

# ~/bowtie2-2.4.1-linux-x86_64/bowtie2 --met-file found-errs/ERS491740/ERR315859.met -x ERS491740.reference.contig -1 found-errs/ERS491740/ERR599079_1.fastq.gz -2 found-errs/ERS491740/ERR599079_2.fastq.gz -S ERS491740.all.ERR599079.sam
def process_pair(file1, file2, err, ers):
    metfile=f"found-errs/{ers}/{err}.met"
    if exists(f"{ers}.all.{err}.sam"):
        print(f"{ers}.all.{err}.sam already exists. skipping")
        return
    system(f"touch {ers}.all.{err}.sam")
    system(f"cp {ers}.reference.contig* /dev/shm/")
    system(f"{bowtie2} --no-unal --threads 1 -x /dev/shm/{ers}.reference.contig -1 {file1} -2 {file2} -S /home/ubuntu/{ers}.all.{err}.sam")
    system(f"rm /dev/shm/{ers}.reference.contig*")
    system(f"samtools view -b -o {ers}.all.{err}.bam /home/ubuntu/{ers}.all.{err}.sam")
    system(f"rm /home/ubuntu/{ers}.all.{err}.sam")


ers_err = read_erserr(argv[1])
for ers in ers_err:
    for err in ers_err[ers]:
        if exists(stop_flag):
            print(f"Stop flag found. Exiting. Remove {stop_flag} before next run.")
            raise RuntimeError("Stop")
        file1=f"found-errs/{ers}/{err}_1.fastq.gz"
        file2=f"found-errs/{ers}/{err}_2.fastq.gz"
        if exists(file1) and exists(file2):
            print(f"Processing {file1} {file2}")
            process_pair(file1, file2, err, ers)

