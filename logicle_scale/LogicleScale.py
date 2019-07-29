"""
This is the main script containing all functions which are needed
to transform your parameters into logicle scale
"""

import numpy as np
import Logicle


# definition of a logicle object which contains all
# parameters of the logicle scale
class LogicleObject:

    def __init__(self, T, end_lin=None, W=None, M=None, A=None):

        self.T = T
        self.end_lin = end_lin

        # computation of the original input parameters
        # given T and end_lin
        if W is None:
            W = 0.5
        self.W = W

        if A is None:
            A = -self.W
        self.A = A

        if M is None:
            M = compute_M(self.T, self.end_lin)
        self.M = M

    @property
    def get_T(self):
        return self.T

    def get_W(self):
        return self.W

    def get_M(self):
        return self.M

    def get_A(self):
        return self.A

    def get_end_lin(self):
        return self.end_lin


# function to transfom your par
def logicleTransform(par, T, end_lin=None, W=None, M=None, A=None):

    # compute input parameters
    if W is None:
        W = 0.5

    if A is None:
        A = -W

    if M is None:
        M = compute_M(T, end_lin)

    # store the 4 parameters in a logicle object
    logicle_object = LogicleObject(T=T, W=W, M=M, A=A, end_lin=end_lin)

    # initialize swig object which is necessary to
    # compute the logicle parameter
    logicle_object_swig = Logicle.Logicle(T, W, M, A)

    # initialize logicle parameter
    logicle_par = np.zeros(len(par))

    # transform your parameter into logicle
    for i in range(0, len(par)):
        logicle_par[i] = logicle_object_swig.scale(value=par[i])

    return [logicle_par, logicle_object]


# inverse function to transform your parameters back
def logicleInverseTransform(par, logicle_object):

    # get the swig object from the logicle object
    logicle_object_swig = get_swig_object(logicle_object)

    # initialize inverse logicle par
    inv_logicle_par = np.zeros(len(par))

    # transform your parameters
    for i in range(0, len(par)):
        inv_logicle_par[i] = logicle_object_swig.inverse(scale=par[i])

    return inv_logicle_par


# compute gradient with center finite differences
def logicleGradient(par, logicle_object):

    stepsize = 1e-5

    grad_logicle = np.zeros(len(par))

    T = logicle_object.get_T
    W = logicle_object.get_W()
    M = logicle_object.get_M()
    A = logicle_object.get_A()

    for i in range(0, len(par)):

        logclePlus = logicleTransform(np.array([par[i]]) + stepsize, T=T, W=W, M=M, A=A)
        logcleMinus = logicleTransform(np.array([par[i]]) - stepsize, T=T, W=W, M=M, A=A)
        grad_logicle[i] = (logclePlus[0] - logcleMinus[0]) / (2 * stepsize)

    return grad_logicle


# compute inverse gradient
def logicleInverseGradient(par, logicle_object):

    # compute swig object
    logicle_object_swig = get_swig_object(logicle_object)

    # compute the 4 parameters which are needed
    # see paper
    a = logicle_object_swig.a()
    b = logicle_object_swig.b()
    c = logicle_object_swig.c()
    d = logicle_object_swig.d()

    if isinstance(par, list):
        par = np.array(par)

    return a * b * np.exp(b * par) + c * d * np.exp(-d * par)


# function for computing the input parameter
# M from T and end_lin
def compute_M(T, end_lin):

    # numerical solving the equation
    from scipy.optimize import newton
    W = 0.5
    f = lambda M: W / logicleTransform([end_lin], T=T, W=W, M=float(M), A=-W)[0][0] + W - M

    # use newton solver to find root of f
    M = newton(f, 3.0, tol=1e-3, maxiter=100)

    return M


# compute swig object from a logicle object
# needed for transformation
def get_swig_object(logicle_object):

    T = logicle_object.get_T
    W = logicle_object.get_W()
    M = logicle_object.get_M()
    A = logicle_object.get_A()

    logicle_object_swig = Logicle.Logicle(T, W, M, A)

    return logicle_object_swig
