import amici
import petab
import pypesto
import pypesto.visualize
import matplotlib.pyplot as plt
import numpy as np
from import_functions import import_modelSelection_results

import save_functions
from save_functions import save_optimization_to_file

import visualize
from LogicleScale import logicleInverseTransform, logicleTransform, logicleInverseGradient
import LogicleScale

# IMPORT MODEL__________________________________________________________________________________________________________

folder_base = "/Users/lukas.spoegler/PycharmProjects/crauste/comprehensive_model/models/"

model_name = "Crauste_full_linear"

petab_problem = petab.Problem.from_folder(folder_base + model_name)

petab_problem.model_name = 'Crauste_full_linear'

importer = pypesto.PetabImporter(petab_problem)
importer.compile_model()

model = importer.create_model()

print("Model parameters:", list(model.getParameterIds()), '\n')
print('Optimization parameters:', petab_problem.get_optimization_to_simulation_parameter_mapping(), '\n')
print("Model outputs:   ", list(model.getObservableIds()), '\n')
print("Model states:    ", list(model.getStateIds()), '\n')

print('sigmas', petab_problem.get_sigmas())

# SOLVER OPTIONS _______________________________________________________________________________________________________

solver = importer.create_solver(model)
# solver = model.getSolver(atol=1e-10, rtol=1e-10)

# play with the tolerance
solver.setRelativeTolerance(rtol=1e-10)
solver.setAbsoluteTolerance(atol=1e-10)

# enable sensitivities
solver.setSensitivityOrder(amici.SensitivityOrder_first)       # First-order ...
solver.setSensitivityMethod(amici.SensitivityMethod_forward)   # ... forward sensitivities
model.requireSensitivitiesForAllParameters()                   # ... w.r.t. all parameters

# CREATE OBJECTIVE FUNCTION_____________________________________________________________________________________________

obj_lin = importer.create_objective(solver=solver)

# logicle parameter
T = 1
end_lin = 1e-5
logicle_obj = LogicleScale.LogicleObject(T=T, end_lin=end_lin)
f = lambda x: obj_lin.get_fval(logicleInverseTransform(par=x, logicle_object=logicle_obj))
g = lambda x: obj_lin.get_grad(logicleInverseTransform(x, logicle_obj)) * logicleInverseGradient(x, logicle_obj)
obj_logicle = pypesto.Objective(fun=f, grad=g) #, hess=h)


# MODEL SELECTION ______________________________________________________________________________________________________

def import_stuff(file_name):
    import_opt = import_modelSelection_results(file_name)
    lambdas = import_opt['lambdas'][~np.isnan(import_opt['lambdas'])]
    sigma = import_opt['sigma'][0]
    par_names_temp = import_opt['par_names']
    par_names_index = [i for i, y in enumerate(par_names_temp) if y is not np.nan]
    par_names = par_names_temp[par_names_index]
    conv_points = import_opt['conv_points'][:len(lambdas)]
    n_starts = import_opt['n_starts'][0]
    options = import_opt['options'][0]

    print(options)

    reg_path_temp = import_opt['reg_path']
    reg_path =[]
    z = 0
    for i in range(0, len(par_names)):
        temp = []
        for j in range(0, len(lambdas)):
            temp.append(reg_path_temp[z+j])
        reg_path.append(temp)
        z += len(lambdas)

    return [reg_path, lambdas, par_names, conv_points]


file_name = ['logicle5_1']

obj_list = [obj_logicle]

threshold_linear = 1e-10
threshold_logicle = logicleTransform([threshold_linear], T=1, end_lin=1e-5)[0]
# threshold_logE = np.log10(1+threshold_linear)
threshold_list = [threshold_logicle] #, threshold_logE, threshold_linear]

#par_linear = visualize.get_opt_par_list(100, path='modelSelection/linear/')
par_logicle = visualize.get_opt_par_list(200, path='modelSelection/logicle5_1/')
#par_logE = visualize.get_opt_par_list(100, path='modelSelection/logE_1/')
par_list = [par_logicle]

