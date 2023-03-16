### Launcher & Checking algorythm to find valid values of N & Nrep in order to calculate a correct value of Viscosity

## Launch & 1° Step - We must set a first value for N and for Nrep to initiate the first simulation

## Nm 1 - gamma 4.5 - s 1 - rcD 1 - dt 0.05

from launcher_cluster import *
import subprocess

# DATAS

NFREQ = 500
NREP = 500
N = 500
DT = 0.04

# Input file

RHO = 3
rc = 1
rcD = 1
s = 0.5
a = 25
sigma = 6
neql = 2.0e5
nrun = N*NFREQ
nrunmsd = 5.0e4

print("STARTING NREP ROUTINE")

visc_list_2 = [1.0e3]

while True:

    visc_list_1 = []
    i = 0

    while True:
        simulation = Launcher_local(rc, rcD, s, a, DT, sigma, neql, N*NFREQ, nrunmsd, NFREQ, NREP)  # 1° Trial
        simulation.generateFiles("in.Sh")
        current_file,ran_code = simulation.currentFile()

        print("Simulation Launch -> {current_file}\nNFREQ = {NFREQ}\nNREP = {NREP}\nN = {N}\n".format(current_file = current_file, NFREQ = NFREQ, NREP = NREP, N = N))

        simulation.launchSims()

        # Inputs of the checking algorithm
        WINDOW = 30
        ERR_REL = 1.0e-2
        JUMP_INDEX = 8

        # Try/Except to ignore the TypeError that would stop the iteration without a convergence
        try:
            visc_plateau, Nrep, flag_plateau = simulation.checkNrep(WINDOW,ERR_REL,JUMP_INDEX)
            visc_list_1.append(visc_plateau)
            print("Viscosity value found: {viscosity}".format(viscosity = visc_list_1[-1]))
        except TypeError:
            pass

        with open("results_{ran_code}.txt".format(ran_code = ran_code), "w") as res:

            res.write(
                "# Results\n\n\n"

                "filename: {file}\n\n"
                "NFREQ = {NFREQ}\n"
                "NREP = {NREP}\n"
                "N = {N}\n"
                "DT = {DT}\n\n"

                "Viscosity: {visc}\n".format(file = current_file, NFREQ = NFREQ, NREP = NREP, N = N, DT = DT, visc = visc_list_1[-1])
            )

        # Generate Directory & move files inside
        subprocess.run("mkdir {ran_code}; mv {current_file} time_cor.txt_{ran_code} results_{ran_code}.txt log.cite log.lammps dpd_fluid_{ran_code}.restart0 dpd_fluid_{ran_code}.restart1 tmp.rdf video.lammpstrj {ran_code}".format(ran_code = ran_code, current_file = current_file),shell=True)

        # Incremento di Nrep & Nfreq a N costante = 500
        if i == 5:
            N += 250    # Se N non è abbastanza elevato per avere la formazione di un plateau, allora ogni 5 simulazioni non riuscite questo sistema incrementa anche N
        else:
            pass

        if flag_plateau == 0:
            NREP += 500
            NFREQ += 500
            print("WARNING: No Convergence @NREP,NFREQ,N\nRestarting the Process\n")
        else:
            break
            
        i += 1

    # Saving viscosity found in new list
    visc_list_2.append(visc_list_1[-1])
    print("PROCESS COMPLETE! Nrep = {NREP}\nViscosity = {visc}\nAssociated File: {current_file}\n".format(NREP = NREP, visc = visc_list_2[-1], current_file = current_file))

    ## 2° Step

    # Mind that NREP & NFREQ are already memorized in variables, we can simply start a new set of sims without defining again these variables

    print("STARTING N CHECK ROUTINE")
    cov_list = []
    N_list = []
    previous_file = current_file

    while True:
        simulation = Launcher_local(rc, rcD, s, a, DT, sigma, neql, N*NFREQ, nrunmsd, NFREQ, NREP)
        simulation.generateFiles("N_in.Sh")
        current_file,ran_code = simulation.currentFile()
        print("Simulation Launch -> {current_file}\nNFREQ = {NFREQ}\nNREP = {NREP}\nN = {N}\n".format(current_file = current_file, NFREQ = NFREQ, NREP = NREP, N = N))
        simulation.launchSims()

        # Try/Except to ignore the TypeError that would stop the iteration without a convergence
        cov_tmp = simulation.checkN()
        cov_list.append(cov_tmp)
        print("COV value found: {COV}".format(COV = cov_list[-1]))

        # Try/Except to ignore the TypeError that would stop the iteration without a convergence
        try:
            visc_plateau, Nrep, flag_plateau = simulation.checkNrep(WINDOW,ERR_REL,JUMP_INDEX)
            visc_list_1.append(visc_plateau)
            print("Viscosity value found: {viscosity}".format(viscosity = visc_list_1[-1]))
        except TypeError:
            pass
        
        # Writing results file
        with open("results_{ran_code}.txt".format(ran_code = ran_code), "w") as res:

            res.write(
                "# Results\n\n\n"

                "filename: {file}\n\n"
                "NFREQ = {NFREQ}\n"
                "NREP = {NREP}\n"
                "N = {N}\n"
                "DT = {DT}\n\n"

                "Viscosity: {visc}\n".format(file = current_file, NFREQ = NFREQ, NREP = NREP, N = N, DT = DT, visc = visc_plateau)
            )

        # Generate Directory & move files inside
        subprocess.run("mkdir {ran_code}; mv {current_file} time_cor.txt_{ran_code} log.cite log.lammps results_{ran_code}.txt dpd_fluid_{ran_code}.restart0 dpd_fluid_{ran_code}.restart1 tmp.rdf video.lammpstrj {ran_code}".format(ran_code = ran_code, current_file = current_file),shell=True)

        # Incremento di N a Nrep & Nfreq costante

        try:
            if abs(cov_list[-1]-cov_list[-2]) < 1.0e-2:
                print("\nFOUND VALUE OF N: ",N,"FINAL FILE: ",current_file)
                break
        except:
            pass
        
        N += 100

    ## Schmidt Number

    # v_fitslope
    from v_fitslope_extr import v_fits
    diff = v_fits("{ran_code}/log.lammps".format(ran_code = ran_code))
    print("\nDiffusivity: {mean_fit}".format(mean_fit = diff))

    schmidt_number = visc_list_2[-1]/diff/RHO
    print("Schmidt Number ({file}): {sch}".format(file = current_file, sch = schmidt_number))

    # Effective Friction Factor

    from gamma_eff import *
    g_eff = gamma_eff("{ran_code}/tmp.rdf".format(ran_code = ran_code), 50, sigma, rcD, s)

    # File extraction & generation

    print("\n\nPROCESS ENDED\nGENERATING RESULTS FILE - results_{ran_code}.txt".format(ran_code = ran_code))

    with open("results_{ran_code}.txt".format(ran_code = ran_code), "w") as res:

        res.write(
            "# Results\n\n\n"

            "filename: {file}\n\n"
            "NFREQ = {NFREQ}\n"
            "NREP = {NREP}\n"
            "N = {N}\n"
            "DT = {DT}\n\n"

            "Viscosity: {visc}\n"
            "Diffusivity: {diff}\n"
            "Schmidt Number: {sch}\n\n"

            "Effective Friction Factor: {gamma_eff}\n".format(file = current_file, NFREQ = NFREQ, NREP = NREP, N = N, DT = DT, visc = visc_list_2[-1], diff = diff, sch = schmidt_number, gamma_eff = g_eff)
        )

    # Checking if final_viscosity is reached

    if abs(visc_list_2[-1] - visc_list_2[-2])/visc_list_2[-1] < 5.0e-2:
        print("\nFinal dt found = {dt}\nFinal Viscosity = {visc}\n".format(dt = DT, visc = visc_list_2[-1]))
        break
    else:
        print("\nDecreasing the value of dt by 2.0e-3 & restarting the checking routine\nLast Simulaton: ", current_file)
        if DT == 0:
            print("\nERROR! dt can't be = 0\nLast Processed File: {file}".format(file = current_file))
            break
        DT -= 1/3*DT
