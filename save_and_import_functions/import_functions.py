import pandas as pd
import numpy as np


# function to import optimization results
# output: dictionary
def import_optimization_results(df):

    data = pd.read_csv(df)
    n_start = data['n_start'].values
    xs = data['xs'].values
    fval = data['fval'].values
    best_par = data['best_par'].values
    nominal_par = data['nominal_par']
    par_names = data['par_names'].values
    opt_lh = data['opt_lh'].values
    conv_points = data['conv_points'].values
    comp_time = data['comp_time'].values
    opt_interval = data['opt_interval'].values
    try:
        startpoints = data['startpoints'].values
    except:
        startpoints = None
    options = data['options'].values

    return {'n_start': n_start, 'xs': xs, 'fval': fval, 'best_par': best_par, 'nominal_par': nominal_par,
            'par_names': par_names, 'opt_lh': opt_lh, 'conv_points': conv_points, 'comp_time': comp_time,
            'opt_interval': opt_interval, 'startpoints': startpoints, 'options': options}


# function for regularization results
# output dictionary
def import_modelSelection_results(df):

    data = pd.read_csv(df)

    reg_path = data['reg_path'].values
    lambdas = data['lambdas'].values
    sigma = data['sigma'].values
    par_names = data['par_names'].values
    conv_points = data['conv_points'].values
    n_starts = data['n_starts'].values
    try:
        aic = data['aic'].values
        aicc = data['aicc'].values
        bic = data['bic'].values
    except:
        aic = None
        aicc = None
        bic = None
    options = data['options'].values

    return {'reg_path': reg_path, 'lambdas': lambdas, 'sigma': sigma, 'par_names': par_names,
            'conv_points': conv_points, 'n_starts': n_starts, 'aic': aic, 'aicc': aicc, 'bic': bic,
            'options': options}


# import function which returns the results
def import_results(file_name):
    import_opt = import_modelSelection_results(file_name)
    lambdas = import_opt['lambdas'][~np.isnan(import_opt['lambdas'])]
    sigma = import_opt['sigma'][0]
    par_names_temp = import_opt['par_names']
    par_names_index = [i for i, y in enumerate(par_names_temp) if y is not np.nan]
    par_names = par_names_temp[par_names_index]
    conv_points = import_opt['conv_points'][:len(lambdas)]
    n_starts = import_opt['n_starts'][0]
    options = import_opt['options'][0]

    print(options)

    reg_path_temp = import_opt['reg_path']
    reg_path =[]
    z = 0
    for i in range(0, len(par_names)):
        temp = []
        for j in range(0, len(lambdas)):
            temp.append(reg_path_temp[z+j])
        reg_path.append(temp)
        z += len(lambdas)

    return [reg_path, lambdas, par_names, conv_points]


# import all best parameters along the penalization strength
def import_best_parameter_along_lambda(file_name):

    import_opt = import_modelSelection_results(file_name)
    lambdas = import_opt['lambdas'][~np.isnan(import_opt['lambdas'])]
    par_names_temp = import_opt['par_names']
    par_names_index = [i for i, y in enumerate(par_names_temp) if y is not np.nan]
    par_names = par_names_temp[par_names_index]

    reg_path_temp = import_opt['reg_path']
    reg_path = []
    index = 0
    for i in range(0, len(par_names)):
        temp = []
        for j in range(0, len(lambdas)):
            temp.append(reg_path_temp[index + j])
        reg_path.append(temp)
        index += len(lambdas)

    parameter_list = []
    for i in range(0, len(lambdas)):
        temp = []
        for j in range(0, len(par_names)):
            temp.append(reg_path[j][i])
        parameter_list.append(temp)

    return parameter_list


# function to import start point guesses
# output
def import_guesses(df):

    data = pd.read_csv(df)

    n_starts = int(data['n_starts'].values[0])
    nominal_par = data['nominal_par'].values[~np.isnan(data['nominal_par'])]
    options = data['options'].values[0]

    guesses_temp = data['guesses'].values  # [:(n_starts * len(nominal_par))]

    len_temp = len(guesses_temp) / len(nominal_par)

    guesses = np.zeros((int(len_temp), len(nominal_par)))
    z = 0
    for i in range(0, int(len_temp)):
        for j in range(0, len(nominal_par)):
            guesses[i, j] = guesses_temp[z + j]
        z += len(nominal_par)

    return [guesses, n_starts, options]


#_______________________________________________________________________________________________________________________

# function to import start points
def import_startpoints(df):

    data = pd.read_csv(df)

    n_starts = int(data['n_starts'].values[0])
    n_par = int(data['n_par'].values[0])
    options = data['options'].values[0]

    startpoints_temp = data['startpoints'].values

    len_temp = len(startpoints_temp) / n_par

    startpoints = np.zeros((int(len_temp), n_par))
    z = 0
    for i in range(0, int(len_temp)):
        for j in range(0, n_par):
            startpoints[i, j] = startpoints_temp[z + j]
        z += n_par

    return startpoints