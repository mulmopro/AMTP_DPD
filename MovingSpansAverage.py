
class MovingSpans:

    # Simple Moving Average

    def __init__(self, cum_int_data):

        self.cum_int_data = cum_int_data
        self.count = 1
    
    def runAve(self,window,err_rel,jump_index,printNrep="y"):

        # Moving Spans Averages

        moving_averages, val_temp = [], []
        Nrep, val_media = 1, 0

        for i in range(0,len(self.cum_int_data),1):     # (.1)

            val_temp.append(self.cum_int_data[i])

            if len(val_temp) == window:                 # Riempimento della lista con all'interno i valori dell'integrale cumulativo
                val_media = sum(val_temp)/window        # e calcolo della media dell'intervallo
                moving_averages.append(val_media)

                if len(moving_averages)>1+jump_index:   # (.2)

                    # Ciclo di controllo definito dal jump index (numero di "spazi" da saltare nella lista delle medie) e calcolo
                    # dell'errore relativo tra i due valori di media degli intervalli definiti nel ciclo (.1)

                    err_sol = abs((moving_averages[-1]-moving_averages[-2-jump_index]))/moving_averages[-1]

                    if err_sol <= err_rel:

                        # Per essere verificata la condizione di output serve che sia l'errore relativo tra due valori consecutivi di media
                        # che l'errore relativo tra gli errori relativi siano verificati

                        if printNrep == "y":
                            print("All Done!\nNrep = {Nrep}".format(Nrep = Nrep))
                        else:
                            pass
                            
                        while_flag = 1

                        return moving_averages[-1],Nrep, while_flag
                
                else:
                    pass

                val_media = []
                val_temp = []

            Nrep += 1

        print("\n\nNo Plateau - TRYING DIFFERENT VALUES\n")
        while_flag = 0
        return moving_averages[-1], Nrep, while_flag