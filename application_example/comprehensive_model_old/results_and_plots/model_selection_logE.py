import amici
import petab
import pypesto
import pypesto.visualize
import matplotlib.pyplot as plt
import numpy as np
from import_functions import import_modelSelection_results, import_optimization_results

import save_functions
from save_functions import save_optimization_to_file

import visualize
from LogicleScale import logicleInverseTransform, logicleTransform, logicleInverseGradient
import LogicleScale

# IMPORT MODEL__________________________________________________________________________________________________________

folder_base = "/Users/lukas.spoegler/PycharmProjects/CrausteModel_full/models/"
model_name = "Crauste_full_linear"

petab_problem = petab.Problem.from_folder(folder_base + model_name)

petab_problem.model_name = 'Crauste_full_linear'

importer = pypesto.PetabImporter(petab_problem)
importer.compile_model()

model = importer.create_model()


# SOLVER OPTIONS _______________________________________________________________________________________________________

solver = importer.create_solver(model)
# solver = model.getSolver(atol=1e-10, rtol=1e-10)

# play with the tolerance
solver.setRelativeTolerance(rtol=1e-10)
# solver.setAbsoluteTolerance(atol=1e-10)

# enable sensitivities
solver.setSensitivityOrder(amici.SensitivityOrder_first)       # First-order ...
solver.setSensitivityMethod(amici.SensitivityMethod_forward)   # ... forward sensitivities
model.requireSensitivitiesForAllParameters()                   # ... w.r.t. all parameters

# CREATE LINEAR OBJECTIVE FUNCTION _____________________________________________________________________________________

obj_lin = importer.create_objective(solver=solver)

eps = 1e-5
f = lambda x: obj_lin.get_fval(10**np.array(x) - eps)
g = lambda x: obj_lin.get_grad(10**np.array(x) - eps) * 10**np.array(x)  * np.log(10)
obj = pypesto.Objective(fun=f, grad=g)


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

# calculate reg_path
def calculate_regularization_path(par_list, lambdas, n_sigma=None):

    parameter_list = []
    for i in range(0, len(par_list[0])):
        parameter = []

        for j in range(0, len(par_list)):
            parameter.append(par_list[j][i])

        # add zeros to the end for non optimized results
        j=0
        while len(par_list)+j < len(lambdas):
            parameter.append(0.0)
            j+=1

        parameter_list.append(parameter)

    return parameter_list

#______________________________________

obj_list = [obj]


scale = 'logE'
threshold_linear = 1e-7
threshold_logE = np.log10(threshold_linear+1e-5)
par_list = visualize.get_opt_par_list_logE(200, 'modelSelection/'+scale +'/')
lambdas = np.linspace(-8, 6, 200)

reg_path = calculate_regularization_path(par_list, lambdas)


reg_path_list = []
lambdas_list = []
par_names_list = []
conv_list = []
ms_list = []

import visualize_crauste

c = visualize_crauste.plot_aic_logE(reg_path=reg_path,
                                    obj=obj,
                             lambdas=lambdas,
                             opt_par=par_list,
                             threshold=threshold_logE,
                             n_data=21)


file_name = 'modelSelection/'+scale+'/result_190'
import_opt = import_optimization_results(file_name)
names = np.array(import_opt['par_names'])[:21]


# visualize.regularization_path(reg_path=reg_path, lambdas=lambdas, parameter_names=names, n_sigma=0)
visualize_crauste.barplot_logE(reg_path, lambdas, threshold_logE, names, -5, 0.5, opt_lambda= c[3])
# visualize_crauste.number_of_reactions_logE(reg_path, lambdas, threshold_logE, opt_lambda=c[3])
plt.show()


print('aicc', c[5], par_list[c[5]])
print('aic', c[1], par_list[c[1]])
print('bic', c[3], par_list[c[3]])