import sys

parent      = "/nas/qcd5776/lammps/active_matter/2.const_cont_force"
main        = "2.Pe_0"
cont_list   = [5,10,25,50,75,100,200,500,1000]  # only the systems at steady state
seed        = [1,2,3,4,5]

#cont_list   = [5,10,25]  # only the systems at steady state
#seed        = [1,2]

SAMPLE      = 2.5  # How much t_box will be sampled from the last

cont1       = 1   # contractive bead indices
cont2       = 201 
Pe          = 0.0

T           = 1.0
Lfil        = 10.0
damp        = 1.0
step_cpt    = 1e5
Lbead       = 1.0
Lbox        = 300.0 

### INDUCED VARIABLES ###
F_act       = Pe * T / Lfil ** 2
v_act       = damp * F_act

if v_act <= 1:
    v_act = 1

t_cpt       = Lbead / v_act
dt          = t_cpt / step_cpt
t_box       = Lbox / v_act

t_sample    = SAMPLE * t_box
N_sample    = int(t_sample / t_cpt)

### ARGUMENTS ###
#if len(sys.argv) == 4:
#    cont1 = int(sys.argv[1])  # contractive bead index
#    cont2 = int(sys.argv[2])  # ex) 1, 201
#    Pe = float(sys.argv[3])  # Peclet number
#else:
#    print("\nArguments:")
#    print("\tcontractive bead index 1, index 2, Pe")
#    print("Example: ")
#    print("\tpython3 d_cont.py 1 201 0\n")
#    quit()
