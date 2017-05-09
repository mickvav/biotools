#!/usr/bin/python

import sys
f=open(sys.argv[1],'r')
start={}
stop={}
ori={}
chrom={}
pair_list={}
left={}
start_f={}
stop_f={}
r1_start={}
num_start={}
num_total={}

for line in f:
    line=line.strip().split()
    read_id=line[3].split('/')[0]
    pair_id=read_id.split('.')[0]+'.'+read_id.split('.')[1]
    read_num=int(read_id.split('.')[2])
    if not pair_id in pair_list:
        pair_list[pair_id]=0
    pair_list[pair_id]+=1
    if not pair_id in start:
        start[pair_id]={}
    start[pair_id][read_num]=int(line[1])
    if not pair_id in stop:
        stop[pair_id]={}
    stop[pair_id][read_num]=int(line[2])
    if not pair_id in chrom:
        chrom[pair_id]={}
    chrom[pair_id][read_num]=line[0]
    if not pair_id in ori:
        ori[pair_id]={}
    ori[pair_id][read_num]=line[5]
    if pair_list[pair_id]==2:
        start_f=min(start[pair_id][1],start[pair_id][2])
        stop_f=max(stop[pair_id][1],stop[pair_id][2])
        print chrom[pair_id][read_num]+"\t"+pair_id+"\t"+ori[pair_id][1]+"\t"+ori[pair_id][2]+"\t"+str(start_f)+"\t"+str(stop_f)
        del pair_list[pair_id]
        del start[pair_id]
        del stop[pair_id]
        del chrom[pair_id]
        del ori[pair_id]

f.close()
 
