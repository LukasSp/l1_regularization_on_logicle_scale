"""
    Routines to visualize results from the
    l1 regularization
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl



# PLOT REGULARIZATION PATH _____________________________________________________________________________________________


def plot_regularization_path(reg_path, lambdas, parameter_names, n_sigma=None):
    for i in range(0, len(reg_path)):
        plt.plot(lambdas, reg_path[i], label=parameter_names[i])

    plt.xlabel('$\log_{10}(\lambda)$')
    plt.ylabel('parameter value')
    plt.legend()
    plt.show()


# PLOT REGULARIZATION BARS _____________________________________________________________________________________________


# this function calculates the bars and
# sets values smaller than a threshold to zero
def calculate_broken_barhplot(reg_path, threshold):

    xranges = []
    x_binary_list = []
    indices_list = []

    for i in range(len(reg_path)):

        # convert to array and set all elements
        # below threshold to 0 and all elements
        # above threshold to 1
        x_binary = np.array(reg_path[i])

        if threshold == 0.0:
            x_binary[x_binary == threshold] = 0
            x_binary[x_binary > threshold] = 1
        else:
            x_binary[x_binary < threshold] = 0
            x_binary[x_binary >= threshold] = 1

        # calculate the length of the 1 sequences
        # (= elements above threshold)
        import itertools as it
        length = [len(list(g)) for k, g in it.groupby(x_binary) if k > 0]

        # calculate the first index of every
        # sequence
        x_nonzero = np.nonzero(x_binary)[0]

        if x_nonzero != []:
            indices = [x_nonzero[0]]
            first_index = 0 # x_nonzero[0]
            for i in range(len(length) - 1):
                first_index += length[i]
                indices.append(x_nonzero[first_index])
        else:
            indices = np.arange(0, len(reg_path[0]), 1)

        # store indices and lengths as tuple
        a = list(zip(indices, length))
        xranges.append(a)
        x_binary_list.append(x_binary)
        indices_list.append(indices)

    return [xranges, x_binary_list, indices_list]


# plot the bar plot

def plot_regularization_bars(reg_path,
                             lambdas,
                             threshold,
                             par_names,
                             ax,
                             opt_lambda=None,
                             v_min=None,
                             v_max=None,
                             cb_ticks=None):

    """
       reg_path: regularization path (compute_reg_path)

       lambda_range: penalization interval, e.g. [0, 100]

       n_lambda: number of penalizations

       threshold: all values smaller than the threshold are set to 0

       ax: axis for the plot

       opt_lambda: optimal penalization strengt, e.g. the penalization
                   strength which has the smalles regularized AIC/BIC

       v_min: lower bound of the colorbar

       v_max: upper bound of the colorbar

       cb_ticks: ticks of the colorbar

    """

    if v_min is None:
        v_min = 0

    if v_max is None:
        v_max = 1


    # compute the interval of one stripe
    interval = np.abs(lambdas[0] - lambdas[1])

    # claculate the bars
    bars = calculate_broken_barhplot(reg_path=reg_path, threshold=threshold)[0]

    # compute the color gradients
    grad = []
    for i in range(0, len(reg_path)):
        grad.append(np.atleast_2d(reg_path[i]))

    for par in range(len(bars)):

        #default heigth
        h = 0.8
        # y coordinate of the bar in reverse order
        y = len(bars) - 1 - par

        # plot empty bars for black edges in reverse order
        # and center them

        t = []
        for i in range(0, len(np.array(bars[par]))):
            s = [np.array(bars[par])[i][0] * interval - interval/2, np.array(bars[par])[i][1]*interval]
            t.append(s)

        ax.broken_barh(t , (y - h / 2, h), color='none',
                       edgecolor='black')

        # fill in bars with gradient
        for bar in range(len(bars[par])):

            # x coordinate
            x = bars[par][bar][0]

            # with of bar
            w = bars[par][bar][1]

            # calculate gradient for explicit bar
            g = [grad[par][0][x:x+w]]

            # shift intervall into lambda range
            # plot gradient
            ax.imshow(g, extent=[x*interval-interval/2, interval*(x+w)-interval/2, y-h/2, y+h/2],
                       aspect="auto", zorder=0, cmap='Blues', vmin=v_min, vmax=v_max)


    # plot optimal penalization strength when given
    if opt_lambda is not None:
        ax.vlines(lambdas[opt_lambda] - lambdas[0] + interval/2, -1, len(par_names)+1, color='red', linestyles='dashed')

    # define axis
    ax.set_xlim(-interval/2, abs(lambdas[-1]) + abs(lambdas[0])+ interval/2)
    ax.set_ylim((-1, len(par_names)))
    ax.set_xticks(np.arange(0, abs(lambdas[-1]) + abs(lambdas[0])+ 1, step=1))
    ax.set_xticklabels(np.arange(lambdas[0], lambdas[-1] + 1, step=1))
    ax.set_yticks(np.arange(0, len(par_names), step=1))
    ax.set_yticklabels(par_names[::-1])
    ax.set_xlabel('$\log_{10}(\lambda)$')
    ax.set_ylabel('parameter name')


    # plot colorbar
    norm = mpl.colors.Normalize(vmin=0, vmax=v_max)
    sm = plt.cm.ScalarMappable(cmap='Blues', norm=norm)
    sm.set_array([])
    if cb_ticks is None:
        plt.colorbar(sm, ax=ax)#, ticks = [0, 1], boundaries=[0,1], ax=ax)
    else:
        plt.colorbar(sm, ax=ax, ticks = cb_ticks)#  boundaries=[0,1], ax=ax)

    return ax

# PLOT NUMBER_____________________________________________________________________________________________

def plot_number_of_parameters(reg_path, lambdas, threshold, ax,  opt_lambda=None):


    bars = calculate_broken_barhplot(reg_path=reg_path, threshold=threshold)[1]

    # number of nonzero parameters
    num_par = np.count_nonzero(bars, axis=0)

    ax.step(lambdas, num_par)

    if opt_lambda is not None:
        ax.vlines(lambdas[opt_lambda], 0, len(reg_path), color='red', linestyles='dashed', label='min AIC')

    ax.set_ylabel('Number of non-zero parameters')
    ax.set_xlabel('$\log_{10}(\lambda)$')
    ax.set_yticks(np.arange(0, len(reg_path)+1))

    return ax

