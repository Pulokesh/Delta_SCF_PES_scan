import math
import sys
import os


N = 185 # file numbers, grid number
fname = "pes_en/full_re_Ham"
fout = open("pes.out","w")
for i in xrange(N):
    fout.write(" %i "%(i+75))
    f=open(fname+"_%i"%i,"r")
    A=f.readlines()
    f.close()

    for j in xrange(len(A)):
        #if len(A[j])>0:
        ja = A[j].split()
        if len(ja) >0:
            fout.write(" %12.7f "%float(ja[j]))
    fout.write("\n")
fout.close()
        

