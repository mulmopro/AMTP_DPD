from CumulativeIntegral import K, cum_integral
from ImportDatas import importdatas
from MovingSpansAverage import MovingSpans


class Launcher_local:

    def __init__(self, rc, rcD, s, a, dt, sigma, neql, nrun, nrunmsd, Nfreq, Nrep):

        ## Import dei dati per generare il file di input di LAMMPS

        self.ndim = 3
        self.xsize, self.ysize, self.zsize = 15,15,15
        
        self.rho = 3
        self.kb = 1
        self.T = 1/self.kb
        self.rc = rc
        self.rcD = rcD
        self.s = s
        self.a = a
        self.dt = dt
        self.sigma = sigma
        self.nBeads = (self.xsize*self.ysize*self.zsize)*self.rho

        self.neql = neql
        self.nrun = nrun
        self.nrunmsd = nrunmsd

        self.Nev = 1
        self.Nrep = Nrep
        self.Nfreq = Nfreq

    def generateFiles(self,filename):

        ## Generazione file di input di LAMMPS con i dati importati prima

        # Il random_code serve per identificare a quale file script.sbatch è associato ogni input_file, oltre che gli output della simulazione con il singolo input file

        import string    
        import random
        S = 4 
        ran = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(S)) 
        random_code = str(ran)
        self.ran_code = random_code

        self.filename = str(filename) + "_" + random_code

        with open(self.filename, "w") as input:

            input.write(
                "# LAMMPS input script specifies a simple DPD simulation about water to calculate Sc number and RDF\n"
                "# Viscosity calculated with Green-Kubo formula\n"
                "# Self-diffusivity calculated with Einstein relation\n\n"

                "# Initialization\n\n"

                "units       lj\n"
                "variable    ndim      equal 3\n\n\n\n"


                "# Box size\n\n"

                "variable    xsize     equal {xsize}\n"
                "variable    ysize     equal {ysize}\n"
                "variable    zsize     equal {zsize}\n\n\n\n"


                "# DPD parameters\n\n"

                "variable    rho       equal {rho}\n"
                "variable    kb        equal {kb}\n"
                "variable    T         equal 1/${{kb}}\n"
                "variable    rc        equal {rc}\n"
                "variable    rcD       equal {rcD}\n"
                "variable    s         equal {s}\n"
                "variable    a         equal {a}\n"
                "variable    dt        equal {dt}\n" 
                "variable    sigma     equal {sigma}\n"
                "variable    nBeads    equal (${{xsize}}*${{ysize}}*${{zsize}})*${{rho}}\n\n\n\n"


                "# Post-processing correlation function parameters\n\n"

                "variable    Nev  equal {Nev}    # correlation length\n"
                "variable    Nrep equal {Nrep}     # sample interval\n"
                "variable    Nfreq  equal {Nfreq}   # dump interval\n\n\n\n"


                "# Simulation parameters\n\n"

                "timestep     ${{dt}}\n"
                "dimension    ${{ndim}}\n" 
                "variable     neql      equal {neql}\n"
                "variable     nrun      equal {nrun}\n"
                "variable     nrunmsd   equal {nrunmsd}\n\n\n\n" 


                "# Create simulation box\n\n"

                "atom_style   atomic\n"
                "boundary     p p p\n" 
                "comm_modify  vel yes\n\n"
                "newton       on\n" 
                "lattice      none 1\n"
                "region       box block 0 ${{xsize}} 0 ${{ysize}} 0 ${{zsize}}\n"
                "create_box   1 box\n"
                "create_atoms 1 random ${{nBeads}}  126775  box\n\n\n\n"


                "# Define masses and interaction coefficient\n\n"

                "pair_style   dpdext/fdt ${{T}} ${{rc}} 123455\n"
                "mass         1 1.0\n"
                "pair_coeff   1 1 ${{a}} ${{sigma}} ${{sigma}} ${{s}} ${{s}} ${{rcD}}\n\n"

                "velocity all create ${{T}} 4928 mom yes dist gaussian\n\n\n\n"

                "fix          1 all shardlow\n"
                "fix          2 all nve\n"
                "thermo       ${{Nfreq}}\n"
                "run          ${{neql}}\n\n"

                "write_restart  dpd_fluid_{random_code}.restart0\n\n\n\n"


                "# Post-processing:\n"
                "# Green-Kubo viscosity calculation\n\n"

                "reset_timestep 0\n"
                "variable pxy equal pxy\n"
                "variable pxz equal pxz\n"
                "variable pyz equal pyz\n"
                "variable V   equal vol\n"
                "variable K   equal 1/(${{kb}}*$T)*$V*${{Nev}}*${{dt}}\n\n"

                "fix              SS all ave/correlate ${{Nev}} ${{Nrep}} ${{Nfreq}} &\n"
                "                v_pxy v_pxz v_pyz type auto file time_cor.txt_{random_code} ave running\n\n"

                "variable v11 equal trap(f_SS[3])*${{K}}\n"
                "variable v22 equal trap(f_SS[4])*${{K}}\n"
                "variable v33 equal trap(f_SS[5])*${{K}}\n\n\n\n"


                "thermo_style custom step temp press v_v11 v_v22 v_v33\n"
                "thermo ${{Nfreq}}\n" 
                "run ${{nrun}}\n\n"

                "write_restart  dpd_fluid_{random_code}.restart1\n\n"

                "variable v equal (v_v11+v_v22+v_v33)/3.0\n"
                'print    "viscosity: $v (DPD units)"\n\n'

                "# Green-Kubo self-diffusivity calculation\n\n" 

                "compute         msd all msd com yes\n"
                "fix             9 all vector ${{Nev}} c_msd[4]\n"
                "variable        fitslope equal slope(f_9)/6/dt\n\n\n\n"


                "# Radial distribution function calculation\n\n"

                "comm_modify cutoff 2\n"
                "compute myRDF all rdf 50 1 1 cutoff ${{rcD}}\n"
                "fix 5 all ave/time 100 1 100 c_myRDF[*] file tmp.rdf mode vector ave running\n\n"

                "thermo_style	custom step temp press c_msd[4] v_fitslope\n\n"

                "run      ${{nrunmsd}}\n\n"

                "# DONE\n".format(xsize = self.xsize, ysize = self.ysize, zsize = self.zsize, rho = self.rho, kb = self.kb, rc = self.rc, rcD = self.rcD, s = self.s, a = self.a, dt = self.dt, sigma = self.sigma, Nev = self.Nev, Nrep = self.Nrep, Nfreq = self.Nfreq, neql = self.neql, nrun = self.nrun, nrunmsd = self.nrunmsd, random_code = self.ran_code)
                )

    def launchSims(self):

        import subprocess

        subprocess.run('CASE_IN="{filename}"; mpirun -np 8 /path/to/lammps/src/lmp_mpi -in $CASE_IN'.format(filename = self.filename),shell=True)

    def checkNrep(self,window,err_rel,jump_index):

        # Importing datas
        timestep, pxy, pxz, pyz = importdatas("time_cor.txt_{ran_code}".format(ran_code = self.ran_code),self.Nrep)

        # Generating the cumulative integral
        cum_int = cum_integral(timestep, pxy, pxz, pyz, K=K(self.kb,self.Nev,15**3,self.dt,return_value="n"))

        # Finding the plateau
        visc_init = MovingSpans(cum_int)
        visc_plateau, Nrep, flag = visc_init.runAve(window,err_rel,jump_index,printNrep="n")

        return visc_plateau, Nrep, flag
    
    def checkN(self):

        # Importing datas
        timestep, pxy, pxz, pyz = importdatas("time_cor.txt_{ran_code}".format(ran_code = self.ran_code),self.Nrep)

        # Generating the cumulative integral
        cum_int = cum_integral(timestep, pxy, pxz, pyz, K=K(self.kb,self.Nev,15**3,self.dt,return_value="n"))

        # COV & STD
        import numpy as np
        cov = lambda x: np.std(x, ddof=1) / np.mean(x)
        cov_tmp = cov(cum_int)

        return cov_tmp
    
    def currentFile(self):
        return self.filename,self.ran_code
