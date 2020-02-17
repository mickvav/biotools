#!/usr/bin/python3
#
#  Example of library usage.
# 
#  expecting to have fasta file as argument, file should contain multiple
#  chromosomes as separate entries.
#
#
from sys import argv
from getcontext import FullGenome

G=FullGenome(argv[1])

print(G.getcontext(0,10))
print(G.getcontext(0,100))
print(G.getcontext(0,2))
print(G.getcontext(0,3))
print(G.getcontext(0,4))
print(G.getcontext(0,5))
print(G.getcontext(0,6))
print("AAA nearest to 10 in 1'st chromosome:")
print(G.findnearestcontext("AAA",0,10))
print("AAA nearest to 10000000 in 1'st chromosome:")
print(G.findnearestcontext("AAA",0,10000000))
