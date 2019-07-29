"""
    Plot the waterfall and the parameters for
    the optimization of the true model
"""

import numpy as np
import matplotlib.pyplot as plt
import pypesto.visualize
from import_functions import import_optimization_results


file_name = 'optimization/logicle5_1000/1000'


import_opt = import_optimization_results(file_name)
fval = import_opt['fval'][~np.isnan(import_opt['fval'])]
fval = fval[fval < 1e10]


n_starts = int(import_opt['n_start'][~np.isnan(import_opt['n_start'])])
best_par = import_opt['best_par'][~np.isnan(import_opt['best_par'])]
nominal_par = import_opt['nominal_par'][~np.isnan(import_opt['nominal_par'])]
par_names = ['$\\xi_1$','$\\xi_2$','$\\tilde{\sigma}}$']
opt_lh_value = import_opt['opt_lh'][~np.isnan(import_opt['opt_lh'])]
conv_points = import_opt['conv_points'][0]
comp_time = import_opt['comp_time'][0]
opt_interval = import_opt['opt_interval']
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

print('\nbest lh value:', fval[0])
print('opt lh value:', opt_lh_value)
print('\nbest parameter:', best_par)





fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, constrained_layout=True, figsize=(9,4))

# waterfall
n = 1000
pypesto.visualize.waterfall_lowlevel(fval[:n], scale_y='lin', ax=ax1)
# ax1.text(-0.08, 1.03, 'A', transform=ax1.transAxes, size=20, weight='bold')
ax1.hlines(-6.07, 0, n, linestyles='dashed')
ax1.set_title('Waterfall plot', fontsize=14)
ax1.set_xlabel('ordered optimizer run', fontsize=14)
ax1.set_ylabel('function value', fontsize=14)
ax1.set_xticks([0, 200, 400, 600, 800, 1000])
ax1.set_xlim(-10, n)

# parameter plot
y = np.linspace(0, len(nominal_par)-1, len(nominal_par))
ax2.plot(np.array(lb)[::-1], np.linspace(0, len(lb)-1, len(lb)), '--', color='black')
ax2.plot(np.array(ub)[::-1], np.linspace(0, len(ub)-1, len(ub)), '--', color='black')
ax2.plot(nominal_par[::-1], y, 'o--', color='green', label='true parameters')
ax2.plot(best_par[::-1], y, 'o-', color='red', label='optimized parameters')
# ax2.text(-0.08, 1.03, 'B', transform=ax2.transAxes, size=20, weight='bold')
ax2.set_title('Estimated parameters', fontsize=14)
ax2.set_ylabel('parameter name', fontsize=14)
ax2.set_xlabel('parameter value', fontsize=14)
ax2.set_yticks(y)
ax2.set_yticklabels(par_names[::-1], fontsize=14)
ax2.legend(fontsize=9)

plt.show()

# fig.savefig('opt_true.eps', format='eps', dpi=1200)

