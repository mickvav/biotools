#!/usr/bin/python
## U13369.1	SRR1535830.1075026	+	-	0	30
## U13369.1	SRR1535830.1185702	+	-	0	67

import sys
## 
f=open(sys.argv[1],'r')
g=open(sys.argv[2],'w')
g.write("chr"+"\t"+"pos"+"\t"+"#all reads on direct chain"+"\t"+"#all reads on reverse chain"+"\t"+"#all reads, which starts in the position"+"\t"+"#total number of reads in the position"+"\n")
ops={}
dops={}
ops['+-']={}
ops['-+']={}
dops['+-']={}
dops['-+']={}
evs={}
evs['+-']={}
evs['-+']={}
evs['']={}
for line in f:
    line=line.strip().split()
    pair_id=line[1]
    chr_id=line[0]
    ori=line[2]+line[3]
    if not chr_id in evs['']:
        for o in ['+-','-+']:
            ops[o][chr_id]={}
            dops[o][chr_id]={}
            evs[o][chr_id]={}
            evs[o][chr_id]={}
            evs[''][chr_id]={}
    start=int(line[4])
    stop=int(line[5])
    if stop<start:
        print "oops: pair_id="+pair_id+" stop<start: "+str(stop)+" < "+str(start)
    if not start in ops[ori][chr_id]:
        ops[ori][chr_id][start]=1
    else:
        ops[ori][chr_id][start]+=1
    if not stop in dops[ori][chr_id]: 
        dops[ori][chr_id][stop]=1
    else:
        dops[ori][chr_id][stop]+=1
    evs[ori][chr_id][start]=1
    evs[ori][chr_id][stop]=1 
    evs[''][chr_id][start]=1
    evs[''][chr_id][stop]=1
 
for c in evs[''].keys():
    v={}
    v['+-']=0
    v['-+']=0
    minev=min(evs[''][c])
    maxev=max(evs[''][c])
    for ev in range(minev,maxev+1):
        starts=0
        if ev in ops['+-'][c]:
            v['+-']+=ops['+-'][c][ev]
            starts+=ops['+-'][c][ev]
        if ev in dops['-+'][c]:
            starts+=dops['-+'][c][ev]
        if ev in ops['-+'][c]:
            v['-+']+=ops['-+'][c][ev]
        vs=v['-+']+v['+-']
        if(starts>vs):
            print "ghm: c:"+c+" ev:"+str(ev)+" starts>vs "+str(starts)+">"+str(vs)
        g.write(c+"\t"+str(ev)+"\t"+str(v['+-'])+"\t"+str(v['-+'])+"\t"+str(starts)+"\t"+str(vs)+"\n")
        if ev in dops['+-'][c]:
            v['+-']-=dops['+-'][c][ev]
        if ev in dops['-+'][c]:
            v['-+']-=dops['-+'][c][ev]

