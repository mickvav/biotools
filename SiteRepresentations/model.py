#!/usr/bin/env python3
import csv
import numpy as np
import numpy.linalg as li
A=None
B=None
first=1
with open('test.csv', 'r') as csvfile:
    rows = csv.reader(csvfile, delimiter='\t',quotechar='"')
    for row in rows:
        if(first == 1):
             first=0
        else: 
            datarow=[s.replace(',','.') for s in row[1:]]
            if A is None:
                A=np.array([[float(d) for d in datarow[:-2]]])
                B=np.array([float(row[-1].replace(',','.'))])
            else:
                A=np.append(A,[[float(d) for d in datarow[:-2]]], axis=0)
                B=np.append(B,[float(row[-1].replace(',','.'))])

res=li.lstsq(A,B)
sol=res[0]
print(sol)
pred=np.dot(A,sol)
c1=0
c2=0
for i in range(0,len(pred)-1):
    if (pred[i]<0.78 and B[i]>0.78):
        c1+=1
    if (pred[i]>0.78 and B[i]<0.78):
        c2+=1

print(c1)
print(c2)
