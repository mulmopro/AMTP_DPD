# Automated Method to compute Transport Properties from DPD equilibrium simulations

**Motivations and Application**

The code implements an automated reliable method to compute transport properties from DPD equilibrium simulations performed with LAMMPS. It has the aim of improving the Green-Kubo approach realibility and computational feasibility for the calculation of the zero-shear viscosity in DPD simulations. It is based on an iterative algorithm that automatically finds for a given DPD system:

1) the parameters of the approximated algorithm adopted by LAMMPS (Nrep, Nfreq, Nsim) for the calculation of the SACF with the shortest trajectory and the proper temporal resolution giving the fixed statistical accuracy

2) the resulting viscosity value, the self-diffusion coefficient and the Schmidt number 

**Workflow description**

![Fig1](https://github.com/mulmopro/AMTP_DPD/assets/83214196/b6e45fd8-9cd8-445f-9f6a-ebe8240b5a67)

The Python script constituting the algorithm for transport properties calculation from DPD equilibrium simulations is made of:

main.py - This is the main file of the method that should be executed to start a new cycle of simulations. It doesn't explicitly contain all operations performed by the code, but orchestrates the succession of tasks performed. These tasks include:

	1. Simulation initialization (Setup of the DPD system specific input parameters a, s, sigma, rcD and Setup of the initial guest for Nrep, Nsim and dt to initiate the 1st simulation)
	2. Simulation run
	3. Reading the output of the simulations
	4. Verification of the out-of-loop conditions 

launcher_cluster.py - This contains all the information needed to generate the LAMMPS input script according to the INPUT DATA specified in the main.py and the command line to run LAMMPS in parallel via mpirun. The position of the LAMMPS executable (lmp_mpi) has to be consistent with the path-to-executable in the command line.
	
	1. In this case LAMMPS is run executing the Singularity image out of the folder "lammps_dpdext_SH.sif" by the command  :
	"prun singularity exec ../lammps_dpdext_SH.sif /home/lammps/src/lmp_mpi -in $CASE_IN"
		
	2. To run the LAMMPS executable locally the previous command has to be substituted by: "mpirun -np 6 path/to/lmp_mpi -in $CASE_IN")

ImportDatas.py - This contains a function that imports OUTPUT DATA from the LAMMPS output files and converts it into data that Python is able to manipulate. 

CumulativeIntegral.py - This contains all the instructions to calculate the viscosity cumulative integral (CVI) from the SACF computed by LAMMPS simulation and saved into time_cor.txt file.

MovingSpansAverage.py - This implements an adaptation of the Simple Moving Average algorithm to identify the point where the plateau is reached in the CVI.

v_fitslope_extr.py - This contains a single function that imports from the log.lammps file the values to calculate the self-diffusion coefficient.  

gamma_eff.py - This contains all the functions needed to import the RDF computed by LAMMPS simulation and saved into tmp.rdf file and calculate the effective friction coefficient value.

**Technical informations**

To run the program the command to execute is: "python3 main.py"
The Python libraries needed are NumPy and Pandas. The Python subprocess module is used.
The command running the LAMMPS simulations is in "launcher_cluster.py" as previous explained. 


