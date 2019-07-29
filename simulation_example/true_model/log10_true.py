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

# IMPORT MODEL__________________________________________________________________________________________________________

folder_base = "models/"
model_name = "caroModel_true_log10"

petab_problem = petab.Problem.from_folder(folder_base + model_name)

petab_problem.model_name = 'caroModel_true_log10'

importer = pypesto.PetabImporter(petab_problem)
importer.compile_model()

model = importer.create_model()

# scaling
# print(model.getParameterScale(), '\n')
# model.setParameterScale(amici.ParameterScaling_none)

print("Model parameters:", list(model.getParameterIds()), '\n')
print('Optimization parameters:', petab_problem.get_optimization_to_simulation_parameter_mapping(), '\n')
print("Model outputs:   ", list(model.getObservableIds()), '\n')
print("Model states:    ", list(model.getStateIds()), '\n')

print('sigmas', petab_problem.get_sigmas())


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
save_startpoints(result=result, path='startpoints/', file_name='log10')

# import startpoints
startpoints_import = import_startpoints('startpoints/log10')


# SAVE OPTIMIZATION RESULTS ____________________________________________________________________________________________

# add options
options = 'MODEL: caro model true, ' \
          '\nSCALE: log10, ' \
          '\nSTARTS: ' + str(n_starts) + \
          '\nCONV POINTS: ' + str(conv_points) + \
          '\nTIME: ' + str(comp_time)

# specify path
path = 'results/log10/'

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
