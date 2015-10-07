#!/usr/bin/env python3
import sys
import csv
import numpy as np
import numpy.linalg as li
A=None
B=None
colnames=None
rownames=None
first=1
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
                A=np.array([[float(d) for d in datarow[:-2]]])
                B=np.array([float(row[-1].replace(',','.'))])
            else:
                rownames.append(row[0])
                A=np.append(A,[[float(d) for d in datarow[:-2]]], axis=0)
                B=np.append(B,[float(row[-1].replace(',','.'))])

res=li.lstsq(A,B)
sol=res[0]
print("Solution:")
for i in range(0,len(sol)-1):
    print(colnames[i],"\t",sol[i])

pred=np.dot(A,sol)
c1=0
c2=0
print("Test results:")
for i in range(0,len(pred)-1):
    if (pred[i]<0.78 and B[i]>0.78):
        print("underprediction:",rownames[i])
        c1+=1
    if (pred[i]>0.78 and B[i]<0.78):
        print("overprediction:",rownames[i])
        c2+=1
print("Total underpredicted: ",c1," overpredicted: ",c2)
