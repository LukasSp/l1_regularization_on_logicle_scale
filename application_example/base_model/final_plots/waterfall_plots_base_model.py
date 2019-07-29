"""
    Plot the waterfalls for all 4 scales log10, logicle,
    shifted log10 with 1 and 1e-5. The dashed line is
    the lh value at the optimal value found by crauste et al
"""

import numpy as np
import matplotlib.pyplot as plt
import pypesto.visualize
from import_functions import import_optimization_results


file_name = 'optimization/log10/5000'
import_opt = import_optimization_results(file_name)
fval1 = import_opt['fval'][~np.isnan(import_opt['fval'])]
fval1 = fval1[fval1 < 1e10]

file_name = 'optimization/logicle5_100/5000'
import_opt = import_optimization_results(file_name)
fval2 = import_opt['fval'][~np.isnan(import_opt['fval'])]
fval2 = fval2[fval2 < 1e10]

file_name = 'optimization/logE_1/5000'
import_opt = import_optimization_results(file_name)
fval3 = import_opt['fval'][~np.isnan(import_opt['fval'])]
fval3 = fval3[fval3 < 1e10]

file_name = 'optimization/logE_eps/5000'
import_opt = import_optimization_results(file_name)
fval4 = import_opt['fval'][~np.isnan(import_opt['fval'])]
fval4 = fval4[fval4 < 1e10]


fval = [fval1,fval2,fval3, fval4]
title = ['$\log_{10}$', 'logicle', '$\log_{10}(\\theta + 1)$', '$\log_{10}(\\theta + 10^{-5})$']

n = 100

l = ['A', 'B', 'C', 'D']
i = 0
fig, axs = plt.subplots(nrows=2, ncols=2, constrained_layout=True, sharex='col', sharey='row', figsize=(8,7))
for ax in axs.flatten():
    pypesto.visualize.waterfall_lowlevel(fval[i][:n], scale_y='lin', ax=ax)
    ax.set_xticks([0, 20, 40, 60, 80, 100])
    ax.set_title(title[i], fontsize=14) #, weight='bold')
    ax.text(-0.1, 1.05, l[i], transform=ax.transAxes, size=20, weight='bold')
    ax.hlines(193,  0, 1000, linestyles='dashed')
    ax.set_xlim(-3, 100)
    ax.set_ylim(top=320)

    if i == 0 or i == 1:
        ax.set_xlabel('')
    if i == 1 or i == 3:
        ax.set_ylabel('')
    if i == 0 or i == 2:
        ax.set_ylabel('function value', fontsize=14)
    if i == 2 or i == 3:
        ax.set_xlabel('ordered optimizer run', fontsize=14)
    i += 1

plt.show()

# fig.savefig('waterfall_true.eps', format='eps', dpi=1200)


