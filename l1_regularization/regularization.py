"""
    This script contains the whole l1 regularization
"""

import numpy as np
import pypesto
from save_functions import save_optimization_to_file


class l1_regularization:

    """
        inputs:

        model: model defined by petab import

        petab_problem: petab problem

        objective: the objctive function of the problem

        scale_list: list with the parameter scales
                    ['logicle', 'logicle',...]

        estimate_list: list containing 0 and 1. By l1 regularization we do
                       not peanlize the noise, therefore there should be 0

        lambda_range: interval where my penalization strength lambda
                      e.g. [10, 100]

        n_lambda: number (integer) of how many penalization strength
                  chosen in the interval lambda range. We use equidistant
                  lambdas

        optional

        logicle_object: if you use logicle Scale than you have to give
                        the coresponding logcile object as input

        shift par: if you use the shifted logarithmic scale here you
                   can specify the value of epsilon
    """

    def __init__(self,
                 model,
                 petab_problem,
                 objective,
                 scale_list,
                 estimate_list,
                 lambda_range,
                 n_lambda,
                 logicle_obj=None,
                 shift_par=None):

        self.model = model
        self.petab_problem = petab_problem
        self.scale_list = scale_list
        self.estimate_list = estimate_list
        self.lambda_range = lambda_range
        self.n_lambda = n_lambda
        self.n_estimate = sum(estimate_list)
        self.objective = objective
        self.logicle_obj = logicle_obj
        self.shift_par = shift_par

        # l1 regularization is achieved by using laplacian
        # priors
        priorType_list = ['lap'] * len(scale_list)

        # calculate a list of priors corresponidng to
        # all penalization strengths
        prior_list = multiple_prior(model=self.model,
                                    priorType_list=priorType_list,
                                    scale_list=self.scale_list,
                                    estimate_list=self.estimate_list,
                                    lambda_range=self.lambda_range,
                                    n_lambda=self.n_lambda,
                                    logicle_object=self.logicle_obj,
                                    shift_par=self.shift_par)

        self.prior_list = prior_list

        # for all priors calculate the corresponding objective
        # function and store them in a list
        objecitve_list = multiple_objective(obj=self.objective,
                                            prior_list=self.prior_list)

        self.objective_list = objecitve_list

    # call regularization
    # optimize all objective functions
    def __call__(self,
                 n_starts,
                 x_guesses=None,
                 opt_method=None,
                 opt_options=None,
                 par_names=None,
                 option_stop=False,
                 threshold=None,
                 path=None):

        # if option_stop=True than a parameter smaller than the threshold is
        # set to 0 for all future optimizations

        # optimite multiple objecives
        result_list = multiple_optimization(petab_problem=self.petab_problem,
                                            objective_list=self.objective_list,
                                            n_starts=n_starts,
                                            n_estimate=self.n_estimate,
                                            threshold=threshold,
                                            x_guesses=x_guesses,
                                            par_names=par_names,
                                            path=path)

        return result_list


# ______________________________________________________________________________________________________________________


# function to generate multiple priors corresponding
# to all the different penalization strnegths
def multiple_prior(model,
                   priorType_list,
                   priorParameters_list=None,
                   scale_list=None,
                   estimate_list=None,
                   lambda_range=None,
                   n_lambda=None,
                   logicle_object=None,
                   shift_par=None):

    # define all the laplace prior parameters for the different lambdas
    # lambda_range_log = [np.log10(lambda_range[1]), np.log10(lambda_range[0])]
    # print(lambda_range_log)

    # reverse lambda: l = 1/b
    # lambda_log = np.linspace(lambda_range_log[0], lambda_range_log[1], n_lambda)

    lambda_range_log = [np.log10(lambda_range[0]), np.log10(lambda_range[1])]
    lambda_log = -np.linspace(lambda_range_log[0], lambda_range_log[1], n_lambda)

    priorParameters_list = []
    for i in range(0, n_lambda):
        parameters = [[0, 10**lambda_log[i]]] * len(model.getParameters())
        priorParameters_list.append(parameters)

    #print(priorParameters_list)
    prior_list = []

    for par in range(0, n_lambda):
        prior = pypesto.Prior(priorType_list=priorType_list,
                              priorParameters_list=priorParameters_list[par],
                              scale_list=scale_list,
                              estimate_list=estimate_list,
                              logicle_object=logicle_object,
                              shift_par=shift_par)
        prior_list.append(prior)

    return prior_list


def multiple_objective(obj, prior_list, importer=None):

    # generate objective function from the model
    #obj = importer.create_objective()

    # calculate the objective functions for the different priors
    objective_list = []
    for prior in range(0, len(prior_list)):
        objective = pypesto.Objective(fun=obj.get_fval, grad=obj.get_grad, prior=prior_list[prior])
        objective_list.append(objective)

    return objective_list


def multiple_optimization(petab_problem,
                          objective_list,
                          n_starts,
                          x_guesses=None,
                          opt_method=None,
                          opt_options=None,
                          par_names=None,
                          option_stop=False,
                          threshold=None,
                          n_estimate=None,
                          path=None):

    import pypesto

    result_list = []
    x_fixed_indices = []
    x_fixed_vals = []

    if opt_method is None:
        opt_method = 'L-BFGS-B'

    if threshold is None:
        threshold = 1e-10

    if n_estimate is None:
        n_estimate = len(petab_problem.x_nominal)

    for obj in range(0, len(objective_list)):

        optimizer = pypesto.ScipyOptimizer(method=opt_method)
        optimizer.options = opt_options

        if option_stop:

            problem = pypesto.problem.Problem(objective=objective_list[obj],
                                              lb=petab_problem.lb,
                                              ub=petab_problem.ub,
                                              x_fixed_vals=x_fixed_vals,
                                              x_fixed_indices=x_fixed_indices,
                                              x_guesses=x_guesses)
        else:

            problem = pypesto.problem.Problem(objective=objective_list[obj],
                                              lb=petab_problem.lb,
                                              ub=petab_problem.ub,
                                              x_guesses=x_guesses)

        # engine = pypesto.SingleCoreEngine()
        engine = pypesto.MultiProcessEngine()

        # do the optimization
        result = pypesto.minimize(problem=problem,
                                  optimizer=optimizer,
                                  n_starts=n_starts,
                                  engine=engine)

        print('result', obj, '=', result)
        print('best result = ', result.optimize_result.as_list('x')[0]['x'])


        # if option_stop=True, than fix the parameters
        if option_stop:
            print('hier')
            # set small values to 0 and fix them
            best_result = result.optimize_result.as_list('x')[0]['x']
            best_result[best_result < threshold] = 0

            x_fixed_indices = np.where(best_result == 0)[0]

            if len(x_fixed_indices):
                x_fixed_vals = [0] * len(x_fixed_indices)

            if len(x_fixed_indices) == n_estimate:
                result_list.append(result)
                break

        # get the best results as startpoints of the next optimization
        x_guesses = []
        for i in range(0, n_starts):
            temp = result.optimize_result.as_list('x')[i]['x']
            if temp is not None:
                x_guesses.append(temp)

        # save result
        if path is not None:

            file_name = 'result_' + str(obj)
            save_optimization_to_file(result=result,
                                      n_start=n_starts,
                                      nominal_par=petab_problem.x_nominal,
                                      par_names=par_names,
                                      opt_lh=objective_list[obj](petab_problem.x_nominal),
                                      conv_points=0,
                                      comp_time=0,
                                      opt_interval=[problem.lb, problem.ub],
                                      options='modelSelection run:' + str(obj),
                                      path=path,
                                      file_name=file_name)

        # append result to list
        result_list.append(result)

    return result_list
