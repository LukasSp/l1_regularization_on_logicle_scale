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

import LogicleScale
from LogicleScale import logicleInverseTransform, logicleInverseGradient


# IMPORT MODEL__________________________________________________________________________________________________________

folder_base = "models/"
model_name = "Crauste_full_logicle5_10"

petab_problem = petab.Problem.from_folder(folder_base + model_name)

petab_problem.model_name = 'Crauste_full_logicle5_10'

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

# play with the tolerance
solver.setRelativeTolerance(rtol=1e-10)
solver.setAbsoluteTolerance(atol=1e-10)

# enable sensitivities
solver.setSensitivityOrder(amici.SensitivityOrder_first)       # First-order ...
solver.setSensitivityMethod(amici.SensitivityMethod_forward)   # ... forward sensitivities
model.requireSensitivitiesForAllParameters()                   # ... w.r.t. all parameters

# play with FSA tolerances
solver.setRelativeToleranceFSA(rtol=1e-10)
solver.setAbsoluteToleranceFSA(atol=1e-10)

# CREATE LOGICLE OBJECTIVE FUNCTION __________________________________________________________________________________

obj_lin = importer.create_objective(solver=solver)

# logicle parameter
T = 10
end_lin = 1e-5
logicle_obj = LogicleScale.LogicleObject(T=T, end_lin=end_lin)

f = lambda x: obj_lin.get_fval(logicleInverseTransform(par=x, logicle_object=logicle_obj))
g = lambda x: obj_lin.get_grad(logicleInverseTransform(x, logicle_obj)) * logicleInverseGradient(x, logicle_obj)

obj = pypesto.Objective(fun=f, grad=g) #, hess=h)

print('optimal x = ', petab_problem.x_nominal)
print('optimal lh value', obj(petab_problem.x_nominal))


# check gradient at optimum and at random point
check_grad_1 = obj.check_grad(petab_problem.x_nominal)
print(check_grad_1[np.array(['grad', 'fd_c', 'abs_err', 'rel_err'])])

x_random = np.random.normal(0.5, 0.005, 22)
check_grad_2 = obj.check_grad(x_random)
print(check_grad_2[np.array(['grad', 'fd_c', 'abs_err', 'rel_err'])])


# OPTIMIZATION WITHOUT PRIOR ___________________________________________________________________________________________

optimizer = pypesto.ScipyOptimizer(method='L-BFGS-B')

# play with optimization options
optimizer.options = {'maxiter': 1e5, 'ftol': 1e-10, 'gtol': 1e-10, 'maxls': 80}
# optimizer.options = {'maxcor': 10, 'ftol': 1e-10, 'gtol': 1e-05, 'eps': 1e-08, 'maxfun': 1e5,
#                     'maxiter': 1e5, 'maxls': 20}

problem = importer.create_problem(obj)
engine = pypesto.SingleCoreEngine()
n_starts = 10
start = time.time()
result = pypesto.minimize(problem=problem,
                          optimizer=optimizer,
                          n_starts=n_starts,
                          engine=engine)
end = time.time()

print('\nbest parameter: ', result.optimize_result.as_list('x')[0]['x'])
print('best likelihood value: ', obj(result.optimize_result.as_list('x')[0]['x']))

# calculate computation time
comp_time = end - start

# calculate converged points
conv_points = compute_converged_points_single(result=result)
print('converted points: ', conv_points)


# SAVE STARTPOINTS _____________________________________________________________________________________________________

# calculate the startpoints
startpoints = result.optimize_result.get_for_key('x0')

# save the startpoints
save_startpoints(result=result, path='startpoints/', file_name='logicle5_10')


# SAVE OPTIMIZATION RESULTS ____________________________________________________________________________________________

# options
options = 'MODEL: Crauste model FULL, ' \
          '\nSCALE: logicle(T=' + str(T) + ', end_lin=' + str(end_lin) + ')' +\
          '\nSTARTS: ' + str(n_starts) + \
          '\nCONV POINTS: ' + str(conv_points) + \
          '\nTIME: ' + str(comp_time)

# specify path
path = 'results_and_plots/optimization/logicle5_10/'

# file name is equal to starting points
file_name = str(n_starts)

