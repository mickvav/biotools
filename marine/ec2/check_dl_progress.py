#!/usr/bin/env python3

import subprocess
import re
from os import stat, readlink
from time import sleep
from sys import argv
if len(argv) > 1:
    interval=float(argv[1])
else:
    interval=5
def wget_pid_progress(pid):
    stat1 = stat(f"/proc/{pid}/fd/5")
    return stat1[6]

lines = subprocess.check_output('ps -A | grep wget', shell=True, universal_newlines=True)
state = {}
for line in lines.split("\n"):
    try:
        (pid, pts, time, name) = re.split("\s+",line.strip())
        s = wget_pid_progress(pid)
        print(pid, pts, s, readlink(f"/proc/{pid}/fd/5"))
        state[pid] = s
    except Exception as ee:
        pass

sleep(interval)
perf = 0
for line in lines.split("\n"):
    try:
        (pid, pts, time, name) = re.split("\s+",line.strip())
        s = wget_pid_progress(pid)
        print(pid, (s-state[pid])/interval)
        perf += (s-state[pid])/interval
    except Exception as ee:
        pass
print(f"Total download performance: {perf} bytes/s")
