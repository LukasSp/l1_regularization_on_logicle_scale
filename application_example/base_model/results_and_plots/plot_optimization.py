"""
    plot the different optimizaiton results for
    a quick view

    Only change the path
"""

import numpy as np
import matplotlib.pyplot as plt
import pypesto.visualize
from import_functions import import_optimization_results

# specify path
file_name = 'optimization/logicle5_1/10'


# import file and store it
import_opt = import_optimization_results(file_name)
n_starts = int(import_opt['n_start'][~np.isnan(import_opt['n_start'])])
fval = import_opt['fval'][~np.isnan(import_opt['fval'])]
fval = fval[fval < 1e9]
best_par = import_opt['best_par'][~np.isnan(import_opt['best_par'])]
nominal_par = import_opt['nominal_par'][~np.isnan(import_opt['nominal_par'])]
par_names = np.array(import_opt['par_names'])[:len(nominal_par)]
opt_lh_value = import_opt['opt_lh'][~np.isnan(import_opt['opt_lh'])]
conv_points = import_opt['conv_points'][0]
comp_time = import_opt['comp_time'][0]
opt_interval = import_opt['opt_interval']
startpoints = import_opt['startpoints']
lb = []
ub = []
for i in range(0, len(nominal_par)):
    lb.append(opt_interval[i])
    ub.append(opt_interval[i + len(nominal_par)])
options = import_opt['options'][0]
xs_temp = import_opt['xs'][:(n_starts*len(nominal_par))]
xs = np.zeros((len(fval), len(nominal_par)))
z = 0
for i in range(0, len(fval)):
    for j in range(0, len(nominal_par)):
        xs[i, j] = xs_temp[z+j]
    z += len(nominal_par)

print(options)

print('\nbest lh value: ', fval[0])

print('\nbest parameter: ', best_par)

# plot waterfalls
pypesto.visualize.waterfall_lowlevel(fval, scale_y='lin')
plt.show()

# plot parameters
pypesto.visualize.parameters_lowlevel(xs=xs, fvals=fval, lb=np.array(lb), ub=np.array(ub), x_labels=par_names)
plt.plot(nominal_par[::-1], np.arange(1, len(nominal_par)+1), '--o', color='green')
plt.show()

# plot best parameter and nominal parameter
y = np.linspace(0, len(nominal_par)-1, len(nominal_par))
plt.plot(np.array(lb)[::-1], np.linspace(0, len(lb)-1, len(lb)), '--', color='black')
plt.plot(np.array(ub)[::-1], np.linspace(0, len(ub)-1, len(ub)), '--', color='black')
plt.plot(nominal_par[::-1], y, 'o--', color='green', label='nominal parameters')
plt.plot(best_par[::-1], y, 'o-', color='red', label='optimized parameters')
plt.ylabel('parameter name')
plt.xlabel('parameter value')
plt.yticks(y, par_names[::-1])
plt.legend()
plt.show()
