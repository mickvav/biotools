#!/usr/bin/python
import sys
import optparse
import os
import re

if len(sys.argv) == 1:
    print "python join_rebase_alien.py -h for help"
    exit()

parser = optparse.OptionParser()
parser.add_option("-i", "--in_dir", help="Directory with files output by parse_alien_tab.py", dest="in_dir")
parser.add_option("-r", "--rebase_rm_file", help="file of rm systems as outputed by get_rm_genes_mick.py", dest="rm_file")
parser.add_option("-s", "--rebase_RE_dna_file", help="sums_edited.csv", dest="ri_file")
parser.add_option("-d", "--table_S5", help="file of Table_S5 from article", dest="s_file")

options, args = parser.parse_args()
vars().update(vars(options))

idx={}
if in_dir==None:
    print "No in_dir was specified"
    exit()
else:
    if(not(os.path.isfile(in_dir+"/out.index"))):
        print "Indexing directory "+in_dir
        os.system("python index_out_files.py "+in_dir)
    f=open(in_dir+"/out.index")
    for l in f.readlines():
        e=l.rstrip("\n").split("\t")
        idx[e[0]]=e[1]
    f.close() 
        
ris=open(ri_file)
#
# REBASE genome ID,Sequence AC,R-M system type,REBASE name,Gene type,Recognition site,ORF number,Locus,GI,UniProt AC,Protein ID,Gene length,Protein length,Note
# 1,CR543861,Type I,AspADPORF3432P,R,-,3430,ACIAD3430,49532374,Q6F779,CAG70086.1,3063,1020,Hha21639ORF1774P (63% identity); putative;
s_lines=ris.readlines()
gsf={}
for line in s_lines:
    a=line.split(",")
    gsf[a[3]]=a[1]
#
#"Table S5. List of all actual {site, genome} pairs. Sites of experimentaly studied restriction endonucleases (REBASE Gold Standard) are marked ""yes"" in corresponding column.",,,,,,,,,,last update 04.03.15,
#GenBank,Site,Complementary site,Genome type,RE types,RE names (REBASE),Ke,Ke for complementary,Kr,Kr for complementary,REBASE Gold Standard,Methylomes
#AE000511.1,ACANNNNNNNNTAG,CTANNNNNNNNTGT,Bacteria,Type I,HpyAXIIIP,161.29,191.51,0.88,0.98,No,Yes
#
sf={}
if s_file==None :
    s=open(ri_file)
    s_lines=s.readlines()
    for line in s_lines:
        a=line.rstrip("\n").split(",")
        sf[a[3]]=a[1]
    s.close();
else:
    s=open(s_file)
    s_lines=s.readlines()
    for line in s_lines:
        a=line.rstrip("\n").split(',')
        if a[5] in gsf:
            if a[0].rfind(gsf[a[5]])==0: 
                sf[a[5]]=a[0]
        else:
            sf[a[5]]=a[0]
    s.close();
    
r=open(rm_file)
of=open(rm_file+".out.full",'w')
al={}
r.readline()
r_lines=r.readlines()
iii=0
data={}
for line in r_lines:
    iii=iii+1
    a=line.split("\t")
    enz_id=a[2]
    enz_loc=a[5].split("-")
    enz_start=int(enz_loc[0])
    enz_end=int(enz_loc[1])
    print "Working with enz_id:"+enz_id
    if enz_id in sf:
        if(not(sf[enz_id] in al)):
            if sf[enz_id] in idx:
                fname=idx[sf[enz_id]]
            else: 
                fname=in_dir+"/"+sf[enz_id]+".fasta.out"
            if(not(os.path.isfile(fname))) :
                gn=1
                for n in range(1,10):
                    fname=in_dir+"/"+sf[enz_id]+"."+str(n)+".fasta.out"
                    if(os.path.isfile(fname)):
                        gn=n
                fname=in_dir+"/"+sf[enz_id]+"."+str(gn)+".fasta.out"
            fname_parsed=fname+".parsed"
            if(not(os.path.isfile(fname_parsed))):
                if(os.path.isfile(fname)):
                    os.system("python parse_alien_tab.py -i "+fname+" >"+fname_parsed)
                else:
                    of.write(line.rstrip("\n")+"\t"+fname+" not found\n")
                    data[enz_id]=line.rstrip("\n")+"\t"+fname+" not found\n"
                    continue
            f=open(fname_parsed)
            f_lines=f.readlines()
            f.close()
            al[sf[enz_id]]={}
            for fline in f_lines:
                aaa=fline.split("\t");
                al[sf[enz_id]][aaa[1]]={}
                al[sf[enz_id]][aaa[1]]['end']=aaa[2]
                al[sf[enz_id]][aaa[1]]['thresh']=aaa[3]
                al[sf[enz_id]][aaa[1]]['score']=aaa[4]
        washit=0
        for start in al[sf[enz_id]].iterkeys():
            iend=int(al[sf[enz_id]][start]['end'])
            istart=int(start)
            thresh=al[sf[enz_id]][start]['thresh']
            score=al[sf[enz_id]][start]['score']
            hit=0
            if((istart<=enz_start)and(istart<=enz_end)and(iend>=enz_start)and(iend>=enz_end)):
                hit=3
            elif ((istart<=enz_start)and(iend>=enz_start)):
                hit=2
            elif ((istart<=enz_end) and (iend>=enz_end)):
                hit=1
            if(hit>0):
                washit=1
                of.write(line.rstrip("\n")+"\t"+str(hit)+"\t"+start+"\t"+str(iend)+"\t"+thresh+"\t"+score+"\n")
                data[enz_id]=line.rstrip("\n")+"\t"+str(hit)+"\t"+start+"\t"+str(iend)+"\t"+thresh+"\t"+score+"\n"
        if(washit==0):
                of.write(line.rstrip("\n")+"\t0\t\t\t\t\n")
                data[enz_id]=line.rstrip("\n")+"\t0\t\t\t\t\n"
    else:
        print "Not found in sf:"+enz_id 
 

of.close()


if s_file==None:
    of=open(rm_file+".sonly.out",'w')
    s=open(ri_file)
    s_lines=s.readlines()
    for line in s_lines:
        a=line.rstrip("\n").split(',')
        enz_id=a[3]
        orig_id=gsf[enz_id]
        if enz_id in data:
            of.write("\t".join(a)+"\t"+orig_id+"\t"+data[enz_id])
        else:
            of.write("\t".join(a)+"\t"+orig_id+"\tNo data found.\n")
    of.close()    
else:
    of=open(rm_file+".out",'w')
    s=open(s_file)
    s_lines=s.readlines()
    for line in s_lines:
        a=line.rstrip("\n").split(',')
        enz_id=a[5]
        orig_id=""
        if enz_id in gsf:
            orig_id=gsf[enz_id]
        if enz_id in data:
            of.write("\t".join(a)+"\t"+orig_id+"\t"+data[enz_id])
        else:
            of.write("\t".join(a)+"\t"+orig_id+"\tNo data found.\n")
    of.close()
