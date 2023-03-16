def v_fits(filename):

    string_start = "Step Temp Press c_msd[4] v_fitslope \n"

    line_flag = 0
    string_flag = 0

    with open(filename, "r") as file:
        with open("v_fitslope.txt", "w") as save:
            for line in file.readlines():

                j = 1

                if line == string_start or string_flag == 1:

                    for number in line.split():

                        if number == "Loop":
                            line_flag = 1
                            break
                        if j != 5:
                            number = number + " "
                            save.write(number)
                        if j == 5:
                            number = number + "\n"
                            save.write(number)

                        string_flag = 1
                        j += 1
                else:
                    pass
            
                if line_flag == 1:
                    break

    import pandas as pd

    save_df = pd.read_csv("v_fitslope.txt", sep=" ")
    mean_vfits = save_df["v_fitslope"][2:-4].mean()

    return mean_vfits
