import math
import os
import sys



def run_coord():
    ##
    # This function outputs 1D cuts coords in each 5 deg interval

    cf=open("traj.xyz","r")
    CRD=cf.readlines()
    cf.close()
    natm= 24 #params["nat"] #Number of atoms, 24 for azobenzene
    snps=(len(CRD))/(natm+2) # Total number of trajectories
    nl0,nl1=0,0
    deg_intr = 5
    deg_lst = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120,125,130,135,140,145,150,155,160,165,170,175,180]
    fut=open("new_coord.xyz","w")
    
    for i in deg_lst:
        nl0 = i*(natm+2)+2
        nl1 = nl0 + natm

        #print "Grid point %i"%i
        #print CRD[nl0:nl1]
        fut.write(" 24 \n    CNNC= %i \n"%i)    
        for j in xrange(natm):
            fut.write(" %s"%CRD[nl0:nl1][j])
        #fut.write("\n")
    fut.close()
        #qe_to_libra(params, CRD[nl0:nl1], str(i))

#--------------------
#   main function call
#--------------------

run_coord()
print "Done creating new coord file!!!"
