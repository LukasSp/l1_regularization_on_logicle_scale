import LogicleScale
from LogicleScale import logicleTransform
import numpy as np

# logicle_object = LogicleScale.LogicleObject(T=3, end_lin=1e-5)

par = np.linspace(0,100, 100)

l = logicleTransform(par, T=100.0, end_lin=1e-5)

l1 = LogicleScale.logicleInverseTransform(l[0], l[1])

l2 = LogicleScale.logicleGradient(l[0], l[1])

l3 = LogicleScale.logicleInverseGradient(1, l[1])
