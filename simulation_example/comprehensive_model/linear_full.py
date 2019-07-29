import amici
import petab
import pypesto
import pypesto.visualize
import numpy as np
import time

# import function to save/import your results
from save_functions import save_optimization_to_file, save_guesses, save_modelSelection, save_startpoints
from import_functions import import_guesses, import_startpoints

# import regularization routines
from l1_regularization_computations import compute_regularization_path, \
                                           compute_converged_points_single, \
                                           compute_converged_points, \
                                           compute_model_selection_criteria

# IMPORT MODEL__________________________________________________________________________________________________________

folder_base = "models/"
model_name = "caroModel_linear"

petab_problem = petab.Problem.from_folder(folder_base + model_name)

petab_problem.model_name = 'caroModel_linear'

importer = pypesto.PetabImporter(petab_problem)
importer.compile_model()

model = importer.create_model()

print("Model parameters:", list(model.getParameterIds()), '\n')
print('Optimization parameters:', petab_problem.get_optimization_to_simulation_parameter_mapping(), '\n')
print("Model outputs:   ", list(model.getObservableIds()), '\n')
print("Model states:    ", list(model.getStateIds()), '\n')


# SOLVER OPTIONS _______________________________________________________________________________________________________

solver = importer.create_solver(model)

# enable sensitivities
solver.setSensitivityOrder(amici.SensitivityOrder_first)       # First-order ...
solver.setSensitivityMethod(amici.SensitivityMethod_forward)   # ... forward sensitivities
model.requireSensitivitiesForAllParameters()                   # ... w.r.t. all parameters

# CREATE OBJECTIVE FUNCTION_____________________________________________________________________________________________

obj = importer.create_objective(model=model, solver=solver)

print('optimal x = ', petab_problem.x_nominal)
print('optimal lh value', obj(petab_problem.x_nominal))

# # OPTIMIZATION WITHOUT PRIOR ___________________________________________________________________________________________
#
# optimizer = pypesto.ScipyOptimizer()
# problem = importer.create_problem(obj)
# engine = pypesto.SingleCoreEngine()
# n_starts = 10
# start = time.time()
# result = pypesto.minimize(problem=problem,
#                           optimizer=optimizer,
#                           n_starts=n_starts,
#                           engine=engine)
# end = time.time()
#
# print('best parameter: ', result.optimize_result.as_list('x')[0]['x'])
# print('best likelihood value: ', obj(result.optimize_result.as_list('x')[0]['x']))
#
# # calculate computation time
# comp_time = end - start
#
# # calculate converged points
# conv_points = compute_converged_points_single(result=result)
# print('converted points: ', conv_points)
#
#
# # SAVE STARTPOINTS _____________________________________________________________________________________________________
#
# # calculate the startpoints
# startpoints = result.optimize_result.get_for_key('x0')
#
# # save the startpoints
# save_startpoints(result=result, path='startpoints/', file_name='linear')
#
# # import startpoints
# startpoints_import = import_startpoints('startpoints/linear')
#
#
# # SAVE OPTIMIZATION RESULTS ____________________________________________________________________________________________
#
# # add options
# options = 'MODEL: caro model, ' \
#           '\nSCALE: linear, ' \
#           '\nSTARTS: ' + str(n_starts) + \
#           '\nCONV POINTS: ' + str(conv_points) + \
#           '\nTIME: ' + str(comp_time)
#
# # specify path
# path = 'results_and_plots/optimization/linear/'
#
# # file name is equal to starting points
# file_name = str(n_starts)
#
# # save
# save_optimization_to_file(result=result,
#                           n_start=n_starts,
#                           nominal_par=petab_problem.x_nominal,
#                           par_names=['$\theta_1$', '$\theta_2$', '$\theta_3$', '$\sigma$'],
#                           opt_lh=obj(petab_problem.x_nominal),
#                           file_name=file_name,
#                           conv_points=conv_points,
#                           comp_time=comp_time,
#                           opt_interval=[problem.lb, problem.ub],
#                           startpoints=startpoints,
#                           options=options,
#                           path=path)
#
# # SAVE GUESSES _________________________________________________________________________________________________________
#
# # save converged points to use them as starting points for
# # the regularization
#
# path_guess = 'guesses/linear/'
#
# save_guesses(result=result,
#              n_starts=n_starts,
#              nominal_par=petab_problem.x_nominal,
#              options=options,
#              path=path_guess,
#              file_name=file_name)


# INITIALIZE L1 REGULARIZATION _________________________________________________________________________________________

import regularization

# specify inputs
n = len(model.getParameters())

# all parameters are linear
scale_list_lin = ['lin'] * n

# the noise parameter should not be penalized
estimate_list = [1, 1, 1, 0]

# the range of penalization strength
lambda_range = [1, 100]

# number of penalizations
n_lambda = 10


# initalize l1 regularization
initialize_regularization = regularization.l1_regularization(model=model,
                                                             petab_problem=petab_problem,
                                                             objective=obj,
                                                             scale_list=scale_list_lin,
                                                             estimate_list=estimate_list,
                                                             lambda_range=lambda_range,
                                                             n_lambda=n_lambda)

# DO L1 REGULARIZATION _________________________________________________________________________________________________

# specify inputs
n_starts = 10

# optimization method and options
opt_method = 'L-BFGS-B'
opt_options = {'maxiter': 1e5, 'ftol': 1e-10, 'gtol': 1e-10}

# define startpoints as the best starts of the optimization
path_guess = 'guesses/linear/1000'
x_guesses = import_guesses(path_guess)[0]

# define path for the results
path_ms = 'results_and_plots/modelSelection/linear/'

start = time.time()
res_list = initialize_regularization(n_starts=n_starts,
                                     x_guesses=x_guesses,
                                     opt_method=opt_method,
                                     opt_options=opt_options,
                                     par_names=['$\theta_1$', '$\theta_2$', '$\theta_3$'],
                                     path=path_ms)
end = time.time()


# SAVE REGULARIZATION RESULTS TO FILE __________________________________________________________________________________

# computation time
comp_time = end - start

# options
options = 'MODEL: caro model, ' \
          '\nSCALE: linear' + \
          '\n#LAMBDA: ' + str(n_lambda) + \
          '\nSTARTS: ' + str(n_starts) + \
          '\nTIME: ' + str(comp_time)

# compute regularization path
reg_path = compute_regularization_path(result_list=res_list,
                                       lambda_range=lambda_range,
                                       n_lambda=n_lambda,
                                       n_sigma=1)

# compute aic along penalization strength
aic = compute_model_selection_criteria(result_list=res_list, objective=obj, ms_criteria='AIC')

# compute bic along penalization strength
aicc = compute_model_selection_criteria(result_list=res_list, objective=obj, ms_criteria='AICC', n_data=6)

# compute bic along penalization strength
bic = compute_model_selection_criteria(result_list=res_list, objective=obj, ms_criteria='BIC', n_data=6)

# compute converted points
conv_points = compute_converged_points(result_list=res_list)

file_name_ms = str(n_lambda) + ',' + str(n_starts)

save_modelSelection(reg_path=reg_path,
                    lambda_range=lambda_range,
                    n_lambda=n_lambda,
                    n_sigma=1,
                    par_names=['$\\theta_1$', '$\\theta_2$', '$\\theta_3$', '$\sigma$'],
                    conv_points=conv_points,
                    n_starts=n_starts,
                    aic=aic,
                    aicc=aicc,
                    bic=bic,
                    options=options,
                    path=path_ms,
                    file_name=file_name_ms)
