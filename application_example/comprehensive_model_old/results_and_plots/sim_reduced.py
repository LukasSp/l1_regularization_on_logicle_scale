import amici
import petab
import pypesto
import pypesto.visualize
import matplotlib.pyplot as plt
import numpy as np

import save_functions
from save_functions import save_optimization_to_file

import visualize
from LogicleScale import logicleInverseTransform, logicleTransform, LogicleObject
import LogicleScale

# IMPORT MODEL__________________________________________________________________________________________________________

folder_base = "/Users/lukas.spoegler/PycharmProjects/CrausteModel_full/models/"
model_name = "Crauste_full_linear"
petab_problem = petab.Problem.from_folder(folder_base + model_name)
petab_problem.model_name = 'Crauste_full_linear'
importer = pypesto.PetabImporter(petab_problem)
importer.compile_model()
model = importer.create_model()

timepoints = np.linspace(2, 30, 100)
# timepoints = [4, 6, 8, 10, 12, 14, 16, 18, 20, 22]
model.setTimepoints(timepoints)

solver = importer.create_solver(model)
solver.setRelativeTolerance(rtol=1e-10)
# solver.setAbsoluteTolerance(atol=1e-10)
solver.setSensitivityOrder(amici.SensitivityOrder_first)       # First-order ...
solver.setSensitivityMethod(amici.SensitivityMethod_forward)   # ... forward sensitivities
model.requireSensitivitiesForAllParameters()                   # ... w.r.t. all parameters

obj = importer.create_objective(solver=solver)


best_par_paper = [0.59, 0.025, 0.009, 21.5e-6, 3.6e-8, 7.5e-6,
                  0.75, 5.5e-2, 1.8e-7, 1.8e-5, 0.64, 0.15,
                  0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 1, 1, 1]

best_par_log = 10**np.array([ -0.07426949, -1.5424396, -1.71845154, -4.79418012, -10., -5.23332452, -0.12601026,
                              -4.99988123, -9.99999998, -4.55638098, -0.30898867, -0.90503462, -10., -6.96050283,
                              -8.54550995, -10., -0.80136887, -10., -8.31990936, -4.27926881, -4.63058586, 0, 0, 0, 0])

logicle_obj = LogicleObject(T=100, end_lin=1e-5)
best_par_logicle = logicleInverseTransform([0.73294927, 0.54583766, 0.52801805, 0.13235649, 0., 0.03449152, 0.71937865,
                                            0.00973187, 0.09015665, 0.05718341, 0.68776811, 0.62018734, 0.27800834,
                                            0.08857416 ,0.27061034, 0.24731772, 0.63725277, 0., 0.0983246 , 0.00224438,
                                            0.054455, 1, 1, 1, 1], logicle_obj)

logicle_obj = LogicleObject(T=100, end_lin=1e-5)
best_par_red = logicleInverseTransform([0.71403861, 0.53124423, 0.49639239, 0.07264355, 0, 0.04018985, 0.7201659, 0,
                                        0.0019951 , 0.12294839, 0.7012356,  0.61790586,0,0,0,0,0.56526125, 0,0,0,0,1, 1, 1, 1], logicle_obj)

best_par_red = 10**np.array([-0.11508453 ,-1.59008064 ,-1.71610071, -4.63725562,-100, -5.22995268, -0.10316299,-100,
 -7.09262244, -4.62050801, -0.31441241, -0.90634609,-100,-100,-100,-100, -0.77518533,-100,-100,-100,-100,0,0,0,0])

par_dict = {'nominal $(\mathcal{M}_{crauste})$': best_par_paper,
            #'$\log_{10}$ $(\mathcal{M}_{com})$': best_par_log,
            'logicle $(\mathcal{M}_{com})$': best_par_logicle,
            #'logicle $(\mathcal{M}^*)$': best_par_red}
            '$\log_{10}$ $(\mathcal{M}^*)$': best_par_red}
            #'$\log(k+10^{-5})$ $(\mathcal{M}_{com})$': best_par_logE}#,  #,
            #'aic': best_par_logE_aic,
            #'aicc': best_par_logE_aicc}#,
            #'bic': best_par_logE_bic}


#_______________________________________________________________________________________________________________________

par_values = list(par_dict.values())
par_names = list(par_dict.keys())

rdata = []
rdata_par = []
for i in range(len(par_dict)):
    model.setParameters(amici.DoubleVector(par_values[i]))
    rdata_tmp = amici.runAmiciSimulation(model, solver)['y']
    # print('iiiiiii', i)
    # print(rdata_tmp)

    naive = [item[0] for item in rdata_tmp]
    ee = [item[1] for item in rdata_tmp]
    le = [item[2] for item in rdata_tmp]
    memory = [item[3] for item in rdata_tmp]

    rdata.append([naive, ee, le, memory])


se = [[0, 2], [2, 9], [9, 16], [16, 21]]
color = ['green', 'red', 'gold']
k = ['A', 'B', 'C', 'D']
title = ['NAIVE T-CELLS', 'EARLY EFFECTOR T-CELLS', 'LATE EFFECTOR T-CELLS','MEMORY T-CELLS']
l = []

fig, axs = plt.subplots(nrows=2, ncols=2, constrained_layout=True, sharex='col', figsize=(9, 7))
a = 0
for ax in axs.flatten():
    time = petab_problem.measurement_df['time'][se[a][0]:se[a][1]]
    measurement = petab_problem.measurement_df['measurement'][se[a][0]:se[a][1]]
    noise = petab_problem.measurement_df['noiseParameters'][se[a][0]:se[a][1]]
    ax.errorbar(time, measurement, yerr=noise, fmt='o', capsize=4, label='measurement', color='black')
    if a == 0:
        ax.set_ylim(1, 10000)
    if a==1:
       ax.set_ylim(1, 1000000)
    if a == 3:
        ax.set_ylim(bottom=1, top=100000)
    a+=1

for i in range(0, len(par_dict)):
    j = 0       
    for ax in axs.flatten():
        ax.plot(timepoints, rdata[i][j], label=par_names[i], color=color[i])
        ax.set_title(title[j])
        ax.text(-0.1, 1.05, k[j], transform=ax.transAxes, size=22, weight='bold')
        ax.set_yscale('log')
        ax.set_xticks([0, 5, 10, 15, 20, 25,30])
        j += 1
j = 0
for ax in axs.flatten():
    if j == 0 or j == 2:
        ax.set_ylabel('no. of cells', fontsize=14)
    if j == 2 or j == 3:
        ax.set_xlabel('time [days]', fontsize=14)
    j+=1
    ax.set_xlim(1, timepoints[-1])
     # ax.set_xticks([4, 6, 7, 8, 13, 15, 22, 28])

par_names.append('measurement')

fig.legend(labels=par_names, loc=5, fontsize=11)
fig.tight_layout()
fig.subplots_adjust(right=0.75)

plt.show()

fig.savefig('sim_true_com.eps', format='eps', dpi=1200)

plt.show()
