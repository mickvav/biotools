#!/usr/bin/env python3

from sys import argv
from os import system, fork
from os.path import basename, exists
from typing import Dict, List
from collections import defaultdict
import re

stop_flag="/home/ubuntu/stop-coverage"

def read_erserr(filename) -> Dict[str, List[str]]:
    result = defaultdict(list)
    with open(filename,"r") as r:
        for line in r:
            (ers,tara,err) = line.strip().split("\t")
            result[ers].append(err)
    return result

# ~/bowtie2-2.4.1-linux-x86_64/bowtie2 --met-file found-errs/ERS491740/ERR315859.met -x ERS491740.reference.contig -1 found-errs/ERS491740/ERR599079_1.fastq.gz -2 found-errs/ERS491740/ERR599079_2.fastq.gz -S ERS491740.all.ERR599079.sam
def process(filename):
    sorted_file = f"{filename}.sorted.bam"
    if exists(f"sorted/{sorted_file}"):
        return
    system(f"touch sorted/{sorted_file}")
    system(f"samtools sort -o /home/ubuntu/{sorted_file} -O BAM -m 1G --threads 2 {filename}")
    system(f"samtools coverage /home/ubuntu/{sorted_file} -o /home/ubuntu/{filename}.coverage")
    system(f"mv -f /home/ubuntu/{sorted_file} sorted/{sorted_file}")
    system(f"mv -f /home/ubuntu/{filename}.coverage coverage/{filename}.coverage")


for filename in argv[1:]:
    if exists(stop_flag):
        raise RuntimeError(f"Remove {stop_flag} before next run")
    print("Processing {filename}")
    process(filename)

