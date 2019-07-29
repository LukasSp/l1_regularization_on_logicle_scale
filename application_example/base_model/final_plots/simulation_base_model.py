"""
    Simulate all 4 observables for different parameters.
    We simulate in the linear scale
"""
import amici
import petab
import pypesto
import pypesto.visualize
import matplotlib.pyplot as plt
import numpy as np


import LogicleScale
from LogicleScale import logicleInverseTransform, logicleTransform, LogicleObject


# IMPORT LINEAR MODEL___________________________________________________________________________________________________

folder_base = '/Users/lukas.spoegler/PycharmProjects/crauste/base_model/models/'
model_name = "Crauste_CellSystems2017_linear"
petab_problem = petab.Problem.from_folder(folder_base + model_name)
petab_problem.model_name = "Crauste_CellSystems2017_linear"
importer = pypesto.PetabImporter(petab_problem)
importer.compile_model()
model = importer.create_model()

# simulation timepoints
timepoints = np.linspace(2, 30, 100)
model.setTimepoints(timepoints)

solver = importer.create_solver(model)
solver.setRelativeTolerance(rtol=1e-10)
solver.setAbsoluteTolerance(atol=1e-10)
solver.setSensitivityOrder(amici.SensitivityOrder_first)       # First-order ...
solver.setSensitivityMethod(amici.SensitivityMethod_forward)   # ... forward sensitivities
model.requireSensitivitiesForAllParameters()                   # ... w.r.t. all parameters

obj = importer.create_objective(solver=solver)

# DEFINE SIMULATION PARAMETER __________________________________________________________________________________________

# best parameter from crauste et al
best_par_paper = [0.59, 0.025, 0.009, 21.5e-6, 3.6e-8, 7.5e-6,
                  0.75, 5.5e-2, 1.8e-7, 1.8e-5, 0.64, 0.15, 1, 1, 1, 1]

# optimal log10 parameter
best_par_log = 10**np.array([-0.2390705, -1.59656206, -1.92944291, -4.61622465, -9.99597055, -5.12195751,
                             -0.1410224,  -4.80272898, -10., -4.70446442, -0.26370535, -0.91631592, 0, 0, 0, 0])

# optimal logicle parameter
logicle_obj = LogicleObject(T=100, end_lin=1e-6)
best_par_logicle = logicleInverseTransform([0.74506269, 0.58513538, 0.53479985, 0.17364882, 0., 0.16668271, 0.75314595,
                                            0.49857313, 0.,0.21001242, 0.74363556, 0.66104223, 1, 1, 1, 1], logicle_obj)

# optimal log10 + 1e-5 parameter
best_par_logE_E = 10**np.array([-0.2212495,  -1.55911411 , -1.99446709 , -4.66316381 ,-5., -4.76937694,
                                -0.12450302, -4.99997509, -4.97341095, -4.60686091, -0.22922818,
                                -0.92992495, 0, 0, 0, 0]) - 1e-5

par_dict = {'nominal': best_par_paper,
            '$\log_{10}$': best_par_log,
            'logicle': best_par_logicle,
            '$\log_{10}(\\theta+10^{-5}$)': best_par_logE_E}


# PLOT _________________________________________________________________________________________________________________

par_values = list(par_dict.values())
par_names = list(par_dict.keys())

rdata = []
rdata_par = []
for i in range(len(par_dict)):
    model.setParameters(amici.DoubleVector(par_values[i]))
    rdata_tmp = amici.runAmiciSimulation(model, solver)['y']
    print(rdata_tmp)

    naive = [item[0] for item in rdata_tmp]
    ee = [item[1] for item in rdata_tmp]
    le = [item[2] for item in rdata_tmp]
    memory = [item[3] for item in rdata_tmp]

    rdata.append([naive, ee, le, memory])


se = [[0, 2], [2, 9], [9, 16], [16, 21]]
color = ['green', 'royalblue', 'red', 'orange']
k = ['A', 'B', 'C', 'D']
title = ['NAIVE T-CELLS', 'EARLY EFFECTOR T-CELLS', 'LATE EFFECTOR T-CELLS','MEMORY T-CELLS']
l = []

fig, axs = plt.subplots(nrows=2, ncols=2, constrained_layout=True, sharex='col', figsize=(9,7))
a = 0
for ax in axs.flatten():
    time = petab_problem.measurement_df['time'][se[a][0]:se[a][1]]
    measurement = petab_problem.measurement_df['measurement'][se[a][0]:se[a][1]]
    noise = petab_problem.measurement_df['noiseParameters'][se[a][0]:se[a][1]]
    ax.errorbar(time, measurement, yerr=noise, fmt='o', capsize=4, label='measurement', color='black')
    if a ==0:
        ax.set_ylim(bottom=1, top=10000)
    if a == 1:
        ax.set_ylim(bottom=1, top=1000000)
    if a == 3:
        ax.set_ylim(bottom=1, top=100000)
    a+=1

for i in range(0, len(par_dict)):
    j = 0
    for ax in axs.flatten():
        ax.plot(timepoints, rdata[i][j], label=par_names[i], color=color[i])
        ax.set_title(title[j], fontsize=14)
        ax.text(-0.1, 1.05, k[j], transform=ax.transAxes, size=22, weight='bold')
        ax.set_yscale('log')
        j += 1
j = 0
for ax in axs.flatten():
    if j == 0 or j == 2:
        ax.set_ylabel('no. of cells', fontsize=14)
    if j == 2 or j == 3:
        ax.set_xlabel('time [days]', fontsize=14)
    j+=1
    ax.set_xlim(0, 30)
    # ax.set_xticks([4, 6, 7, 8, 13, 15, 22, 28])


par_names.append('measurement')

fig.legend(labels=par_names, loc=5, fontsize=12)
fig.tight_layout()
fig.subplots_adjust(right=0.78)

plt.show()

# fig.savefig('sim_base_model.eps', format='eps', dpi=1200)
