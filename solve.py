import pandas as pd
import gurobipy as gb
import numpy as np
import matplotlib.pyplot as plt
import math
import timeit
import distance
import print_solution
import master_constraints
import sub_constraints
import decision_variables
import objective_function

number_of_patients = 100  #30/35/40/50/100

dir = r"data\{}P.xlsx" .format((number_of_patients))
df = pd.DataFrame(pd.read_excel(dir, 'patients'))  # patient data
df_n = pd.DataFrame(pd.read_excel(dir, 'nurses'))  # nurse data
df, df_n = df.fillna(0).astype('int'), df_n.fillna(0).astype('int')
df
df_n
t = 5  # number of days in planning horizon
n = df.shape[0] - 1  # number of patients
f = list(df["f"].astype('int'))  # frequency of visit for every patients
nN = list(df["nN"].astype('int'))  # number of nurses required by each patient
et = list(df["et"].astype('int'))  # earliest service start time for each patient
lt = list(df["lt"].astype('int'))  # latest service start time for each patient
sd = list(df["sd"].astype('int'))  # service duration for each patient
q = list(df["Q'"].astype('int'))  # qulification of first nurse required for each patient
q2 = list(df["Q'2"].astype('int'))  # qulification of second nurse required for each patient
q3 = list(df["Q'3"].astype('int'))  # qulification of third nurse required for each patient
Q = list(df_n["Q"].astype('int'))  # qulification of each nurse
m = df_n.shape[0]  # number of nurses
bigM = 2500  # infinitely large number
X, Y = list(df["x"]), list(df["y"])  # coordinates X and Y of each patient and depot
depot = [X[0], Y[0]]  # depot coordinates

grid = distance.dist(X, Y, bigM)  # get distance matrix

start_time = timeit.default_timer()

M = gb.Model("master_problem")  # initialize the model

d, x, y, z, s = {}, {}, {}, {}, {}  # initialize decision variables

decision_variables.decisionVariables(
    M, gb, m, n, t, d, x, y, z, s)  # add decision variables to model

objective_function.objectiveFunction(
    M, gb, d, n)  # add objective function to model

master_constraints.masterConstraints(
    M, d, x, y, m, n, t, q, q2, q3, Q, nN, f, gb)  # add master constraints to model

# sub_constraints.subConstraints(M, y, z, s, m, n, t, nN, et, lt, sd, grid, bigM, df_n, df, gb)  # add sub constraints to model

M.optimize()  # run optimizer

end_time = timeit.default_timer() - start_time

# get attributes
sol_d, sol_x, sol_y, sol_z, sol_s = \
M.getAttr('x', d), M.getAttr('x', x), M.getAttr('x', y), M.getAttr('x', z), M.getAttr('x', s)

print_solution.printSolution(
    M, sol_d, sol_x, sol_y, sol_z, sol_s, m, n, t, df, df_n, q, f)  # print solution

print('\ntotal time taken for optimization is:\n', end_time)
