import math
import sys
import os

ia = 5  # CNNC
ib = 31 # NNCC
N = ia*ib #52 # file numbers, grid number
fname = "pes_en/full_re_Ham"
fout = open("pes_cut.out","w")
for ia1 in xrange(ia):
    for ib1 in xrange(ib):
        fout.write(" %i %i "%((ia1*6+84),(ib1*6+0)))
        f=open(fname+"_%i"%(ia1*ib+ib1),"r")
        A=f.readlines()
        f.close()

        for j in xrange(len(A)):
            ja = A[j].split()
            if len(ja) >0:
                fout.write(" %12.7f "%float(ja[j]))
        fout.write("\n")
    fout.write("\n")
fout.close()
        


