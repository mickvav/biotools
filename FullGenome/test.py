#!/usr/bin/python

from sys import argv
from getcontext import FullGenome

G=FullGenome(argv[1])

print G.getcontext(0,10)
print G.getcontext(0,100)
print G.getcontext(0,2)
print G.getcontext(0,3)
print G.getcontext(0,4)
print G.getcontext(0,5)
print G.getcontext(0,6)
