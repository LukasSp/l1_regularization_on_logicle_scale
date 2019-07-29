"""
    Here we transform the optimal parameters given
    by the benchmark collection into the different
    parameter scales for the petab format
"""

import numpy as np
import LogicleScale
from LogicleScale import logicleTransform

#  0) delta_EL = 0.5179,  (bench, paper)
#  1) delta_LM = 0.02258,
#  2) delta_NE = 0.0119,
#  3) mu_EE =    3.9e-05
#  4) mu_LE =    1.0e-10
#  5) mu_LL =    8.11e-06
#  6) mu_N =     0.7399
#  7) mu_P =     1.0e-05
#  8) mu_PE =    1.3-10
#  9) mu_PL =    3.65e-05
# 10) rho_E =    0.507
# 11) rho_P =    0.126



log10_param = [-0.285715569025781, -1.646263811909550, -1.923330873687940, -4.407424157293230, -9.999999999999970,
               -5.090700702632190, -0.130822685281946, -4.999999984703740, -9.850015466520460, -4.439611388717350,
               -0.294636143004535, -0.898313770624401]

linear_param = [0.51794597529254, 0.0225806365892933, 0.0119307857579241, 3.91359322673521e-05,
                1.00000000000005e-10, 8.11520135326853e-06, 0.739907308603256, 1.00000002976846e-05,
                1.41248724e-10, 3.6340308186265e-05, 0.507415703707752, 0.126382288121756]

print(10**np.array(log10_param))

# par logE
logE_1_param = np.log10(np.array(linear_param)+1)
print('\nlogE + 1: ', logE_1_param)

# par logE_eps
eps = 1e-5
logE_eps_param = np.log10(np.array(linear_param)+eps)
print('\nlogE + ' + str(eps) + ': ', logE_eps_param)

# logicle parameter
logicle_par_1000 = logicleTransform(linear_param, T=1, end_lin=1e-5)[0]
print('\nlogicle T = 1, end_lin = 1e-5: ', logicle_par_1000)

logicle_par_1000 = logicleTransform(linear_param, T=10, end_lin=1e-5)[0]
print('\nlogicle T = 10, end_lin = 1e-5: ', logicle_par_1000)

logicle_par_1000 = logicleTransform(linear_param, T=100, end_lin=1e-5)[0]
print('\nlogicle T = 100, end_lin = 1e-5: ', logicle_par_1000)

logicle_par_1000 = logicleTransform(linear_param, T=1000, end_lin=1e-5)[0]
print('\nlogicle T = 1000, end_lin = 1e-5: ', logicle_par_1000)

logicle_obj = LogicleScale.LogicleObject(T=1, W=0.1, M=0.5, A=-0.1)
print(logicleTransform(linear_param, T=1, W=0.1, M=0.5, A=-0.1)[0])

print(LogicleScale.logicleInverseTransform([0.1/0.4], logicle_obj))
import LogicleScale
l = LogicleScale.LogicleObject(T=1000, end_lin=1e-5)
