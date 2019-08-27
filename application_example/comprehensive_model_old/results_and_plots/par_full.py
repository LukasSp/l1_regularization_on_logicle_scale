import numpy as np
import matplotlib.pyplot as plt
import pypesto.visualize
from import_functions import import_optimization_results
from LogicleScale import logicleTransform, logicleInverseTransform, LogicleObject


def plot_par(nominal_par, lb, ub, best_par, ax):
    y = np.linspace(0, 20, 21)
    z = np.linspace(0 + 9, 11+9, 12)
    ax.plot(np.array(lb)[::-1], np.linspace(0, len(lb) - 1, len(lb)), '--', color='black')
    ax.plot(np.array(ub)[::-1], np.linspace(0, len(ub) - 1, len(ub)), '--', color='black')
    ax.plot(nominal_par[::-1], z, 'o--', color='green', label='nominal parameters')
    print(best_par)
    ax.plot(best_par[::-1], y, 'o-', color='red', label='optimized parameters')
    ax.set_yticks(y)
    ax.set_yticklabels(par_names[::-1], fontsize=12)
    # ax.ylabel('parameter name')
    ax.set_xlabel('parameter value', fontsize=16)
    # ax.yticks(y, par_names[::-1])
    # ax.legend()


best_par_paper_1 = [0.59, 0.025, 0.009, 21.5e-6, 3.6e-8, 7.5e-6,
                  0.75, 5.5e-2, 1.8e-7, 1.8e-5, 0.64, 0.15]#,
                  #10**-10, 10**-10, 10**-10,10**-10,10**-10,10**-10,10**-10,10**-10,10**-10]

best_par_paper = [0.59, 0.025, 0.009, 21.5e-6, 3.6e-8, 7.5e-6,
                  0.75, 5.5e-2, 1.8e-7, 1.8e-5, 0.64, 0.15]#,
                  #0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

best_par_paper_logE = [0.59, 0.025, 0.009, 21.5e-6, 2*1e-5, 2*1e-5,
                  0.75, 5.5e-2, 2*1e-5, 2*1e-5, 0.64, 0.15] #,
                  #2*1e-5,2*1e-5,2*1e-5,2*1e-5,2*1e-5,2*1e-5,2*1e-5,2*1e-5,2*1e-5]


#print('hh', np.log10(np.array(best_par_paper_logE)))
#print('hh', np.log10(np.array(best_par_paper_logE) - 1e-5))

fig, axs = plt.subplots(nrows=1, ncols=3, constrained_layout=True, sharey='row', figsize=(13,6))

scale = ['log10', 'logicle5_100', 'logE_eps'] # , 'log10', 'log10' ]

i = 0

for ax in axs.flatten():

    file_name = 'optimization/' + scale[i] + '/5000'
    import_opt = import_optimization_results(file_name)
    best_par = import_opt['best_par'][~np.isnan(import_opt['best_par'])]
    nominal_par = import_opt['nominal_par'][~np.isnan(import_opt['nominal_par'])]
    par_names = np.array(import_opt['par_names'])[:len(nominal_par)]

    opt_interval = import_opt['opt_interval']
    lb = []
    ub = []
    for j in range(0, len(nominal_par)):
        lb.append(opt_interval[j])
        ub.append(opt_interval[j + len(nominal_par)])

    # ax.set_xscale('log')
    ax.set_ylim(-0.5, 20.5)

    if i == 0:
        paper_log = np.log10(np.array(best_par_paper_1))
        plot_par(paper_log, lb, ub, best_par, axs.flatten()[0])
        ax.set_title('$\log_{10}$', fontsize=16)#, weight='bold')
        ax.set_ylabel('parameter name', fontsize=16)
        ax.text(-0.08, 1.01, 'A', transform=ax.transAxes, size=22, weight='bold')
        ax.set_xticks([-10,-5, 0,  3])
        for j in range(0, 9):
            ax.get_yticklabels()[j].set_color('red')


    if i == 1:
        paper_logicle = logicleTransform(best_par_paper, T=100, end_lin=1e-6)[0]
        plot_par(paper_logicle, lb, ub, best_par, axs.flatten()[1])
        ax.set_title('logicle', fontsize=16)#, weight='bold')
        ax.text(-0.08, 1.01,  'B', transform=ax.transAxes, size=22, weight='bold')
        ax.set_xticks([0,0.25,0.5,0.75,1])

    if i == 2:
        paper_logE = np.log10(np.array(best_par_paper_logE) - 1e-5)
        print('lin', 10 ** np.array(best_par) - 1e-5)
        plot_par(paper_logE, lb, ub, best_par, axs.flatten()[2])
        ax.set_title('$\log_{10}(\\theta+10^{-5})$', fontsize=16)#, weight='bold')
        ax.text(-0.08, 1.01,  'C', transform=ax.transAxes, size=22, weight='bold')
        ax.set_xticks([-5, -2, 0, 2])

    i += 1

plt.show()


fig.savefig('par_full_true.eps', format='eps', dpi=1200)
