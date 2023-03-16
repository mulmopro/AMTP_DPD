import pandas as pd
import numpy as np

def __import_rdf(path_to_file, n_values):
    tmp_rdf = pd.read_csv(path_to_file, sep=" ", skiprows=4, header=None, names=["Row", "r_ij", "g_ij", "c_myRDF[3]"])
    # We need the last n_values
    r_ij = tmp_rdf.r_ij[-n_values:].values.tolist()
    # r_ij = r_ij[0:-7]
    g_ij = tmp_rdf.g_ij[-n_values:].values.tolist()
    # g_ij = g_ij[0:-7]

    return r_ij, g_ij

def gamma_eff(path_to_file, n_values, sigma, rcD, s):
    # Importing necessary datas
    r_ij, g_ij = __import_rdf(path_to_file, n_values)
    w = [(1-r_ij[i]/rcD)**(2*s) for i in range(len(r_ij))]

    # gamma_eff calculations
    fun = [(sigma**2)/2*w[i]*g_ij[i]*4*np.pi*(r_ij[i]**2) for i in range(len(r_ij))]
    gamma_eff = np.trapz(fun, r_ij, rcD/50)

    return gamma_eff
