import numpy as np
import matplotlib.pyplot as plt
import pypesto.visualize
from import_functions import import_optimization_results
from LogicleScale import LogicleObject, logicleTransform

file_name = 'optimization/log10/1000'
import_opt = import_optimization_results(file_name)
fval = import_opt['fval'][~np.isnan(import_opt['fval'])]
fval = fval[fval < 1e10]


n_starts = int(import_opt['n_start'][~np.isnan(import_opt['n_start'])])
best_par = import_opt['best_par'][~np.isnan(import_opt['best_par'])]
nominal_par = import_opt['nominal_par'][~np.isnan(import_opt['nominal_par'])]
par_names = np.array(import_opt['par_names'])[:len(nominal_par)]
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





fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(nrows=2, ncols=2, constrained_layout=True, figsize=(8,7), sharey='row')

# waterfall
n = 100
pypesto.visualize.waterfall_lowlevel(fval[:n], scale_y='lin', ax=ax1)
ax1.hlines(190.96, 0, n, linestyles='dashed')
ax1.text(-0.1, 1.05, 'A', transform=ax1.transAxes, size=20, weight='bold')
ax1.set_title('$\log_{10}$', fontsize=14)
#ax1.set_title('Waterfall plot', fontsize=14)
ax1.set_xlabel('ordered optimizer run', fontsize=14)
ax1.set_ylabel('likelihood value', fontsize=14)
ax1.set_xticks([0, 20, 40, 60, 80, 100])
ax1.set_xlim(-1, n)




best_par_paper = [0.59, 0.025, 0.009, 21.5e-6, 3.6e-8, 7.5e-6,
                  0.75, 5.5e-2, 1.8e-7, 1.8e-5, 0.64, 0.15]
index_lin = np.linspace(1, 12, 12)

best_par_paper_log = [0.59, 0.025, 0.009, 21.5e-6, 3.6e-8, 7.5e-6,
                  0.75, 5.5e-2, 1.8e-7, 1.8e-5, 0.64, 0.15, -5]

par_names = ['delta_EL', 'delta_LM', 'delta_NE', 'mu_EE', 'mu_LE', 'mu_LL', 'mu_N', 'mu_P',
             'mu_PE', 'mu_PL', 'rho_E', 'rho_P','delta_LE']


index_red = [4, 7]

best_par_log = [-0.11508453, -1.59008064, -1.71610071, -4.63725562, -5.22995268, -0.10316299, -7.09262244,
                -4.62050801, -0.31441241, -0.90634609, -0.77518533]

best_par_logicle = [0.71403861, 0.53124423, 0.49639239, 0.07264355, 0.04018985, 0.7201659,
 0.0019951 , 0.12294839 ,0.7012356 , 0.61790586 ,0.56526125]

# index_log = [0, 1, 2, 3, 5, 6, 8, 9, 10, 11, 12]
index_log = [0, 1, 2, 3, 4, 6, 7, 9, 10, 11, 12]

lb_log = [-5, -5, -5, -5, -10, -10, -5, -5, -10, -5, -5, -5, -10]
ub_log = [3]*13

lb_logicle = [0]*13
ub_logicle = [1]*13



paper_log = np.log10(np.array(best_par_paper))

ax3.plot(np.array(lb_log)[::-1], np.linspace(0, len(lb_log) - 1, len(lb_log)), '--', color='black')
ax3.plot(np.array(ub_log)[::-1], np.linspace(0, len(ub_log) - 1, len(ub_log)), '--', color='black')
ax3.plot(paper_log[::-1], index_lin, 'o--', color='green', label='nominal parameters')
ax3.plot(best_par_log[::-1], index_log, 'o-', color='red', label='optimized parameters')
ax3.set_title('$\log_{10}$', fontsize=14)#, weight='bold')
ax3.set_ylabel('parameter name', fontsize=14)
ax3.set_xlabel('parameter value', fontsize=14)
ax3.text(-0.1, 1.05, 'C', transform=ax3.transAxes, size=20, weight='bold')
ax3.set_xticks([-10,-5, 0, 3])
ax3.set_yticks(np.linspace(0, 12, 13))
ax3.set_yticklabels(par_names[::-1])
ax3.get_yticklabels()[0].set_color('red')


file_name = 'optimization/logicle/5000'
import_opt = import_optimization_results(file_name)
fval = import_opt['fval'][~np.isnan(import_opt['fval'])]
fval = fval[fval < 1e10]


n_starts = int(import_opt['n_start'][~np.isnan(import_opt['n_start'])])
best_par = import_opt['best_par'][~np.isnan(import_opt['best_par'])]
nominal_par = import_opt['nominal_par'][~np.isnan(import_opt['nominal_par'])]
par_names = np.array(import_opt['par_names'])[:len(nominal_par)]
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



n = 100
pypesto.visualize.waterfall_lowlevel(fval[:n], scale_y='lin', ax=ax2)
ax2.hlines(190.96, 0, n, linestyles='dashed')
ax2.text(-0.1, 1.05, 'B', transform=ax2.transAxes, size=20, weight='bold')
# ax2.set_title('Waterfall plot', fontsize=14)
ax2.set_title('logicle', fontsize=14)
ax2.set_xlabel('ordered optimizer run', fontsize=12)
ax2.set_ylabel('', fontsize=12)
ax2.set_xticks([0, 20, 40, 60, 80, 100])
ax2.set_xlim(-1, n)


# ax4
paper_logicle =logicleTransform(best_par_paper,T=100, end_lin=1e-5)[0]
ax4.plot(np.array(lb_logicle)[::-1], np.linspace(0, len(lb_logicle) - 1, len(lb_logicle)), '--', color='black')
ax4.plot(np.array(ub_logicle)[::-1], np.linspace(0, len(ub_logicle) - 1, len(ub_logicle)), '--', color='black')
ax4.plot(paper_logicle[::-1], index_lin, 'o--', color='green', label='nominal parameters')
ax4.plot(best_par_logicle[::-1], index_log, 'o-', color='red', label='optimized parameters')
ax4.set_title('logicle', fontsize=14)  # , weight='bold')
# ax4.set_ylabel('parameter name', fontsize=12)
ax4.set_xlabel('parameter value', fontsize=14)
ax4.text(-0.1, 1.05, 'D', transform=ax4.transAxes, size=20, weight='bold')
ax4.set_xticks([0, 0.25, 0.5, 0.75, 1])
# ax4.set_yticks(np.linspace(0, 12, 13))
# ax4.set_yticklabels(par_names[::-1])


plt.show()

# fig.savefig('opt_reduced.eps', format='eps', dpi=1200)

