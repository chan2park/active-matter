# lammpstrj files => unwrap contractive beads coordinates (.npz) 

import numpy as np
import pandas as pd
import variable as var
import time

def param_collect(trjfile):
    """ 
    Collecting Natoms, Nline_frame, Nframes 
    The input format must be '.lammpstrj'
    """

    #start = time.time()
    f = open(trjfile, 'r')
    
    for l in range(4):
        line = f.readline()
    Natoms = int(line)  		    # 4th row
    Nline_frame = Natoms + 9  	            # line number for each frame

    data = f.read()
    Nframes = data.count('TIMESTEP') + 1    # also counting the 1st one
    # Faster method than 'readlines' or 'enumerate' func. methods
    
    f.close()
    #end = time.time()
    #print("{} sec elapsed for parameter collecting".format(end - start))

    return Natoms, Nline_frame, Nframes
 
def skip_header(Nline_frame, Nframes):
    """ Skipping the header part for each frame (9 rows) """

    skip = []
    for k in range(Nframes):
        skip = skip + list(range(Nline_frame*k, Nline_frame*k+9)) # skipped row indices

    return skip

def unwrap_cont_coords(trjfile, skip, var):
    """ Extract contractive beads coordinates and unwrap them """

    dataframe = pd.read_csv(trjfile, sep=r"\s+", skiprows=skip, header=None)
    data = dataframe.to_numpy(dtype=None)
    
    data_cont1 = data[data[:,0] == var.cont1, :]    # 1st contractive bead
    xy_cont1 = data_cont1[:,2:4]                    # x, y coordinates
    ixiy_cont1 = data_cont1[:,5:7]                  # periodic box indices
    xy_unwrap_cont1 = xy_cont1 + ixiy_cont1 * var.Lbox # unwrapped coordinates
    
    data_cont2 = data[data[:,0] == var.cont2, :]    # 2nd contractive bead
    xy_cont2 = data_cont2[:,2:4]
    ixiy_cont2 = data_cont2[:,5:7]
    xy_unwrap_cont2 = xy_cont2 + ixiy_cont2 * var.Lbox

    return xy_unwrap_cont1, xy_unwrap_cont2
    
### LOOP FOR EACH SYSTEM ###

for j in var.seed:
    
    for i in var.cont_list:
        
        #trjfile = '../cont_' + str(i) + '/seed' + str(j) + '/prod.lammpstrj'
        trjfile = f"{var.parent}/{var.main}/cont_{i}/seed{j}/prod.lammpstrj"

        Natoms, Nline_frame, Nframes = param_collect(trjfile)
        
        skip = skip_header(Nline_frame, Nframes)

        xy_unwrap_cont1, xy_unwrap_cont2 = unwrap_cont_coords(trjfile, skip, var)
       
        t = var.t_cpt * np.arange(Nframes)  # t axis for each simulation
        t_dimless = t / var.t_box 

        #np.savez('unwrap_cont'+str(i)+'_seed'+str(j), cont1=xy_unwrap_cont1, cont2=xy_unwrap_cont2, t_dimless=t_dimless)
        np.savez(f"{var.parent}/{var.main}/post/unwrap_cont{i}_seed{j}", cont1=xy_unwrap_cont1, cont2=xy_unwrap_cont2, t_dimless=t_dimless)
        print('Kcont = {}, Seed {} unwrapping complete!'.format(i, j))

