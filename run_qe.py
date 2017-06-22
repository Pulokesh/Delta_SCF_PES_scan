import os
import sys
import math

if sys.platform=="cygwin":
    from cyglibra_core import *
elif sys.platform=="linux" or sys.platform=="linux2":
    from liblibra_core import *
from libra_py import *

user = 1  # 0 - Alexey, 1 - Ekadashi

################ System-specific settings ########################
if user==0:
    # For Alexey
    libra_bin_path = "/projects/academic/alexeyak/alexeyak/libra-dev/libracode-code/_build/src" # set the path name to the source files in libracode
    libra_qe_int_path = "/user/alexeyak/Programming/libra-gamess_interface/src"

elif user==1:
    # For Ekadashi
    libra_bin_path = "/projects/academic/alexeyak/ekadashi/libracode-dev/libracode-code/_build/src"
    libra_qe_int_path = "/projects/academic/alexeyak/ekadashi/Delta_SCF_PES_scan/src"


os.environ["src_path"] = libra_qe_int_path   # Path to the source code
sys.path.insert(1,os.environ["src_path"])    # Path to the source code

#import main  This will later be attached to main LIBRA-X
import scanPES

########## Setup all manual parameters here ####################
params = {}
params["nproc"] = 12              # the number of processors
params["nspin"] = 2
params["electronic_smearing"] = 0.01
#-------------------------
params["scf_itr"] = 2
params["smear_scheme"] = 1 # 1 for [-1,0,1] for S1, 0 for [0] of S0
#-------------------------
params["excitations"] = [ excitation(0,1,1,1) ] #[ excitation(0,1,0,1), excitation(0,1,1,1), excitation(0,1,0,1) ]
params["excitations_init"] = [1]
params["HOMO"] = 0
params["min_shift"] = 0
params["max_shift"] = 1 
for i in range(0,len(params["excitations"])):
    params["qe_inp0%i" %i] = "x%i.scf.in" %i    # initial input file
    params["qe_inp%i" %i] = "x%i.scf_wrk.in" %i # working input file 
    params["qe_out%i" %i] = "x%i.scf.out" %i    # output file

cwd = os.getcwd()
params["pes_en"] = cwd+"/pes_en/"
params["print_pes_en"] = 1
params["run_option"]=-1 # 1 for Delta-SCF-NA-MD; -1 for PES scan
#if params["run_option"]==-1: 
#    scanPES.scanPES(params)  # run actual calculations
#else:
#    main.main(params)

#################################
#      Run actual calculation   #
#################################
scanPES.scanPES(params)
#################################

