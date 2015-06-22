#!/usr/bin/python
import sys
import optparse
import os
import os.path
import re
import glob


if len(sys.argv) == 1:
    print "python index_out_files.py -h for help"
    exit()

parser = optparse.OptionParser()
parser.add_option("-d", "--directory", help="Directory with .out files from alien_hunter to be indexed", dest="in_dir")

options, args = parser.parse_args()
vars().update(vars(options))

if in_dir==None:
    print "No directory was specified"
    exit()

if not(os.path.isdir(in_dir)):
    print "Need a directory!"
    exit()

idx = {}
for fname in glob.glob(in_dir+"/*.out"):
    f=open(fname)
    lines=f.readlines()
    for line in lines:
        m=re.match(r'FT                   /contig_(start|end)="(.*)"',line)
        if m:
            l1=m.group(2)
            elems=l1.split('|')
            if(len(elems)>=4):
                sp1=elems[3].split('.')
                idx[sp1[0]]=fname
            else:
                print "Warning! Problems parsing file: "+fname
                print "Line: "+line
                print "To few elems in:" + l1

    f.close()

f=open(in_dir+"/out.index","w")
for k in idx.keys():
    f.write(k+"\t"+idx[k]+"\n")

