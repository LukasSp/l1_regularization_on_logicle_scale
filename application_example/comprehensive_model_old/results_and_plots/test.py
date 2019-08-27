import numpy as np
import matplotlib.pyplot as plt
import pypesto.visualize
from import_functions import import_optimization_results
from LogicleScale import logicleTransform, logicleInverseTransform, LogicleObject


def plot_par(nominal_par, lb, ub, best_par, ax, xs=None):
    y = np.linspace(0, 20, 21)
    z = np.linspace(0 + 9, 11+9, 12)
    ax.plot(nominal_par[::-1], z, 'o--', color='green', label='nominal parameters')
    l = ['best', '2nd', '3rd', '4th', '5th']
    c = ['red', 'blue', 'orange', 'magenta']
    if xs is not None:
        for i in range(0, len(xs)):
            ax.plot(xs[i][::-1], y, 'o-', color=c[i], label=l[i])

    ax.plot(np.array(lb)[::-1], np.linspace(0, len(lb) - 1, len(lb)), '--', color='black', label='')
    ax.plot(np.array(ub)[::-1], np.linspace(0, len(ub) - 1, len(ub)), '--', color='black')




    print(best_par)
    # ax.plot(best_par[::-1], y, 'o-', color='red', label='optimized parameters')
    ax.set_yticks(y)
    ax.set_yticklabels(par_names[::-1])
    # ax.ylabel('parameter name')
    ax.set_xlabel('parameter value', fontsize=12)
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

fig, ax = plt.subplots(nrows=1, ncols=1, constrained_layout=True, sharey='row', figsize=(8,6))

scale = ['log10', 'logicle5_100', 'logE_eps'] # , 'log10', 'log10' ]


file_name = 'optimization/' + scale[0] + '/5000'
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

xs_temp = import_opt['xs'][:(5000*21)]
xs = np.zeros((5000, len(nominal_par)))
z = 0
for i in range(0, 5000):
    # if xs_temp[i] is not None:
    for j in range(0, len(nominal_par)):
        xs[i, j] = xs_temp[z+j]
    z += len(nominal_par)



ax.set_ylim(-0.5, 20.5)

paper_log = np.log10(np.array(best_par_paper_1))
plot_par(paper_log, lb, ub, best_par, ax, xs[:4])
ax.plot()
ax.set_title('$\log_{10}$', fontsize=16)#, weight='bold')
ax.set_ylabel('parameter name', fontsize=12)
ax.text(-0.08, 1.01, 'A', transform=ax.transAxes, size=22, weight='bold')
ax.set_xticks([-10,-5, 0,  3])
for j in range(0, 9):
    ax.get_yticklabels()[j].set_color('red')

l = ['nominal', 'best', '2nd', '3rd', '4th']#, '5th']
fig.legend(labels=l, loc=5, fontsize=11)
fig.tight_layout()
fig.subplots_adjust(right=0.85)

# ax.legend()
plt.show()


# fig.savefig('par_full_true.eps', format='eps', dpi=1200)
