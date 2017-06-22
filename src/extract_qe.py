#*********************************************************************************
#* Copyright (C) 2017 Ekadashi Pradhan, Alexey V. Akimov
#*
#* This file is distributed under the terms of the GNU General Public License
#* as published by the Free Software Foundation, either version 2 of
#* the License, or (at your option) any later version.
#* See the file LICENSE in the root directory of this distribution
#* or <http://www.gnu.org/licenses/>.
#*^M
#*********************************************************************************/^M

import os
import sys
import math

if sys.platform=="cygwin":
    from cyglibra_core import *
elif sys.platform=="linux" or sys.platform=="linux2":
    from liblibra_core import *

from libra_py import *


def fermi_pop(e,nel,spn,kT,el_st):  # <--- Now population scheme for all the MOs 
    ##
    #
    etol = 0.0000000001
    pop_opt,pop_tot,pop_av = 1,[],[]
    ##if el_st > 1:  # For S0
    #if el_st > 0:  # For S0 and S1 the regular Fermi scheme is used
    el_scheme = [0] # or =[-1,0,1] for other scheme
    ##if el_st ==1:  # For S1
    ##    el_scheme = [-1,0,1]
    
    N = len(e)  # number of active space orbitals - at this point using full orbital space.
    for ib in xrange(N):
        pop_av.append(0.0)
    for ia in el_scheme: #[-1,0,1]: # 0 for N-1, 1 for N and 2 for N+1 electrons
        if spn ==1:
            Nel=nel + ia #nel/2 + nel%2
            degen = 2
        if spn ==2:
            Nel=nel/2 + nel%2 + ia
            degen = 1
        a = MATRIX(N,N)
        for i in xrange(N):
            for j in xrange(N):
                if i==j:
                    a.set(i,j, e[i])
                else:
                    a.set(i,j, 0.0)
        bnds = order_bands(a)
        pop_fermi = populate_bands(Nel, degen, kT, etol, pop_opt, bnds)
        pop_tot.append([item[1] for item in pop_fermi]) #  pop_fermi[:10][1]
    #   For S1

    for ic in xrange(N):
    ##    if el_st ==1: # For S1
    ##        pop_av[ic] = pop_tot[0][ic]+pop_tot[2][ic] - pop_tot[1][ic]
    # For S0
    #for ic in xrange(N):
    ##    else:  # For S0
    ##        pop_av[ic] = pop_tot[0][ic]
        pop_av[ic] = pop_tot[0][ic] # or something else pop_av[ic] = pop_tot[0][ic]+pop_tot[2][ic] - pop_tot[1][ic]

    return pop_av

def qe_extract_eigenvalues(filename,nel):
    f = open(filename,"r")
    a = f.readlines()
    na = len(a)
    HOMO = (nel/2 + nel%2) - 1
    en_alp = []
    for i in xrange(na):
        fa = a[i].split()
        if len(fa) > 0 and fa[0] =="<EIGENVALUES":
            eig_num = i + 1
        if len(fa) > 0 and fa[0] =="</EIGENVALUES>":
            eig_num_end = i 

    eig_val = []
    for ia in range(eig_num,eig_num_end):  # Here we include all the MOs
        fa = a[ia].split()
        eig_val.append(float(fa[0]))
    return eig_val


def check_convergence(filename):

    f_out = open(filename, "r")
    A = f_out.readlines()
    f_out.close()

    status = 1 # 0 is okay, non-zero is somethig else
    nlines = len(A)

    for a in A:
        s = a.split()
        if len(s) > 0 and s[0] == "convergence"  and s[3] == "achieved":
            status = 0

    return status


def qe_extract_info(filename, ex_st): 
##
# This function reads Quantum Espresso output and extracts 
# the descriptive data.
# \param[in] filename The name of the QE output file which we unpack
#
    f_qe = open(filename, "r")
    A = f_qe.readlines()
    f_qe.close()
    Ry_to_Ha = 0.5
    alat = -1.0
    nel, norb, nat = -1, -1, -1
    nlines = len(A)
    tot_ene = 0.0 # in case convergence not achieved in first attempt when index informations are extracted

    for a in A:
        s = a.split() 
        # number of electrons       =        12.00
        if len(s) > 0 and s[0] == "number" and s[2] == "electrons":
            nel = int(float(s[4]))

        # number of Kohn-Sham states=           12  
        if len(s) > 0 and s[0] == "number" and s[2] == "Kohn-Sham":
            norb = int(float(s[4]))

        # number of atoms/cell      =            6
        if len(s) > 0 and s[0] == "number" and s[2] == "atoms/cell":
            nat = int(float(s[4]))

        # lattice parameter (alat)  =       1.8900  a.u.
        if len(s) > 0 and s[0] == "lattice" and s[1] == "parameter" and s[2] == "(alat)":
            alat = float(s[4])

        # !    total energy              =     -27.62882078 Ry
        if len(s) > 0 and s[0] == "!" and s[1] == "total" and s[2] == "energy":
            tot_ene = Ry_to_Ha*float(s[4]) # so convert energy into atomic units

    if alat<0.0:
        print "Error in unpack_file\n"
        print "Lattice parameter is not found. Exiting...\n"
        sys.exit(0)
    if nel==-1:
        print "Error in unpack_file\n"
        print "The number of electronis is not found. Exiting...\n"
        sys.exit(0)
    if nat==-1:
        print "Error in unpack_file\n"
        print "The number of atoms is not found. Exiting...\n"
        sys.exit(0)
    if norb==-1:
        print "Error in unpack_file\n"
        print "The number of bands (orbitals) is not found. Exiting...\n"
        sys.exit(0)

    return tot_ene,norb, nel, nat, alat

def qe_extract(filename, ex_st, nspin):
    ##
    #

    # Read the descriptive info
    tot_ene, norb, nel, nat, alat = qe_extract_info(filename, ex_st)
    f_qe = open(filename, "r")
    A = f_qe.readlines()
    f_qe.close()

    return tot_ene


