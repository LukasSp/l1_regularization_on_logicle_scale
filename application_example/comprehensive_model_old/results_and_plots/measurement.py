import amici
import petab
import pypesto
import pypesto.visualize
import matplotlib.pyplot as plt
import numpy as np

import save_functions
from save_functions import save_optimization_to_file

import visualize
from LogicleScale import logicleInverseTransform, logicleTransform
import LogicleScale

# IMPORT MODEL__________________________________________________________________________________________________________

folder_base = "/Users/lukas.spoegler/PycharmProjects/CrausteModel_full/models/"

model_name = "Crauste_full_linear"

petab_problem = petab.Problem.from_folder(folder_base + model_name)

petab_problem.model_name = 'Crauste_full_linear'

importer = pypesto.PetabImporter(petab_problem)
importer.compile_model()


def calc_simulation(df, petab_problem, start, end):
    measurement = petab_problem.measurement_df['measurement'][start:end]
    sim_timepoints = petab_problem.measurement_df['time'][start:end]
    noise = petab_problem.measurement_df['noiseParameters'][start:end]
    sim_values = []
    for i in range(0, len(df)):
        sim_values.append(df[i]['measurement'][start:end])

    return [measurement, sim_values, sim_timepoints, noise]


def plot_simulation(measurement, time, sim_list, noise, labels, title, ax=None, color=None):

    # plt.plot(time, measurement, '-o', label='measurement')

    # calculate log10 noise value
    # print('noise bevore', noise)
    noise_log10 = 1/np.log(10) * noise/measurement
    # print('noise', noise_log10)

    if color is None:
        color = 'blue'

    ax.errorbar(time, measurement, yerr=noise, fmt='o', capsize=4, label='measurement', color='black')

def sim_crauste(importer, petab_problem, objective, parameter_dict, measurement=None):

    par_values = list(parameter_dict.values())
    par_names = list(parameter_dict.keys())

    # calculate df for every simulation parameter
    df = []
    for i in range(0, len(parameter_dict)):
        rdatas = objective(par_values[i], return_dict=True)['rdatas']
        df_temp = importer.rdatas_to_measurement_df(rdatas)
        df.append(df_temp)

    fig, axs = plt.subplots(nrows=2, ncols=2, constrained_layout=True, sharex='col', figsize=(7,6))


    i = 0
    print(axs.flatten())
    for ax in axs.flatten():

        ax.set_yscale('log')
        ax.set_xticks([4,6,7,8,13,15,22,28])


        if i==0:
            m, x, t, noise = calc_simulation(df, petab_problem, 0, 2)
            plot_simulation(m, t, x, noise, par_names, 'NAIVE T-CELLS', axs.flatten()[0])
            ax.set_title('NAIVE T-CELLS', fontsize=14)
            ax.set_ylabel('no. of cells', fontsize=14)
            ax.text(-0.1, 1.05, 'A', transform=ax.transAxes, size=20, weight='bold')

        if i == 1:
            m, x, t, noise = calc_simulation(df, petab_problem, 2, 9)
            plot_simulation(m, t, x, noise, par_names, 'EARLY EFFECTOR T-CELLS', axs.flatten()[1], 'goldenrod')
            ax.set_title('EARLY EFFECTOR T-CELLS', fontsize=14)
            ax.text(-0.1, 1.05, 'B', transform=ax.transAxes, size=20, weight='bold')

        if i == 2:
            m, x, t, noise = calc_simulation(df, petab_problem, 9, 16)
            plot_simulation(m, t, x, noise, par_names, 'LATE EFFECTOR T-CELLS', axs.flatten()[2], 'red')
            ax.set_title('LATE EFFECTOR T-CELLS', fontsize=14)
            ax.set_xlabel('time (days)', fontsize=14)
            ax.set_ylabel('no. of cells', fontsize=14)
            ax.text(-0.1, 1.05, 'C', transform=ax.transAxes, size=20, weight='bold')

        if i == 3:
            m, x, t, noise = calc_simulation(df, petab_problem, 16, 21)
            plot_simulation(m, t, x, noise, par_names, 'MEMORY T-CELLS', axs.flatten()[3], 'green')
            ax.set_title('MEMORY T-CELLS', fontsize=14)
            ax.set_xlabel('time (days)', fontsize=14)
            ax.text(-0.1, 1.05, 'D', transform=ax.transAxes, size=20, weight='bold')

        i+=1

    plt.show()
    fig.savefig('measurement.eps', format='eps', dpi=1200)

obj = 0
par_dict = {}

sim_crauste(importer=importer, petab_problem=petab_problem, objective=obj, parameter_dict=par_dict)
