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

## \file create_qe_input.py
# This module implements the functions which prepare QE input with different occupation schemes
#

import os
import sys
import math

if sys.platform=="cygwin":
    from cyglibra_core import *
elif sys.platform=="linux" or sys.platform=="linux2":
    from liblibra_core import *

from libra_py import *


def read_qe_inp_templ(inp_filename):
##
# Reading and storing template input file for QE calculations. The input file is essentially a
# normal input file, but we store only the constant section (control option), not the
# coordinates. The latter will be updated at each iteration using the propagated objects
#
# \param[in] inp_filename The name of the initial input file, which will serve as a template
#

    f = open(inp_filename,"r")
    templ = f.readlines()
    f.close()

    for a in templ:
        s = a.split()
        if len(s) > 0 and s[0] == "celldm(1)" and s[1] == "=":
            sa = s[2].split(',')
            cell_dm = float(sa[0])
            break

    # Find the line preceeding the actual atomic coordinates
    for a in templ:
        s = a.split()
        if len(s) > 0 and s[0] == "ATOMIC_POSITIONS":
            ikeep = templ.index(a)
            break

    N = len(templ)
    # Blank space for the atomic positions
    templ[ikeep+1:N] = []
    for i in xrange(ikeep+1):
        print templ[i]


    return  templ




def excitation_to_qe_occ(params, state):
##
# This function converts the Libra "excitation" object to the QE occupation scheme
# \param[in] params Control parameters
# \param[in] state The excitation to convert into QE format
#
# Returns a list of occupation numbers of the alpha, beta, and total (doubly degenerate) orbitals


    norb = params["norb"] # the number of KS orbitals
    nel = params["nel"]    # the number of electrons

    # Number of occupied alpha and beta orbitals
    nocc_alp = nel/2  # integer division!
    nocc_bet = nel - nocc_alp
    homo = nocc_alp -1  # changed indices in order to accomodate with python numbering

    # Generate reference (ground state) occupation scheme for alpha and beta orbitals
    gs_alp = []
    gs_bet = []
    for i in xrange(norb):
        if i<nocc_alp:
            gs_alp.append([i,1.0])
        else:
            gs_alp.append([i,0.0])

        if i<nocc_bet:
            gs_bet.append([i,1.0])
        else:
            gs_bet.append([i,0.0])

    # Compute indices of the orbitals involved in the excitation
    a = state.from_orbit[0] + homo  
    a_s = state.from_spin[0]  # +1 for alp, -1 for bet
    b = state.to_orbit[0] + homo   
    b_s = state.to_spin[0]    # +1 for alp, -1 for bet

    # Do separate alpha and beta excitations
    # Here we use "excite" function from the core of Libra package
    ex_alp = []
    ex_bet = []
    if a_s==1 and a_s == b_s:
        ex_alp = excite(a,b,gs_alp) 
        ex_bet = gs_bet
    elif a_s==-1 and a_s == b_s:
        ex_alp = gs_alp
        ex_bet = excite(a,b,gs_bet)
    else:
        print "Error in qe_occ: excitations with spin flip are not allowed yet\nExiting...\n"
        sys.exit(0)


    # So far we only look at the non-spin-polarized case, so lets compute the
    # total occupation numbers
    occ = [0.0]*norb
    occ_alp = [0.0]*norb
    occ_bet = [0.0]*norb

    for i in xrange(norb):
        occ_alp[i] = ex_alp[i][1]
        occ_bet[i] = ex_bet[i][1]
        occ[i] = ex_alp[i][1] + ex_bet[i][1]

    return occ, occ_alp, occ_bet


def print_occupations(occ):
##
# This function transforms the list of occupations into a formatted
# text. The format is consistent with QE input
# \param[in] occ Occupation scheme representing an excitation (list of floats/integers)
#

    #line = "OCCUPATIONS\n"
    line = ""
    count = 0
    for f in occ:
        line = line + "%12.8f " % f
        count = count +1
        if count % 10 ==0:
            line = line + "\n"
    line = line + "\n"

    return line


def write_qe_input(ex_st, cord, params,occ,occ_alp,occ_bet,restart_flag):
    ##
    # This function writes QE input files using coordinates, occupations bot integer and fractional
    #
    HOMO = params["nel"]/2 - 1 # It must be integer, This is HOMO index
    excitation = params["excitations"][ex_st]
    qe_inp = "x%i.scf_wrk.in" % ex_st

    qe_inp_templ = params["qe_inp_templ"][ex_st]
    cell_dm = params["alat"]
    pp = qe_inp.split('.')
    pfx = pp[0] #"x0" #pp[0] #"x0" #pp[0]
    g = open(qe_inp, "w")     

    # Write control parameters section
    for a in qe_inp_templ:
        aa = a.split()
        if len(aa) >0 and aa[0] == "prefix":
            a = "  prefix = '%s',\n"%pfx
        if len(aa) >0 and aa[0] == "&ELECTRONS" and restart_flag==11: # Second time after SCF break, 
        # wavefunctions and potentials are initiated from previous calculation, 10
            a = "&ELECTRONS \n startingwfc = 'file', \n startingpot = 'file', \n"        
        if len(aa) >0 and aa[0] == "&ELECTRONS" and restart_flag==10:  # First time after SCF breaks,
        # No need to restart wavefunctions and potentials from last SCF calculation
            a = "&ELECTRONS \n"
<<<<<<< HEAD
        if len(aa) >0 and aa[0] == "electron_maxstep" and restart_flag>9:
            a = " electron_maxstep = 2, \n "
=======
        if len(aa) >0 and aa[0] == "electron_maxstep" and restart_flag>9: # For both of the the new SCF iterations
        # steps will be very small, 2. It can also be varied.
            a = " electron_maxstep = %i, \n "%params["scf_itr"]
>>>>>>> devel
    

        g.write(a)
    g.write("\n")

    # Write atom name and coordinatess
    B_to_A = 1.0/cell_dm   # Bohr to Angstrom conversion

    for k in cord:
        g.write("%s"  %k )
    g.write("\n")

    # Write occupation
    g.write(""+'\n')
    g.write("OCCUPATIONS"+'\n')

    # Spin-restricted single excitations
    if params["nspin"] <= 1:
        g.write(print_occupations(occ))
        g.write(""+'\n')

    # Spin-unrestricted single excitations
    if params["nspin"] >1:
        g.write(print_occupations(occ_alp))
        g.write(""+'\n')
        g.write(print_occupations(occ_bet))
        
    g.close()
