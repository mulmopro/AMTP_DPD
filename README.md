# Automated-Method-to-compute-Transport-Properties-from-DPD-equilibrium-simulations
Motivations and Application
The code implements an automated reliable method to compute transport properties from DPD equilibrium simulations performed with LAMMPS. It was thought to assess the Green-Kubo approach realibility and computational feasibility for the calculation of the zero-shear viscosity in DPD simulations. It is based on an iterative algorithm that automatically finds:

1) the parameter of the approximated algorithm adopted by LAMMPS for the calculation of the SACF with the shortest trajectory giving the fixed statistical accuracy

2) the viscosity value that is independent on the choice of time step for a given DPD system

Workflow description

Technical informations


