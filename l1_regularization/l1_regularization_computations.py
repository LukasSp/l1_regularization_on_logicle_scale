''''
    Routines for plotting results from
    the L1 model selection
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import ticker, cm

# CALCULATE CONVERTED POINTS ___________________________________________________________________________________________


def compute_converged_points_single(result, threshold=None):

    # threshold at which two points are assumed to
    # be "equal" (converged)
    if threshold is None:
        threshold = 1e-2

    # get the best result
    best_result = result.optimize_result.as_list('x')[0]['x']

    n_starts = len(result.optimize_result.as_list('x'))

    # compare best result with all other results
    # |best_result - other_result| < threshold
    conv_points = 0
    for i in range(0, n_starts):

        other_result = result.optimize_result.as_list('x')[i]['x']

        if other_result is not None:
            converged = (np.abs((other_result - best_result)) < (threshold * len(other_result))).all()

            if converged:
                conv_points += 1

    return conv_points


def compute_converged_points(result_list, threshold=None):

    convergence_list = []

    for i in range(0, len(result_list)):
        temp = compute_converged_points_single(result=result_list[i], threshold=threshold)

        convergence_list.append(temp)

    return convergence_list


# COMPUTE REGULARIZATION PATH __________________________________________________________________________________________

# the regularization path contains the value of every parameter
# along the penalization strength


def compute_regularization_path(result_list, lambda_range, n_lambda, n_sigma=None):

    # different log10 penalization strengths
    lambda_range_log = np.log10(lambda_range)
    lambdas = -np.linspace(lambda_range_log[0], lambda_range_log[1], n_lambda)[::-1]

    if n_sigma is None:
        n_sigma = 0

    parameter_list = []
    for i in range(0, len(result_list[0].optimize_result.as_list('x')[0]['x']) - n_sigma):
        parameter = []

        for j in range(0, len(result_list)):
            result_list[j].optimize_result.sort()
            parameter.append(result_list[j].optimize_result.as_list('x')[0]['x'][i])

        # add zeros to the end for non optimized results
        j = 0
        while len(result_list) + j < len(lambdas):
            parameter.append(0.0)
            j += 1

        parameter_list.append(parameter)

    return parameter_list

# COMPUTE AIC, AICc, BIC _______________________________________________________________________________________________

def compute_aic(obj, par, n_par):
    return 2 * obj(par) + 2 * n_par

def compute_aicc(obj, par, n_par, n_data, sample_size=None):
    return 2 * obj(par) + 2 * n_par + 2 * n_par * (n_par + 1) / (n_data - n_par - 1)

def compute_bic(obj, par, n_par, n_data):
    return 2 * obj(par) + n_par * np.log(n_data)

# compute aic, aicc, bic along the regularization path
# for every optimal parameter
# ms_criteria = 'AIC' or 'AICC', or 'BIC'
def compute_model_selection_criteria(result_list, objective, ms_criteria, n_data=None):

    ms_list = []

    for i in range(0, len(result_list)):

        best_par = result_list[i].optimize_result.as_list('x')[0]['x']

        # compute number of parameter unequal to 0
        if isinstance(best_par, list):
            best_par = np.array(best_parpar)

        n_par = len(best_par[best_par > 0])

        # compute ms criteria
        if ms_criteria == 'AIC':
            aic = compute_aic(obj=objective, par=best_par, n_par=n_par)
            ms_list.append(aic)

        if ms_criteria == 'AICC':
            aicc = compute_aicc(obj=objective, par=best_par, n_par=n_par, n_data=n_data)
            ms_list.append(aicc)

        if ms_criteria == 'BIC':
            bic = compute_bic(obj=objective, par=best_par, n_par=n_par, n_data=n_data)
            ms_list.append(bic)

    return ms_list
