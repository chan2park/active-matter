# Unwrapped coords => Indentation plot input (.npz) & d_cont(t) plot 

import numpy as np
import pandas as pd
import variable as var
import matplotlib.pyplot as plt
from datetime import datetime

### rcParams (Global) Settings ###
SMALL = 12
MEDIUM = 15
LARGE = 20
DPI = 200
PAD = 0.5
MARGIN = 0.01

plt.rcParams['font.size']           = SMALL     # default text
plt.rcParams['axes.titlesize']      = LARGE     # title
plt.rcParams['axes.labelsize']      = MEDIUM    # x & y axis labels
plt.rcParams['xtick.labelsize']     = SMALL     # x tick labels
plt.rcParams['ytick.labelsize']     = SMALL     # y tick labels
plt.rcParams['legend.fontsize']     = SMALL     # legend

plt.rcParams['axes.xmargin']        = MARGIN    # Margin at upper & lower limit values
plt.rcParams['axes.ymargin']        = MARGIN

plt.rcParams['savefig.dpi']         = DPI
plt.rcParams['savefig.transparent'] = True

plt.rcParams['font.family']         = 'serif'

plt.rcParams['lines.marker']        = '.'
#plt.rcParams['lines.markersize']    = 10
plt.rcParams['lines.markersize']    = 1

plt.rcParams['errorbar.capsize']    = 3

plt.rcParams['figure.figsize']      = (8.0, 4.8)

#plt.rcParams['legend.framealpha']   = 0.0       # transparency of the legend => box edge...?
#plt.rcParams['legend.edgecolor']    = 'black'

#colors = ['lightsalmon', 'navajowhite', 'palegreen']  # 3 states
colors = ['C6','C3','C1','C8','C2','C9','C0','C4','C5','C7']  # cycles colors rearranged

cont_arr = np.array(var.cont_list)

for j in var.seed:

    ### indentation plot input ###
    d_mean_arr = np.array([])
    d_err_arr = np.array([])
    x_mean_arr = np.array([])     # reset for each seed
    x_err_arr = np.array([])

    ### d_cont(t) plot ###
    fig, ax = plt.subplots()
    
    id = 0
    for i in var.cont_list:
        
        ### loading data ###
        unwrap = np.load(f"{var.parent}/{var.main}/post/unwrap_cont{i}_seed{j}.npz")
        xy_unwrap_cont1 = unwrap['cont1']
        xy_unwrap_cont2 = unwrap['cont2']
        t_dimless = unwrap['t_dimless']
        disp = xy_unwrap_cont2 - xy_unwrap_cont1        # (2nd - 1st) displacement

        ### d_cont(t) plot ###
        d_cont = np.sqrt(np.sum(disp**2, axis=1))       # (2nd ~ 1st) distance
        d_dimless = d_cont / d_cont[0]                  # d_cont / d_init
        cont_label = r"$K_{cont} = $" + str(i)
        ax.plot(t_dimless, d_dimless, label=cont_label, color=colors[id])
       
        ### d_cont sampling ###
        d_sample = d_dimless[-var.N_sample:]            # sampling
        d_mean = np.mean(d_sample)  	                # averaging
        d_err = np.std(d_sample)
        d_mean_arr = np.append(d_mean_arr, d_mean)
        d_err_arr = np.append(d_err_arr, d_err)

        ### x sampling ###
        x = np.tile(d_cont[0], len(d_cont)) - d_cont    # x = d_init - d_cont
        x_sample = x[-var.N_sample:]                    # sampling
        x_mean = np.mean(x_sample)  	                # averaging
        x_err = np.std(x_sample)
        x_mean_arr = np.append(x_mean_arr, x_mean)
        x_err_arr = np.append(x_err_arr, x_err)

        id += 1

    ### indentation plot input ###
    np.savez(f"{var.parent}/{var.main}/post/xyz_savez_seed{j}", Kcont=cont_arr, 
             x=x_mean_arr, x_err=x_err_arr, d=d_mean_arr, d_err=d_err_arr)
    print(f"Seed #{j} indentation plot input is saved!")

    ### d_cont(t) plot ###
    ax.set_xlim(0, 30)
    ax.set_ylim(0, 1.2)                                 # if Pe is large, then maybe dist_dimless > 1.0 
    #ax.legend(bbox_to_anchor=(1,0.5), loc='center left')
    ax.legend(bbox_to_anchor=(1,1), loc='upper left')
    ax.set_xlabel(r"$t / t_{box}$")
    ax.set_ylabel(r"$d_{cont} / d_{init}$")
    ax.set_title(f"Pe = {var.Pe}, Seed #{j}")
    
    fig.tight_layout(pad=PAD)
    
    today = datetime.today().strftime("%y%m%d")
    fig.savefig(f"{var.parent}/{var.main}/post/d_cont_seed{j}_{today}.png")
