import amici
import petab
import pypesto
import pypesto.visualize
import numpy as np
import time

# import function to save/import your results
from save_functions import save_optimization_to_file, save_startpoints
from import_functions import import_startpoints

# import regularization routines
from l1_regularization_computations import compute_converged_points_single

import LogicleScale
from LogicleScale import logicleTransform, logicleInverseTransform, logicleInverseGradient


# IMPORT MODEL__________________________________________________________________________________________________________

folder_base = "models/"
model_name = "caroModel_true_logicle5_1000"

petab_problem = petab.Problem.from_folder(folder_base + model_name)

petab_problem.model_name = 'caroModel_true_logicle5_1000'

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


# CREATE LOGICLE OBJECTIVE FUNCTION __________________________________________________________________________________

obj_lin = importer.create_objective(solver=solver)

# logicle parameter
T = 1000
end_lin = 1e-5
logicle_obj = LogicleScale.LogicleObject(T=T, end_lin=end_lin)

f = lambda x: obj_lin.get_fval(logicleInverseTransform(par=x, logicle_object=logicle_obj))
g = lambda x: obj_lin.get_grad(logicleInverseTransform(x, logicle_obj)) * logicleInverseGradient(x, logicle_obj)

obj = pypesto.Objective(fun=f, grad=g)

print('optimal x = ', petab_problem.x_nominal)
print('optimal lh value', obj(petab_problem.x_nominal))


# check gradient
check_grad = obj.check_grad(petab_problem.x_nominal)
print(check_grad[np.array(['grad', 'fd_c', 'abs_err', 'rel_err'])])


# OPTIMIZATION WITHOUT PRIOR ___________________________________________________________________________________________

optimizer = pypesto.ScipyOptimizer()
problem = importer.create_problem(obj)
engine = pypesto.SingleCoreEngine()
n_starts = 10

start = time.time()
result = pypesto.minimize(problem=problem,
                          optimizer=optimizer,
                          n_starts=n_starts,
                          engine=engine)
end = time.time()

print('best parameter: ', result.optimize_result.as_list('x')[0]['x'])
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
save_startpoints(result=result, path='startpoints/', file_name='logicle5_1000')

# import startpoints
startpoints_import = import_startpoints('startpoints/logicle5_1000')


# SAVE OPTIMIZATION RESULTS ____________________________________________________________________________________________

# add options
options = 'MODEL: true caro model, ' \
          '\nSCALE: logicle(T=' + str(T) + ', end_lin=' + str(end_lin) + \
          '\nSTARTS: ' + str(n_starts) + \
          '\nCONV POINTS: ' + str(conv_points) + \
          '\nTIME: ' + str(comp_time)

# specify path
path = 'results/logicle5_1000/'

# file name is equal to starting points
file_name = str(n_starts)

# save
save_optimization_to_file(result=result,
                          n_start=n_starts,
                          nominal_par=petab_problem.x_nominal,
                          par_names=['$\\xi_1$', '$\\xi_2$', '$\sigma$'],
                          opt_lh=obj(petab_problem.x_nominal),
                          file_name=file_name,
                          conv_points=conv_points,
                          comp_time=comp_time,
                          opt_interval=[problem.lb, problem.ub],
                          startpoints=startpoints,
                          options=options,
                          path=path)
