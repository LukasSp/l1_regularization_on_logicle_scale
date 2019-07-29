"""
    This file contains functions which are used to save the optimization
    and regularization results to a file so we do not need to run the
    code over and over again.

    We save only the most import information which are used to visualize
    the result. Every save function has an input "option", where you can
    define specific option, for example the scale, the parameter,...
    This is usefull to keep the overview.


    result: optimization result from pypesto

    n_start: number of start points which are used for the optimization

    nominal_par: true (optimal) parameter given

    par_names: names of the parameter

    conv_points: The number of the converted points

    comp_time: computation time

    opt_interval: parameter intervall of the optimization

    path: path where the file should be saved
    
"""

import pandas as pd
import numpy as np


# save optimization results
def save_optimization_to_file(result, n_start, nominal_par, par_names, opt_lh, conv_points, comp_time, opt_interval,
                              path, startpoints=None, options = None, file_name=None):

    xs = np.zeros(len(nominal_par) * n_start)
    z = 0
    for i in range(0, n_start):
        if result.optimize_result.as_list('x')[i]['x'] is not None:
            for j in range(0, len(nominal_par)):
                xs[z+j] = result.optimize_result.as_list('x')[i]['x'][j]
            z += len(nominal_par)

    fval = result.optimize_result.get_for_key('fval')
    best_par = result.optimize_result.as_list('x')[0]['x']

    opt_interval_temp = []
    for i in range(len(nominal_par)):
        opt_interval_temp.append(opt_interval[0][i])
    for i in range(len(nominal_par)):
        opt_interval_temp.append(opt_interval[1][i])

    dict = {'n_start': n_start, 'xs': xs, 'fval': fval, 'best_par': best_par, 'nominal_par': nominal_par,
            'par_names': par_names, 'opt_lh': opt_lh, 'conv_points': conv_points, 'comp_time': comp_time,
            'opt_interval': opt_interval_temp, 'startpoints': startpoints, 'options': options}

    df = pd.DataFrame({key: pd.Series(value) for key, value in dict.items()})

    if file_name is None:
        file_name = 'opt_result.csv'

    df.to_csv(path + file_name)


# ______________________________________________________________________________________________________________________


# save model selection results
def save_modelSelection(reg_path, lambda_range, n_lambda, n_sigma, par_names, conv_points, n_starts,
                        path, aic=None, aicc=None, bic=None, options = None, file_name=None):

    reg_path_1 = np.array(reg_path).flatten()

    # different log10 penalization strengths
    lambda_range_log = np.log10(lambda_range)
    lambdas = np.linspace(lambda_range_log[0], lambda_range_log[1], n_lambda)

    dict = {'reg_path': reg_path_1, 'lambdas': lambdas, 'sigma': n_sigma, 'par_names': par_names,
            'conv_points': conv_points, 'n_starts': n_starts, 'aic': aic, 'aicc': aicc, 'bic': bic,
            'options': options}

    df = pd.DataFrame({key: pd.Series(value) for key, value in dict.items()})

    if file_name is None:
        file_name = 'modelSelection_result.csv'

    df.to_csv(path + file_name)

# ______________________________________________________________________________________________________________________


# save best points of optimization to text file which than can
# be used as guesses for the regularization
def save_guesses(result, n_starts, nominal_par, options, path, file_name=None):

    # get index where is the firs None
    none_index = n_starts
    for i in range(0, n_starts):
        if result.optimize_result.as_list('x')[i]['x'] is None:
            none_index = i
            break

    guesses = np.zeros(len(nominal_par) * none_index)
    z = 0
    for i in range(0, none_index):
        if result.optimize_result.as_list('x')[i]['x'] is not None:
            for j in range(0, len(nominal_par)):
                guesses[z+j] = result.optimize_result.as_list('x')[i]['x'][j]
            z += len(nominal_par)

    dict = {'guesses': guesses, 'n_starts': n_starts, 'nominal_par': nominal_par, 'options': options}

    df = pd.DataFrame({key: pd.Series(value) for key, value in dict.items()})

    if file_name is None:
        file_name = 'guesses.csv'

    df.to_csv(path + file_name)


# ______________________________________________________________________________________________________________________


# save start points of an optimization
def save_startpoints(result, path, options=None, file_name=None):

    n_starts = len(result.optimize_result.as_list('x'))
    n_par = len(result.optimize_result.as_list('x')[0]['x'])

    startpoints = np.zeros(n_starts*n_par)
    z = 0
    for i in range(0, n_starts):
        for j in range(0, n_par):
            startpoints[z+j] = result.optimize_result.get_for_key('x0')[i][j]
        z += n_par

    dict = {'startpoints': startpoints, 'n_starts': n_starts, 'n_par': n_par, 'options': options}

    df = pd.DataFrame({key: pd.Series(value) for key, value in dict.items()})

    if file_name is None:
        file_name = 'startpoints.csv'

    df.to_csv(path + file_name)


