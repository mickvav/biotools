import urllib2 
import doctest
import optparse
import sys
import os
from time import time
from TableParse import *


def read_and_check(genome_id, protocol):

    current_page=urllib2.urlopen(base_url + genome_id.strip().split()[0]).read() 

    #Check page
    if current_page.find("ERROR:")<>-1:
        missed_id = current_page[current_page.find("ERROR:")+6:].split("<")[0]
        os.system('echo " %s: %s " >>  %s' %  (genome_id.strip(), missed_id, protocol ))
        return None


    #Read page
    corrected_page=current_page.replace("<th","<td")
    corrected_page=corrected_page.replace("</th","</td")
    corrected_page=corrected_page.replace("<p","\n<table><tr><td")
    corrected_page=corrected_page.replace("</p>","</td></tr></table>")
    page_tables=parse(corrected_page)

    
    if len(page_tables)==10:
        organism=page_tables[1][1]
        os.system('echo " %s: %s has no RM systems " >> %s ' % (x.strip(), organism, protocol ))
        return None
    return page_tables


def find_ORF_titles(genome_id, page_tables, protocol):
    ORF_indexes=[]
    for ORF_index in range(len(page_tables)):
        if len(page_tables[ORF_index])==0:
            continue
        if page_tables[ORF_index][0]=='Type':
            ORF_indexes.append(ORF_index)
    if len(ORF_indexes)==0:
        os.system('echo " %s: Page has no title lines with word Type. Aborted." >> %s ' % (genome_id.strip(), protocol ))
        return None         
    return ORF_indexes

def find_head_table(genome_id,page_tables,protocol):
    start_index=3
    for index in range(start_index,len(page_tables)):
        if len(page_tables[index])==0:
            continue
        if page_tables[index][0].find("REBASE ref")<>-1:
            start_index=index
            break  
        continue
    if start_index==3:
        os.system('echo " %s: Page has no line with words REBASE ref. DNA list skipped." >> %s ' % (genome_id.strip(), protocol ))
        return None

    end_index=start_index
    for index in range(end_index+1,len(page_tables)):
        if len(page_tables[index])==0:
            continue
        if page_tables[index][0].find("REBASE acronym")<>-1:
            end_index=index
            break  
        continue
    if end_index==start_index:
        os.system('echo " %s: Page has no line with words REBASE acronym. DNA list skipped." >> %s ' % (genome_id.strip(), protocol ))
        return None
    return [start_index,end_index]

def find_DNAs(genome_id,head_table,protocol):
    """
    Try to find info about DNA in header tables, before title page with word "ORF" 
    """
    if len(head_table)>=3:
        DNAs=[]

        #### Table of DNAs
        if len(head_table[1]) >1:
            if head_table[1][1].find("Sequence length")<>-1:
                for y in head_table[2:] :
                    if len(y)==3:
                        DNAs.append([genome_id.strip(),y[0].replace(":",""),y[1].replace(",","").replace(" bp","").strip(),y[2]])
                    else:
                        os.system('echo " %s: Length of DNA info in line %s is not 3. Skipped." >> %s ' % (genome_id.strip(), y, protocol ))
                if len(DNAs) > 0:
                    return DNAs

        #### "Complete sequence" Info in two lines 
        if len(head_table[1])==1:
            genome_name=""
            if head_table[1][0].find("Complete sequence")<>-1:
                genome_name="Complete_sequence"
            elif head_table[1][0].find("Contig set")<>-1:
                genome_name="Contig_set"
            if genome_name<>"": 
                ttt=head_table[1][0].split(":")
                if len(ttt)>1:
                    DNA_length=ttt[1].split("bp")[0].replace(",","").strip()
                else:
                    DNA_length=-1
                if head_table[2][0].find("GenBank")<> -1:
                    ttt=head_table[2][0].split(":")
                    if len(ttt)>1:
                        DNA_sequence_id=ttt[1].strip()
                    else:
                        DNA_sequence_id="not recovered"
                else:
                    DNA_sequence_id="not recovered"        
                DNAs.append([genome_id.strip(),genome_name,DNA_length,DNA_sequence_id])
                return DNAs

    os.system('echo " %s: Info about DNA was not found. DNAs table empty." >> %s ' % (genome_id.strip(), protocol )) 
    return None


def find_RM_systems(genome_id,page_tables,ORF_indexes,DNAs,protocol):

    DNA_char=["chromosome"," chr.","-chr","plasmid","phage","type"]
    RM_systems=[]

    for i in range(len(ORF_indexes)):
        start_type_index=ORF_indexes[i]-1       #index of ['Type...']
        if i+1==len(ORF_indexes):
            end_type_index=len(page_tables)     #index of next ['Type...'] or end of page_tables+1
        else:
            end_type_index=ORF_indexes[i+1]-1
        RM_type=page_tables[start_type_index]


#### Table of DNA indexes in the type block
        DNA_indexes=[]
        for DNA_index in range(start_type_index,end_type_index):
            if len(page_tables[DNA_index])==0 or (len(page_tables[DNA_index])==1 and page_tables[DNA_index][0]==""):
                continue
            flag=0
            for q in DNA_char:
                if page_tables[DNA_index][0].lower().find(q)<>-1:
                    flag=1
                    break
            if flag==1:
                DNA_indexes.append(DNA_index)

        if len(DNA_indexes)==0:
            DNA_indexes.append(0)
            os.system('echo " %s: no DNAs were found under title Type %s. Type block skipped." >> %s' % (genome_id.strip(),ORF_indexes[i], protocol ))
