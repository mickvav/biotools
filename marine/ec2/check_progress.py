#!/usr/bin/env python3

import subprocess
import re
from os import stat, readlink
from time import sleep
from sys import argv
if len(argv)>1:
    interval=float(argv[1])
else:
    interval=5
def bowtie_pid_progress(pid):
    stat1 = stat(f"/proc/{pid}/fd/3")
    stat2 = stat(f"/proc/{pid}/fd/4")
    with open(f"/proc/{pid}/fdinfo/3") as f:
        line = f.readline()
        pos1=int(line[5:].strip())
    with open(f"/proc/{pid}/fdinfo/4") as f:
        line = f.readline()
        pos2=int(line[5:].strip())
    return (stat1[6], stat2[6], pos1, pos2)

lines = subprocess.check_output('ps -A | grep bowtie2-align-s', shell=True, universal_newlines=True)
state = {}
for line in lines.split("\n"):
    try:
        (pid, pts, time, name) = re.split("\s+",line.strip())
        (s1,s2,p1,p2) = bowtie_pid_progress(pid)
        print(pid, pts, 50*(p1/s1+p2/s2), readlink(f"/proc/{pid}/fd/3"))
        state[pid] = p1 + p2
    except Exception as ee:
        pass

sleep(interval)
perf = 0
print("Pid BPS     ETA[s]")
for line in lines.split("\n"):
    try:
        (pid, pts, time, name) = re.split("\s+",line.strip())
        (s1,s2,p1,p2) = bowtie_pid_progress(pid)
        pr= p1+p2
        eta = (s1 + s2 - p1 - p2) * interval / (pr-state[pid])
        print(pid, (pr-state[pid])/interval, eta )
        perf += (pr-state[pid])/interval
    except Exception as ee:
        pass
print(f"Total performance: {perf} bytes/s")
