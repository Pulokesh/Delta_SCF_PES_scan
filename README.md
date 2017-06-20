# Delta_SCF_PES_scan

   Getting started
## Required softwares
   Libra and Quantum Espresso
   >Download and install [Libra] and [Quantum Espresso]  <br/>
   >Instructions for Libra installation are provided in Libra website [link1].

## Clone or Download this repository
   You can download ZIP file in to your computer or clone entire folder in to your local working directory.
   > For cloning, Copy path to clipboard, then go to your local working directory and type <br/>
   > git clone path-of-the-repository <br/>

## How does it work ?
   In this directory, you will find "src" folder, quantum espresso input and submission scripts, and python scripts.
 - src : Where all the source codes are placed. You don't need to change any files in this directory. If new updates are
         available, git pull will automatically update it.
 - run_qe.py : Here system specific parameters are provided.

### Step-by-Step
1. Create a trajectory file, traj.xyz comtainig 2D, 1D (or random geometries) grid points. If you have 1D or 2D grid in Cartesian coordinate, you are good to go. If you don't have, check out the strategy how I generate 1D or 2D grid points. ([How To Generate Grid Trajectory](#how-to-generate-grid-trajectory)).
2. Create pes_en directory where results will be saved.
3. Edit run_qe.py script as required. ([How To Edit Run Script](#how-to-edit-run-script))
4. Edit "x_i.scf.in"files. ([Editing QE Input Files](#editing-qe-input-files))
   These are Quantum espresso input file for SCF
   calculations. "_i" extension for each of the electronic
   states included in the NAMD calculation.
5. submit submit_templ_qe.slm submission script. If it is a small calculation, you can run on the head
   node by just "python run_qe.py"
6. Upon completion of caculation, results will be printed in pes_en folders.

  

## How To Edit Run Script
```sh
There are many system specific parameters in thi run_qe.py script
and they are presented as params["name-of-the-parameter"]

 - Create a new use index number. Specify "libra_bin_path" and "libra_qe_int_path" for the user.
 - Description of other simulation parameters such as number of processors, number of snaps, 
   nuclear time step, etc., are provided in the run_qe.py script.
 - One of the most important parameters is params["excitations"] 
   which is constructed by excitation() object. This excitation() objct takes 
   four integer arguments for a specific electronic state. From orbital(fo) from spin(fs) 
   to orbital(to) to spin(ts).
  -- As an example, excitation(0101) presents S0 (ground state), 
     excitation(0111) define S1 excited state. Here, orbital numbering 
     starts from HOMO (0). Alpha (up) spin labeled as 1 and beta 
     (down) spin indexed as -1.
 
   
```

## Editing QE Input Files
```sh
While most of the Quantum Espresso input documentation are available in 
their website, some important requirement for libra-QE are given here.
 - pseudo_dir = 'path of pseudo potential files',
 - prefix = 'xi', i varies for different electronic states, eg., for S0, pseudo_dir = "x0" 
 - nspin = 2, this is for spin polarized calculation
 - K_POINTS automatic, For current version, later it will be extended for gamma points.
   1 1 1  0 0 0
 - OCCUPATIONS, This is the most important input specification for Delta-SCF calculation
   Alpha and beta spins orbitals occupations are provided. Single line break is requred between them.
   Although integer occupation number is provided, if SCF does not converge due
   to degeneracy problem or multireference character of the electronic wavefunction, a fermi 
   population is considered and calculation is restarted. This is done automatiocally in the main
   script.
```

[Quantum Espresso]: <http://www.quantum-espresso.org/>
[Libra]: <http://www.acsu.buffalo.edu/~alexeyak/libra/index.html>
[link1]: <http://www.acsu.buffalo.edu/~alexeyak/libra/installation.html>
