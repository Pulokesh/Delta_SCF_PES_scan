#*********************************************************************************
#* Copyright (C) 2017 Ekadashi Pradhan
#*
#* This file is distributed under the terms of the GNU General Public License
#* as published by the Free Software Foundation, either version 2 of
#* the License, or (at your option) any later version.
#* See the file LICENSE in the root directory of this distribution
#* or <http://www.gnu.org/licenses/>.
#*
#*********************************************************************************

import math
import sys
import os


N = 40 # file numbers, grid number
fname = "pes_en/full_re_Ham"
fout = open("pes.out","w")
for i in xrange(N):
    fout.write(" %i "%(i+75)) # 1D cuts along torsional angle from 75 to 114
    f=open(fname+"_%i"%i,"r")
    A=f.readlines()
    f.close()

    for j in xrange(len(A)):
        ja = A[j].split()
        if len(ja) >0:
            fout.write(" %12.7f "%float(ja[j]))
    fout.write("\n")
fout.close()
        

