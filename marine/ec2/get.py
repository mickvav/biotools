#!/usr/bin/env python3

from sys import argv
from os import system, fork
from os.path import basename, exists
import re

with open(argv[1],"r") as f:
    for line in f.readlines():
        if exists("/home/ubuntu/stop.get"):
            raise RuntimeError("remove /home/ubuntu/stop.get")
        if exists(basename(line.strip())):
            print(f"File {line.strip()} exists. Skip download")
        else:
            system(f"wget ftp://{line.strip()}")