# save
save_optimization_to_file(result=result,
                          n_start=n_starts,
                          nominal_par=petab_problem.x_nominal,
                          par_names=model.getParameterIds()[:22],
                          opt_lh=obj(petab_problem.x_nominal),
                          file_name=file_name,
                          conv_points=conv_points,
                          comp_time=comp_time,
                          opt_interval=[problem.lb, problem.ub],
                          startpoints=startpoints,
                          options=options,
                          path=path)

# SAVE GUESSES _________________________________________________________________________________________________________

# save converged points to use them as starting points for
# the regularization

path_guess = 'guesses/logicle5_10/'

save_guesses(result=result,
             n_starts=n_starts,
             nominal_par=petab_problem.x_nominal,
             options=options,
             path=path_guess,
             file_name=file_name)


# INITIALIZE L1 REGULARIZATION _________________________________________________________________________________________

import regularization

# specify inputs, without noise parameters
n = len(model.getParameters()[:22])

# all parameters are logical
scale_list_logicle = ['logicle'] * n

# the noise parameter should not be penalized
estimate_list = [1] * n

# the range of penalization strength
lambda_range = [1e-8, 1e6]

# number of penalizations
n_lambda = 200


# initalize l1 regularization
# add shift parameter (=epsilon) which defines the offset of
# the logarithmic scale
initialize_regularization = regularization.l1_regularization(model=model,
                                                             petab_problem=petab_problem,
                                                             objective=obj,
                                                             scale_list=scale_list_logicle,
                                                             estimate_list=estimate_list,
                                                             lambda_range=lambda_range,
                                                             n_lambda=n_lambda,
                                                             logicle_obj=logicle_obj)


# DO L1 REGULARIZATION _________________________________________________________________________________________________

# specify inputs
n_starts = 1000

# optimization method and options
opt_method = 'L-BFGS-B'
opt_options = {'maxiter': 1e5, 'ftol': 1e-10, 'gtol': 1e-10, 'maxls': 80}
# opt.options = {'maxcor': 10, 'ftol': 1e-10, 'gtol': 1e-05, 'eps': 1e-08, 'maxfun': 1e5,
#                'maxiter': 1e5, 'maxls': 20}

# define startpoints as the best starts of the optimization
path_guess = 'guesses/logicle5_10/5000'
x_guesses = import_guesses(path_guess)[0]

# define path for the results
path_ms = 'results_and_plots/modelSelection/logicle5_10/'

# optimize all objective functions
start = time.time()
res_list = initialize_regularization(n_starts=n_starts,
                                     x_guesses=x_guesses,
                                     opt_method=opt_method,
                                     opt_options=opt_options,
                                     par_names=model.getParameterIds()[:22],
                                     path=path_ms)
end = time.time()


# SAVE REGULARIZATION RESULTS TO FILE __________________________________________________________________________________

# computation time
comp_time = end - start

# options
options = 'MODEL: Crauste model FULL, ' \
          '\nSCALE: logicle(T=' + str(T) + ', end_lin=' + str(end_lin) + ')' +\
          '\nSTARTS: ' + str(n_starts) + \
          '\nCONV POINTS: ' + str(conv_points) + \
          '\nTIME: ' + str(comp_time)

# compute regularization path
reg_path = compute_regularization_path(result_list=res_list,
                                       lambda_range=lambda_range,
                                       n_lambda=n_lambda,
                                       n_sigma=0)

# compute aic along penalization strength
aic = compute_model_selection_criteria(result_list=res_list, objective=obj, ms_criteria='AIC')

# AICc not possible

# compute bic along penalization strength
bic = compute_model_selection_criteria(result_list=res_list, objective=obj, ms_criteria='BIC', n_data=21)

# compute converted points
conv_points = compute_converged_points(result_list=res_list)

file_name_ms = str(n_lambda) + ',' + str(n_starts)

save_modelSelection(reg_path=reg_path,
                    lambda_range=lambda_range,
                    n_lambda=n_lambda,
                    n_sigma=0,
                    par_names=model.getParameterIds()[:22],
                    conv_points=conv_points,
                    n_starts=n_starts,
                    aic=aic,
                    aicc=None,
                    bic=bic,
                    options=options,
                    path=path_ms,
                    file_name=file_name_ms)
