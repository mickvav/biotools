#!/usr/bin/env python3
#
# This scrit summarizes some metadata, obtained from GenBank from
# protein database on multiple organisms using Batch Entrez
# http://www.ncbi.nlm.nih.gov/sites/batchentrez
# in GenPept (full) format.
# Accepts list of files as arguments or reads from stdin.
# Prints output in tab-delimited text for future analisis.
#
# This is a free software, distributed under terms of GPL v3
#
# Copyright (c) Mihail Vasiliev, 2014
#
import fileinput
import re
parsingfeatures=0
parsingsource=0
colnames={}
locusname=""
source=""
accession=""
locusheader=[]
data=[]
colvalues = {}
refid=0
colnames["LOCUS"]=1
colnames["LOCUS1"]=1
colnames["LOCUS2"]=1
colnames["LOCUS3"]=1
colnames["SOURCE"]=1
colnames["ACCESSION"]=1
for line in fileinput.input():
    field=line[0:11]
    
    if (field != "           ") and (parsingsource == 1) :
        parsingsource=0
        parsingfeatures=0
        colvalues["LOCUS"]=locusname
        colvalues["LOCUS1"]=locusheader[1]
        colvalues["LOCUS2"]=locusheader[2]
        colvalues["LOCUS3"]=locusheader[3]
        colvalues["SOURCE"]=source
        colvalues["ACCESSION"]=accession
        source=""
        accession=""
        data.append(colvalues)
        colvalues = {}
        
    if parsingsource==1:
        sourcedata=re.split('="',line[22:-2])
        if(len(sourcedata)==2):
            if(line[-2:-1] != '"'):
                reading=sourcedata[0]
                readingpos=22
                readinglast=-2
            colnames[sourcedata[0]]=1
            colvalues[sourcedata[0]]=sourcedata[1]

    if field == "LOCUS      " :
        locusheader = re.split("\s+",line[12:])
        locusname=locusheader[0]
    elif field == "SOURCE     " :
        source = line[12:-1]
    elif field == "ACCESSION  " :
        accession = line[12:]
    elif field == "FEATURES   " :
        parsingfeatures=1        
    elif field == "     source" :
        source = line[21:]
        parsingsource=1
    elif field == "REFERENCE  " :
        refid = line[12:-1]
        refno = re.findall("\d+",refid)[0]
    elif field == "  AUTHORS  " :
        reading="REF_"+refno+"AUTHORS"
        readingpos=12
        readinglast=-1
        colvalues[reading] = line[12:]
        colnames[reading] = 1
    elif field == "  TITLE    " :
        reading="REF_"+refno+"_TITLE"
        readingpos=12
        readinglast=-1
        colvalues[reading] = line[12:]
        colnames[reading] = 1
    elif field == "  JOURNAL  " :
        reading="REF_"+refno+"_JOURNAL"
        readingpos=12
        readinglast=-1
        colvalues[reading] = line[12:]
        colnames[reading] = 1
    elif field == "           " :
        if(reading != "") :
            colvalues[reading] = colvalues[reading] + " " + line[readingpos:readinglast]
    elif field != "           " :
        reading=""
        
    
cnl=sorted(colnames.keys())

print(str.join("\t",cnl))
    
for cv in data:
    for colname in cnl:
        if colname in cv.keys():
            print(re.sub("\n","",cv[colname]),end="\t")
        else:
            print("-\t",end='')
    print("")
