#*********************************************************************************
#* Copyright (C) 2017 Ekadashi Pradhan, Alexey V. Akimov
#*
#* This file is distributed under the terms of the GNU General Public License
#* as published by the Free Software Foundation, either version 2 of
#* the License, or (at your option) any later version.
#* See the file LICENSE in the root directory of this distribution
#* or <http://www.gnu.org/licenses/>.
#*
#*********************************************************************************/

## \file scanPES.py
# This module runs QE SCF calculation on a given grid of
# internal coordinates and extracts energies corresponding to that
# geometry and electronic state.

import os
import sys
import math

if sys.platform=="cygwin":
    from cyglibra_core import *
elif sys.platform=="linux" or sys.platform=="linux2":
    from liblibra_core import *
from libra_py import *

from x_to_libra_qe import *
from extract_qe import *

def run_scan(params):
    ##
    # This function calls qe_to_libra function from x_to_libra_qe module
    # The function qe_to_libra then process the rest of functionality of PES scan
    nstates = len(params["excitations"])
    cf=open("traj.xyz","r")
    CRD=cf.readlines()
    cf.close()
    natm=params["nat"] #Number of atoms, 24 for azobenzene
    snps=(len(CRD))/(params["nat"]+2) # Total number of trajectories
    nl0,nl1=0,0
    for i in xrange(snps):   
        nl0 = i*(natm+2)+2
        nl1 = nl0 + natm

        print "Grid point %i"%i
        qe_to_libra(params, CRD[nl0:nl1], str(i))


def scanPES(params):
    ##
    # This function takes input parameters and coordinates, runs an initial QE calculation,
    # extract and same additional system parameters, such as number of orbitals, number of atoms etc.
    # Finlly calls run_scan function for scanning the PES
    # Used in: run_qe.py

    nstates = len(params["excitations"])
    nspin = params["nspin"]

    for ex_st in xrange(nstates):
        os.system("cp x%i.scf.in x%i.scf_wrk.in" % (ex_st, ex_st))

    params["qe_inp_templ"] = []
    for ex_st in xrange(nstates): #

        params["qe_inp_templ"].append( read_qe_inp_templ("x%i.scf_wrk.in" % ex_st) )
        exe_espresso(ex_st)
        if ex_st ==0:
            tot_ene, params["norb"], params["nel"], params["nat"], params["alat"] = qe_extract_info("x%i.scf.out" % ex_st, ex_st)
    
    print "run PES scan"
    run_scan(params)
    print "------------------- \n ------ END of PES SCANNING JOB ------ \n ------------------"
