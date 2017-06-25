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

## \file x_libra_qe.py 

import os
import sys
import math

if sys.platform=="cygwin":
    from cyglibra_core import *
elif sys.platform=="linux" or sys.platform=="linux2":
    from liblibra_core import *

from extract_qe import *
from create_input_qe import *

def exe_espresso(i):
##
# Function for executing calculations using Quantum Espresso
# once the calculations are finished, all the temporary data are
# deleted
# \param[in] inp The name of the input file
# \param[in] out The name of the output file
#
    inp = "x%i.scf_wrk.in" % i # e.g. "x0.scf_wrk.in"
    out = "x%i.scf.out" % i    # e.g. "x0.scf.out"
    os.system("srun pw.x < %s > %s" % (inp,out))

def qe_to_libra(params, cord, suff):
    ##
    # This function takes input parameters and coordinates and run QE scf calculation,
    # Check convergence, exctract energies if convergence is achieved, invoke Fermi population scheme if
    # SCF is not converged.

    nstates = len(params["excitations"])
    E2 = MATRIX(nstates,nstates)
    nspin = params["nspin"]
    nel = params["nel"]
    #======== Run QE calculations and get the info  ========
    for ex_st in xrange(nstates): # for each excited configuration
        
        excitation = params["excitations"][ex_st]
        occ, occ_alp, occ_bet = excitation_to_qe_occ(params, excitation)
        status = -1
        restart_flag = 0
        coount = 0
        while status != 0: #for i in xrange(5):
            coount = coount + 1
            write_qe_input(ex_st,cord,params,occ,occ_alp,occ_bet,restart_flag)
            exe_espresso(ex_st)
            status = check_convergence("x%i.scf.out" % ex_st) # returns 0 if SCF converges, 1 if not converges
            if status == 0:
                tot_ene = qe_extract("x%i.scf.out" % ex_st, ex_st, nspin)
            else:
                if coount==1:
                    restart_flag = 10  # For the first time after SCF break
                else:
                    restart_flag = 11  # Second iteration after SCF break
                if params["nspin"] == 2: # Spin-polar
                    en_alp = qe_extract_eigenvalues("x%i.save/K00001/eigenval1.xml"%ex_st,nel)
                    en_bet = qe_extract_eigenvalues("x%i.save/K00001/eigenval2.xml"%ex_st,nel)
<<<<<<< HEAD
                    occ_alp = fermi_pop(en_alp,nel,params) # 1 for alpha
                    occ_bet = fermi_pop(en_bet,nel,params) # -1 for beta spin

                if params["nspin"] == 1: # non-Spin-polar
                    en_alp = qe_extract_eigenvalues("x%i.save/K00001/eigenval.xml"%ex_st,nel)
                    occ = fermi_pop(en_alp,nel,params)
=======
                    occ_alp = fermi_pop(en_alp,nel,params,1) # 1 for alpha spin index
                    occ_bet = fermi_pop(en_bet,nel,params,-1) # -1 for beta spin index

                if params["nspin"] == 1: # non-Spin-polar
                    en_alp = qe_extract_eigenvalues("x%i.save/K00001/eigenval.xml"%ex_st,nel)
                    occ = fermi_pop(en_alp,nel,params,1)
>>>>>>> devel
        E2.set(ex_st, ex_st, tot_ene)
    #---------------------------------------------------------------
    #               Print total energies                           #
    #---------------------------------------------------------------
    if params["print_pes_en"]==1:
        E2.show_matrix(params["pes_en"]+"full_re_Ham_"+suff)

