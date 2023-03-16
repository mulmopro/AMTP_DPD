import numpy as np

def cum_integral(timestep, pxy, pxz, pyz,K):

    data_storage = [pxy,pxz,pyz]

    cum_int_storage0, cum_int_storage1, cum_int_storage2 = [], [], []

    for j in range(0,len(data_storage),1):

        current_ev_data = data_storage[j]

        for i in range(0,len(timestep),1):

            single_cum_int_value = np.trapz(current_ev_data[0:i],timestep[0:i])

            if j == 0:
                cum_int_storage0.append(single_cum_int_value)
            if j == 1:
                cum_int_storage1.append(single_cum_int_value)
            if j == 2:
                cum_int_storage2.append(single_cum_int_value)

    funz_int_cum = __funzCum(K,cum_int_storage0,cum_int_storage1,cum_int_storage2,timestep)

    return funz_int_cum

def K(kb,Nev,V,dt,return_value='y'):

    T = 1/kb
    K_value = 1/(kb*T)*V*Nev*dt
    
    if return_value == 'y':
        print("Current K value: {K}\n".format(K = K_value))
    else:
        pass

    return K_value


def __funzCum(K,cum_int_storage0,cum_int_storage1,cum_int_storage2,timestep):

    # Private Method

    viscosity_cum = []

    for i in range(0,len(timestep)):
        val_temp = (cum_int_storage0[i] + cum_int_storage1[i] + cum_int_storage2[i])/3*K
        viscosity_cum.append(val_temp)

    return viscosity_cum
