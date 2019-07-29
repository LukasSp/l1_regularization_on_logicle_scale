# l1 regularization

With this script you can perform model reduction for ODE using l1 regularization. The corresponding ODE model should be given in PEtab format.



- regularization: contains the l1 regularization routine. The algorithm contains two parts:

                  1. Initialize the regularization: here you define general settings for the l1 regularization, e.g. which parameter    scale, which parameters get penalized, penalization interval, number of penalizations...
                  
                  2. call the initalize regularization: by calling the inilization object means you optimize all the objective function corresponding to the respective penalization. Here you can define how many startin gpoints, optimization method, ....
                  
- l1_regularization_computation: Contains function which are necessary to compute different results of the regularization algorithm, e.g. the regularization path, AIC, AICC, BIC, ....

- l1_regularization_visualize: contains routines to visualize the regularization results