#            break         
#        if len(DNA_indexes)==0 and DNAs<>None:
    
#### Fill RM_systems 
        for j in range(len(DNA_indexes)): 
            if  DNA_indexes[0]==0:
                start_DNA_index=start_type_index+1
            else:
                start_DNA_index=DNA_indexes[j]
            start_RMs_index=start_DNA_index+1
            if j+1==len(DNA_indexes):
                end_DNA_index=end_type_index
            else:
                end_DNA_index=DNA_indexes[j+1]

            RM_start=len(RM_systems)
            RM_system_name="unknown"
            for RM_index in range(start_RMs_index,end_DNA_index):
                if len(page_tables[RM_index])==0:
                    continue
                elif len(page_tables[RM_index])<>6:
                    os.system('echo " %s: Length of line %s is not 6. Skipped " >> %s' % (genome_id.strip(),page_tables[RM_index], protocol ))
                else:
                    if DNA_indexes[0]==0:
                        DNA_name="Unrecovered"
                        if DNAs<>None:
                            if len(DNAs)==1:
                                DNA_name=DNAs[0][1]
                    else:
                        DNA_name=page_tables[start_DNA_index][0]

                    if page_tables[RM_index][1] <>"":
                        ttt=page_tables[RM_index][4].split(".")
                        if len(ttt)==1:
                            enzyme_system_name=ttt[0]
                        else:
                            enzyme_system_name=ttt[1]
                        if RM_system_name=="unknown":
                            RM_system_name=enzyme_system_name
                        elif RM_system_name<>enzyme_system_name:
                            RM_system_name=RM_system_name + "_" + enzyme_system_name


                    crd=page_tables[RM_index][5].split(" ")
                    c=""
                    if len(crd)==2:
                        c=crd[1]		
                    RM_systems.append([genome_id.strip(),
                                       page_tables[RM_index][0],
                                       page_tables[RM_index][1],
                                       page_tables[RM_index][2],
                                       page_tables[RM_index][3],
                                       page_tables[RM_index][4],
                                       crd[0],
                                       c,
                                       RM_system_name])
#        for t in range(RM_start,len(RM_systems)):
#            RM_systems[t][8]=RM_system_name
              
    return RM_systems


################################## MAIN ###########################################

if len(sys.argv) == 1:
    print "python get_rm_genes.py -h for help"
    exit()

parser = optparse.OptionParser()
parser.add_option("-i", "--in_file", help="In_file with list of ReBase genome ids like 2241", dest="in_file")
parser.add_option("-r", "--out_rm", help="Out_file xls with RM genes info", dest="out_rm", default="RM_systems.xls")
parser.add_option("-d", "--out_dna", help="Out_file xls with DNAs (chomosomes, plasmids) info", dest="out_dna", default="DNAs_info.xls")
parser.add_option("-c", "--coma", action="store_true", help="3.14 or 3,14 on output", dest="coma")
parser.add_option("-u", "--base_url", help="Base url of ReBase genomes", dest="base_url", default="http://tools.neb.com/~vincze/genomes/report.php?genome_id=")
parser.add_option("-t", "--test", action="store_true", help="docttest only")


options, args = parser.parse_args()
vars().update(vars(options))

if test:
    doctest.testmod()
    exit()

if in_file==None:
    print "No file with list of genome ids was specified"
    exit()

# Open protocol
protocol='protocol_' + in_file + '.txt'  
os.system('echo "Protocol" > ' + protocol)
start_time=time()

#Read list of genome ids
f=open(in_file)
genome_ids=f.readlines()
f.close()

h=open(out_rm,'w')
h.write('Genome_ID\tRM_enzyme_type\tRM_system_id\tRM_type\tSpecificity\tCoordinates\tComplement\n')
 
print "Wait..."
 
############################# Start #########################################
for x in genome_ids:

    page_tables=read_and_check(x, protocol) 
    if page_tables==None:
        continue
    organism=page_tables[1][1]

    if page_tables==None:
        continue

    #### Table of title lines 'ORF ...' indexes

    ORF_indexes=find_ORF_titles(x, page_tables, protocol)
    if ORF_indexes==None:
        print "ORF_indexes == None"
        os.system('echo " %s: %s no RM systems " >> %s ' % (x.strip(), organism,  protocol ))
        continue
    print ORF_indexes
    #### Table of DNAs 

    head_table_indexes=find_head_table(x,page_tables,protocol) 
    print "head_table_indexes:"
    print head_table_indexes
    if head_table_indexes==None:
        DNAs=None
    else:
        ttt=page_tables[head_table_indexes[1]][0].split(":")
        if len(ttt) > 1:
            organism_acronym=ttt[1].strip()
        else:
            organism_acronym="failed to recover"
        DNAs=find_DNAs(x, page_tables [head_table_indexes[0]:head_table_indexes[1]], protocol) 
        
   
    #### Table of RM systems

    print "x:"
    print x
   
    RM_systems=find_RM_systems(x,page_tables,ORF_indexes,DNAs, protocol) 
    print "RM:"
    print RM_systems
    if RM_systems==None:
        os.system('echo " %s: No RM systems were recovered from the page" >> %s' % (x.strip(), protocol ))
        continue

    for z in  RM_systems:
        h.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (z[0],z[2],z[3],z[1],z[4],z[6],z[5],z[7],z[8]))
    os.system('echo " %s:  %s completed " >> %s' % (x.strip(),organism, protocol ))

 
h.close()

### END

os.system('echo "Finish. Working time is %d seconds. " >> %s' % (time()-start_time, protocol ))
print "...Done"

exit()
    
