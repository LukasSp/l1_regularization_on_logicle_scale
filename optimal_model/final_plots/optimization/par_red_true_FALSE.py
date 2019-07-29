import numpy as np
import matplotlib.pyplot as plt
import pypesto.visualize
from import_functions import import_optimization_results
from LogicleScale import logicleTransform, logicleInverseTransform, LogicleObject



def plot_par(nominal_par, lb, ub, best_par, ax):
    y = np.linspace(0, len(nominal_par) - 1, len(nominal_par))
    ax.plot(np.array(lb)[::-1], np.linspace(0, len(lb) - 1, len(lb)), '--', color='black')
    ax.plot(np.array(ub)[::-1], np.linspace(0, len(ub) - 1, len(ub)), '--', color='black')
    ax.plot(nominal_par[::-1], y, 'o--', color='green', label='nominal parameters')
    print(best_par)
    ax.plot(best_par[::-1], y, 'o-', color='red', label='optimized parameters')
    ax.set_yticks(y)
    ax.set_yticklabels(par_names[::-1])
    # ax.ylabel('parameter name')
    ax.set_xlabel('parameter value', fontsize=12)
    # ax.yticks(y, par_names[::-1])
    # ax.legend()


best_par_paper = [0.59, 0.025, 0.009, 21.5e-6, 3.6e-8, 7.5e-6,
                  0.75, 5.5e-2, 1.8e-7, 1.8e-5, 0.64, 0.15, 0]

best_par_paper_log = [0.59, 0.025, 0.009, 21.5e-6, 3.6e-8, 7.5e-6,
                  0.75, 5.5e-2, 1.8e-7, 1.8e-5, 0.64, 0.15, -5]

par_names = ['delta_EL', 'delta_LM', 'delta_NE', 'mu_EE', 'mu_LE', 'mu_LL', 'mu_N', 'mu_P',
             'mu_PE', 'mu_PL', 'rho_E', 'rho_P','delta_LE']


index_red = [4, 7]


fig, axs = plt.subplots(nrows=1, ncols=2, constrained_layout=True, sharey='row', figsize=(12,5))

scale = ['log10','log10']# 'logicle5_100'] # , 'log10', 'log10' ]

i = 0

for ax in axs.flatten():

    file_name = 'optimization/' + scale[i] + '/1000'
    import_opt = import_optimization_results(file_name)
    best_par_tmp = import_opt['best_par'][~np.isnan(import_opt['best_par'])]
    nominal_par = import_opt['nominal_par'][~np.isnan(import_opt['nominal_par'])]
    par_names_1 = np.array(import_opt['par_names'])[:len(nominal_par)]

    best_par = []
    for j in range(len(best_par_tmp)):
        best_par.append(best_par_tmp[j])

    print(best_par)
    best_par.insert(index_red[0], 0)
    best_par.insert(index_red[1], 0)
    print(best_par)


    opt_interval = import_opt['opt_interval']
    lb = []
    ub = []
    for j in range(0, len(nominal_par)):
        lb.append(opt_interval[j])
        ub.append(opt_interval[j + len(nominal_par)])

    # ax.set_xscale('log')



    if i == 0:
        paper_log = np.log10(np.array(best_par_paper_log))
        plot_par(paper_log, lb, ub, best_par, axs.flatten()[0])
        ax.set_title('$\log_{10}$', fontsize=18)#, weight='bold')
        ax.set_ylabel('parameter name', fontsize=14)
        ax.set_xlabel('parameter value', fontsize=14)
        ax.text(-0.08, 1.03, 'A', transform=ax.transAxes, size=22, weight='bold')
        ax.set_xticks([-10,-5, 3])


    if i == 1:
        paper_log = np.log10(np.array(best_par_paper_log))
        plot_par(paper_log, lb, ub, best_par, axs.flatten()[0])
        ax.set_title('$\log_{10}$', fontsize=18)#, weight='bold')
        ax.set_ylabel('parameter name', fontsize=14)
        ax.set_xlabel('parameter value', fontsize=14)
        ax.text(-0.08, 1.03, 'A', transform=ax.transAxes, size=22, weight='bold')
        ax.set_xticks([-10,-5, 3])

        # paper_logicle = logicleTransform(best_par_paper, T=100, end_lin=1e-5)[0]
        # plot_par(paper_logicle, lb, ub, best_par, axs.flatten()[1])
        # ax.set_title('logicle', fontsize=18)#, weight='bold')
        # ax.text(-0.08, 1.03, 'B', transform=ax.transAxes, size=22, weight='bold')
        # ax.set_xlabel('parameter value', fontsize=14)
        # ax.set_xticks([0,0.25,0.5,0.75,1])

    i += 1

plt.show()


fig.savefig('par_true_our.eps', format='eps', dpi=1200)