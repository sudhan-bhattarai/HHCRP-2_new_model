import pandas as pd
import gurobipy as gb
import numpy as np
import matplotlib.pyplot as plt
import math
import distance
import print_solution
import master_constraints
import sub_constraints
import decision_variables
import objective_function

df = pd.DataFrame(pd.read_excel(r'sample_data.xlsx', 'patients'))  # patient data
df_n = pd.DataFrame(pd.read_excel(r'sample_data.xlsx', 'nurses'))  # nurse data
m = 3  # number of nurses
t = 5  # number of days in planning horizon
n = df.shape[0] - 1  # number of patients
f = list(df["f"][1:].astype('int'))  # frequency of visit for every patients
nN = list(df["nN"][1:].astype('int'))  # number of nurses required by each patient
et = list(df["et"].astype('int'))  # earliest service start time for each patient
lt = list(df["lt"].astype('int'))  # latest service start time for each patient
sd = list(df["sd"].astype('int'))  # service duration for each patient
q = list(df["Q'"][1:].astype('int'))  # qulification of first nurse required for each patient
q2 = list(df["Q'2"][1:].astype('int'))  # qulification of second nurse required for each patient
q3 = list(df["Q'3"][1:].astype('int'))  # qulification of third nurse required for each patient
Q = list(df_n["Q"].astype('int'))  # qulification of each nurse
bigM = 1000000  # infinitely large number
X, Y = list(df["x"]), list(df["y"])  # coordinates X and Y of each patient and depot
depot = [X[0], Y[0]]  # depot coordinates

grid = distance.dist(X, Y, bigM)  # get distance matrix

M = gb.Model("master_problem")  # initialize the model

d, x, y, z, s = {}, {}, {}, {}, {}  # initialize decision variables

decision_variables.decisionVariables(
    M, gb, m, n, t, d, x, y, z, s)  # add decision variables to model

objective_function.objectiveFunction(
    M, gb, d, n)  # add objective function to model

master_constraints.masterConstraints(
    M, d, x, y, m, n, t, q, q2, q3, Q, nN, f, gb)  # add master constraints to model

sub_constraints.subConstraints(
    M, y, z, s, m, n, t, nN, et, lt, sd, grid, bigM, df_n, df, gb)  # add sub constraints to model

M.optimize()  # run optimizer

# get attributes
sol_d, sol_x, sol_y, sol_z, sol_s =
    M.getAttr('x', d), M.getAttr('x', x), M.getAttr('x', y), M.getAttr('x', z), M.getAttr('x', s)

print_solution.printSolution(
    M, sol_d, sol_x, sol_y, sol_z, sol_s, m, n, t, df, df_n, q, f)  # print solution
