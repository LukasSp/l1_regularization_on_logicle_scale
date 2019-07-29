"""
    Generating the grafic from the thesis
"""

import numpy as np
import matplotlib.pyplot as plt

from LogicleScale import logicleTransform, logicleInverseTransform

par = np.linspace(0, 1000, 1000)

T = 1000
W = 2

par_logicle = logicleTransform(par=par, T=T, M=4.5, W=W, A=-W)


fontsize = 12


fig,(ax1, ax2) = plt.subplots(nrows=1, ncols=2, constrained_layout=True, figsize=(9,4))

# generate parameters
par = [0.0]
p2 = np.linspace(1e-20, 1e-3, 1000)
p3 = [1000.0]

for i in range(0, len(p2)):
    par.append(p2[i])
par.append(p3[0])

T = 1000
end_lin = 1e-5

# transform your parameter
par_logicle = logicleTransform(par=par, T=T, end_lin=end_lin)

# calculate transition
W = par_logicle[1].W
M = par_logicle[1].M
transition = logicleInverseTransform(np.array([W/(M-W)]), par_logicle[1])

ax1.plot(par, par_logicle[0], color='black', label='logicle')
ax1.set_xlabel("linear parameter value ($\\theta$)", fontsize=fontsize)
ax1.set_ylabel("transformed parameter value ($\\xi$)", fontsize=fontsize)
ax1.plot(par, 5580*np.array(par), '--', color='green',  label='linear')
ax1.plot(par[1:], 0.115 * np.log10(par[1:])+0.65,  '--', color='red', label='logarithmic')
ax1.set_xscale('log')
ax1.set_xlim(1e-9, 1e3)
ax1.set_ylim(0, 1)
ax1.legend(loc='lower right')
ax1.text(-0.1, 1.05, 'A', transform=ax1.transAxes, size=20, weight='bold')


# display the logicle parameter
ax2.plot(par, par_logicle[0], color='black')
ax2.vlines(transition, 0, 1, color='green', label='rough end linear')
ax2.set_xlabel("linear parameter value ($\\theta$)", fontsize=fontsize)
ax2.set_ylabel("logicle parameter value ($\\xi$)", fontsize=fontsize)
ax2.set_xscale('log')
ax2.set_xlim(1e-9, 1e3)
ax2.set_ylim(0, 1)
ax2.legend(loc='lower right')
ax2.text(-0.1, 1.05, 'B', transform=ax2.transAxes, size=20, weight='bold')
plt.show()

fig.savefig('logicle_scale.eps', format='eps', dpi=1200)
