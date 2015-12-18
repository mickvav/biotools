#!/usr/bin/env python3
import sys
import csv
import math
import numpy as np
import numpy.linalg as li
A=None
B=None
colnames=None
rownames=None

def PreprocA(x):
    return math.log1p(x)

def PreprocB(x):
    return x
first=1
if (len(sys.argv)>2):
    if (sys.argv[2] == 'Always1'):
        shift=-2
        substr=".A1"
        threshold=0.78
else:
    shift=-1
    substr=""
    threshold=0.22
f = open(sys.argv[1]+substr+".Solution.csv", "w") 
g = open(sys.argv[1]+substr+".Common.csv", "w")
h = open(sys.argv[1]+substr+".Results.csv", "w")
with open(sys.argv[1], 'r') as csvfile:
    rows = csv.reader(csvfile, delimiter='\t',quotechar='"')
    for row in rows:
        if(first == 1):
             first=0
             colnames=row[1:]
        else: 
            datarow=[s.replace(',','.') for s in row[1:]]
            if A is None:
                rownames=[row[0]]
                A=np.array([[ PreprocA(float(d)) for d in datarow[:-2]]])
                B=np.array([ PreprocB(float(row[shift].replace(',','.')))])
            else:
                rownames.append(row[0])
                A=np.append(A,[[ PreprocA(float(d)) for d in datarow[:-2]]], axis=0)
                B=np.append(B,[ PreprocB(float(row[shift].replace(',','.')))])

print("B=",B)
if (substr == ".A1"):
    A=np.c_[A,np.ones(len(B))]
##
#
#  Solving least squares problem
#
##
#res=li.lstsq(A,B,rcond=1e-2)
res=li.lstsq(A,B)

sol=res[0]
if (substr == ".A1"):
    colnames[len(sol)-1]='Always1'

print("Solution:")
for i in range(0,len(sol)):
    print(colnames[i],"\t",sol[i])
    f.write(colnames[i]+"\t"+str(sol[i])+"\n")
pred=np.dot(A,sol)
c1=0
c2=0
print("Test results:")
for i in range(0,len(pred)-1):
    if (pred[i]<=threshold and B[i]>=threshold):
        print("underprediction:",rownames[i])
        c1+=1
    if (pred[i]>=threshold and B[i]<=threshold):
        print("overprediction:",rownames[i])
        c2+=1
a="Total underpredicted: "+str(c1)+" overpredicted: "+str(c2)
g.write(a)


h.write("Name\tValue\tPrediction"+"\n")
for i in range(0,len(pred)-1):
    h.write(rownames[i]+"\t"+str(B[i])+"\t"+str(pred[i])+"\n")
##
#
# Computing Coefficient_of_determination
# (https://en.wikipedia.org/wiki/Coefficient_of_determination)
##
ymean=np.mean(B)
SStot=0
SSres=0
for i in range(0,len(pred)-1):
    SStot=SStot+(B[i]-ymean)**2
    SSres=SSres+(pred[i]-B[i])**2

Rsq=1-SSres/SStot

print("Ymean:"+str(ymean))
print("SStot:"+str(SStot))
print("SSres:"+str(SSres))
g.write("Coefficient of determination: "+str(Rsq)+" \n")
print("Coefficient of determination: "+str(Rsq))

## 
#
# Computing lack of fit sum of squares
#
# https://en.wikipedia.org/wiki/Lack-of-fit_sum_of_squares
#
##



f.close()
g.close()
h.close()
    
