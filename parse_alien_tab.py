import sys
import optparse
import os
import re

if len(sys.argv) == 1:
    print "python parse_alien_tab.py -h for help"
    exit()

parser = optparse.OptionParser()
parser.add_option("-i", "--in_file", help="In_file in .out format of alien_hunter", dest="in_file")

options, args = parser.parse_args()
vars().update(vars(options))

if in_file==None:
    print "No In_file was specified"
    exit()

f=open(in_file)
lines=f.readlines()

feature=''
note=''
score=''
c_start=''
c_end=''
s_pos=''
e_pos=''

for line in lines:
    m=re.match(r'^FT   misc_feature    (\d+\.\.\d+)',line)
    if m:
	if (feature is not ''):
		print in_file+"\t"+re.sub(r'\.\.',"\t",feature)+"\t"+note+"\t"+score+"\t"+c_start+"\t"+c_end+"\t"+s_pos+"\t"+e_pos
	feature=m.group(1)
    m=re.match(r'FT                   /note="threshold: (\d+\.?\d*)',line)
    if m:
	note=m.group(1)
    m=re.match(r'FT                   /score=(\d+\.?\d*)',line)
    if m:
	score=m.group(1)
    m=re.match(r'FT                   /contig_start="(.*)"',line)
    if m:
        c_start=m.group(1)
    m=re.match(r'FT                   /contig_end="(.*)"',line)
    if m:
        c_end=m.group(1)
    m=re.match(r'FT                   /start_relative_position="(.*)"',line)
    if m:
        s_pos=m.group(1)
    m=re.match(r'FT                   /end_relative_position="(.*)"',line)
    if m:
        e_pos=m.group(1)




print in_file+"\t"+re.sub(r'\.\.',"\t",feature)+"\t"+note+"\t"+score+"\t"+c_start+"\t"+c_end+"\t"+s_pos+"\t"+e_pos
