"""
    plot model selection results for a quick
    view
"""

import pandas as pd
import amici
import petab
import pypesto
import numpy as np
import matplotlib.pyplot as plt
from import_functions import import_modelSelection_results
from LogicleScale import logicleTransform

file_name = 'modelSelection/logicle5_1000/100,1000'

# IMPORT FILE AND READ _________________________________________________________________________________________________

import_opt = import_modelSelection_results(file_name)
lambdas = import_opt['lambdas'][~np.isnan(import_opt['lambdas'])]
sigma = import_opt['sigma'][0]
par_names_temp = import_opt['par_names']
par_names_index = [i for i, y in enumerate(par_names_temp) if y is not np.nan]
par_names = par_names_temp[par_names_index]
conv_points = import_opt['conv_points'][:len(lambdas)]
n_starts = import_opt['n_starts'][0]
# aic = import_opt['aic'][:len(lambdas)]
# aicc = import_opt['aicc'][:len(lambdas)]
# bic = import_opt['bic'][:len(lambdas)]
options = import_opt['options'][0]

reg_path_temp = import_opt['reg_path']
reg_path =[]
z = 0
for i in range(0, len(par_names)):
    temp = []
    for j in range(0, len(lambdas)):
        temp.append(reg_path_temp[z+j])
    reg_path.append(temp)
    z += len(lambdas)

print(options)


for i in range(0, len(reg_path)):
    print('\n', reg_path[i])

# PLOT REGULARIZATION PATH _____________________________________________________________________________________________

import l1_regularization_visualize

print(reg_path)
# plot regularization path
l1_regularization_visualize.plot_regularization_path(reg_path=reg_path,
                                                     lambdas=lambdas,
                                                     parameter_names=par_names,
                                                     n_sigma=sigma)


# PLOT BARS ____________________________________________________________________________________________________________

# define threshold which parameters are set to 0
threshold_linear = 1e-8

fig = plt.figure()
ax = fig.add_subplot(111)

l1_regularization_visualize.plot_regularization_bars(reg_path=reg_path,
                                                     lambdas=lambdas,
                                                     threshold=threshold_linear,
                                                     par_names=['$\\theta_1$', '$\\theta_2$', '$\\theta_3$'],
                                                     ax=ax,
                                                     opt_lambda=None,
                                                     v_min=0,
                                                     v_max=1,
                                                     cb_ticks=None)

plt.show()



# PLOT NUMBER OF PARAMETERS ____________________________________________________________________________________________

fig = plt.figure()
ax = fig.add_subplot(111)
l1_regularization_visualize.plot_number_of_parameters(reg_path=reg_path,
                                                      lambdas=lambdas,
                                                      threshold=threshold_linear,
                                                      ax=ax,
                                                      opt_lambda=None)
plt.show()


# PLOT AIC _____________________________________________________________________________________________________________

# plot aic



# plot aicc


# plot bic