reg_path_list = []
lambdas_list = []
par_names_list = []
conv_list = []
ms_list = []

for j in range(0, len(file_name)):

    path = 'modelSelection/' + file_name[j] + '/200,5000'
    reg_path, lambdas, par_names, conv_points = import_stuff(path)


    reg_path_list.append(reg_path)
    lambdas_list.append(lambdas)
    par_names_list.append(par_names)
    conv_list.append(conv_points)

    # [aic, min_lambda, bic, min_lambda_bic]
    c = visualize.plot_aic_test1(reg_path=reg_path,
                                 obj=obj_list[j],
                                 lambdas=lambdas,
                                 opt_par=par_list[j],
                                 threshold=threshold_list[j],
                                 n_data=21)
    ms_list.append(c)


# convergence
# for a in range(0, 1):
  #  plt.plot(lambdas_list[a], np.array(conv_list[a])/1000, label=str(a))
#plt.legend()
#plt.show()

import visualize_caro
import visualize


# visualize.regularization_path(reg_path=reg_path, lambdas=lambdas, parameter_names=par_names, n_sigma=0)

print(min(ms_list[0][0]))
print(ms_list[0][1])
print(lambdas_list[0][85])

labels = ['logicle']

print(par_names_list)


fig = plt.figure(figsize=(10, 7))

gs = fig.add_gridspec(2,2)
ax1 = fig.add_subplot(gs[:, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax4 = fig.add_subplot(gs[1, 1])

visualize.bar_plot(reg_path_list[0], lambdas_list[0], threshold_list[0], par_names_list[0], ms_list[0][1], ax1)
# ax1.set_title('logicle', fontsize=12) #, weight='bold')
interval = np.abs(lambdas_list[0][0]-lambdas_list[0][0])
# ax1.vlines(1.2160804 - lambdas_list[0][0] + interval/2, -1, 21, color='green', linestyles='dashed')

ax1.text(-0.08, 1.03, 'A', transform=ax1.transAxes, size=20, weight='bold')
ax1.set_xlabel('$\log_{10}(\lambda)$', fontsize=12)
ax1.set_ylabel('parameter name', fontsize=12)
ax1.set_xlim(0, 14)
ax1.set_ylim((-0.5, len(par_names_list[0])- 0.5))
ax1.set_xticks([0, 2, 4, 6, 8, 10, 12, 14])
ax1.set_yticks(np.arange(0, 21, step=1))
ax1.set_xticklabels([-8, -6, -4, -2, 0, 2, 4, 6])#, fontsize=12)
ax1.set_yticklabels(par_names_list[0][::-1])#, fontsize=12)

for j in range(0, 9):
    ax1.get_yticklabels()[j].set_color('red')

visualize.number_of_reactions(reg_path_list[0], lambdas_list[0], ax2, threshold_list[0], opt_lambda=ms_list[0][1])
# ax2.set_title('logicle', fontsize=12) #, weight='bold')
ax2.text(-0.08, 1.03, 'B', transform=ax2.transAxes, size=20, weight='bold')
# ax2.set_xlabel('$\log_{10}(\lambda)$') # , fontsize=12)
ax2.set_xlim(-8, 6)
ax2.set_ylabel('no. of non-zero parameter')
ax2.set_ylim(0, 21.5)
ax2.set_xticklabels('')

visualize.plot_aic_crauste(ms_list[0][0], lambdas_list[0], ms_list[0][1], ax4, label='AIC')
visualize.plot_bic(ms_list[0][2], lambdas_list[0], ms_list[0][3], ax4, label='BIC')
ax4.text(-0.08, 1.03, 'C', transform=ax4.transAxes, size=20, weight='bold')
ax4.set_yscale('log')
ax4.set_xlabel('$\log_{10}(\lambda)$')# , fontsize=12)
ax4.set_ylabel('AIC/BIC') #, fontsize=12)
ax4.set_xlim(-8, 6)
ax4.legend(loc='upper center')

plt.show()

# fig.savefig('modelselection.eps', format='eps', dpi=1000)
fig.savefig('modelselection.png', format='png')

print(par_names_list)