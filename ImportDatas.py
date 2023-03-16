import pandas as pd

# Import Datas              ## Optimized Version 2.0

def importdatas(path_to_file,Nrep):

    data = pd.read_csv(path_to_file, sep=" ", skiprows=4, header=None, engine='python')

    timestep = data[1].values.tolist()
    considered_timestep = timestep[-Nrep:]

    pxy = data[3].values.tolist()
    considered_pxy = pxy[-Nrep:]

    pxz = data[4].values.tolist()
    considered_pxz = pxz[-Nrep:]

    pyz = data[5].values.tolist()
    considered_pyz = pyz[-Nrep:]

    return considered_timestep, considered_pxy, considered_pxz, considered_pyz