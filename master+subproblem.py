import pandas as pd
import gurobipy as gb
import numpy as np
import matplotlib.pyplot as plt
import math

df = pd.DataFrame(pd.read_excel(r'sample_data.xlsx', 'patients'))
df_n = pd.DataFrame(pd.read_excel(r'sample_data.xlsx', 'nurses'))

'''number of nurses, patients, days, frequency of visit, service duration & qualification'''
m = 3  # number of nurses
t = 5  # number of days in planning horizon
n = df.shape[0]  # number of patients
f = list(df["f"].astype('int'))  # frequency of visit for every patients
et = list(df["et"].astype('int'))
lt = list(df["lt"].astype('int'))
sd = list(df["sd"].astype('int'))
q = list(df["Q'"].astype('int'))
Q = list(df_n["Q"].astype('int'))

''' coordinates X and Y of each patient and depot'''
X,Y = list(df["x"]), list(df["y"])
depot = [X[0], Y[0]]

'''distance grid'''

def dist(x = [],y = []):
    dist_grid = np.empty([len(x),len(y)])
    for i in range(len(x)):
        for j in range(len(y)):
            if i == j:
                dist_grid [i,j] = 1000
            else:
                dist_grid[i,j] = math.sqrt( (x[i]-x[j])**2 + (y[i]-y[j])**2 )
    return dist_grid
grid = dist(X,Y)

'''Initialize the model'''
M = gb.Model("master_problem")

''' decision variable: delta '''
d = {}
for i in range(n):
    d[i] = M.addVar(vtype=gb.GRB.BINARY, name = "d%d" %(i))
M.update()

'''decision variable x'''
x = {}
for i,j in zip(range(m),range(n)):
        x[i,j] = M.addVar(vtype = gb.GRB.BINARY, name = 'x%d,%d' %(i,j))
M.update()

'''decision variable y'''
y = {}
for i,j,k in zip(range(m),range(n),range(t)):
    y[i,j,k] = M.addVar(vtype = gb.GRB.BINARY, name = 'y%d,%d,%d' %(i,j,k))
M.update()

'''variable z'''
z = {}
for i in range(m):
    for j in range(n):
        for l in range(n):
            for k in range(t):
                z[i,j,l,k] = M.addVar(vtype = gb.GRB.BINARY, name = "z%d,%d,%d,%d" %(i,j,l,k))
M.update()

'''variable s'''
s = {}
for i in range(m):
    for j in range(n):
        for k in range(t):
            s[i,j,k] = M.addVar(vtype = gb.GRB.CONTINUOUS, name = "s%d,%d,%d" %(i,j,k))
M.update()

'''objective funtion - 1'''
M.setObjective(gb.quicksum(d[j] for j in range(n)), gb.GRB.MAXIMIZE)
M.update()

'''constraint 2'''
for j in range(n-1):
    M.addConstr(gb.quicksum(x[i,j+1] for i in range(m)) == d[j+1])
M.update()

'''constraint 2'''
for j in range(n-1):
    M.addConstr(gb.quicksum(gb.quicksum(y[i,j+1,k] for k in range(t)) for i in range(m)) == f[j+1]*d[j+1])
M.update()

'''constraint 3'''
for i in range(m):
    for j in range(n-1):
        for k in range(t):
            M.addConstr(y[i,j+1,k] <= x[i,j+1])
M.update()

'''constraint 4'''
for i in range(m):
    for j in range(n-1):
        if q[j+1] != Q[i]:
            M.addConstr(x[i,j+1] == 0)
M.update()

'''constraint 5'''
for i in range(m):
    for k in range(t):
        M.addConstr(y[i,0,k] == 1)  # j = n for depot location
        M.addConstr(y[i,0,k] == 1)
M.update()

'''constraint 6'''
for i in range(m):
    for j in range(n-1):
        for k in range(t):
            for p in range(1, (4-(f[j+1]) + 1)):
                if (k+p) <= 4:
                    M.addConstr(y[i,j+1,k] + y[i,j+1,k+p] <= 1)
M.update()

'''Sub Problem'''
# '''Constraint: every nodes visited once'''
# for i in range(m):
#     for j in range(n+1):
#         for k in range(t):
#             M.addConstr(gb.quicksum(z[i,j,l,k] for l in range(n+1)) == y[i,j,k])
#             M.addConstr(gb.quicksum(z[i,l,j,k] for l in range(n+1)) == y[i,j,k])
#             for l in range(n+1):
#                 if j == l:
#                     if j != 0 and l != 0:
#                         M.addConstr(z[i,j,l,k] == 0)
# M.update()
#
# '''constraints: service start time'''
# for i in range(m):
#     for k in range(t):
#         for j in range(n):
#             for l in range(n):
#                 M.addConstr(s[i,j+1,k] + (sd[j+1] + grid[j+1,l+1])*z[i,j+1,l+1,k] \
#                 <= s[i,l+1,k] + 10000*(1-z[i,j+1,l+1,k]))
# M.update()
#
# '''constraint: nurses' total time available ia planning horizon'''
# for i in range(m):
#     None
#     # M.addConstr(gb.quicksum(gb.quicksum()))
# M.update()
#
# '''time window'''
# for i in range(m):
#     for j in range(n):
#         for k in range(t):
#             M.addConstr(s[i,j+1,k] + 10000 * (1 - y[i,j+1,k]) >= et[j+1])
#             M.addConstr(s[i,j+1,k] + sd[j+1] - 10000 * (1 - y[i,j+1,k]) <= lt[j+1])
# M.update()
#
'''run optimizer'''
M.optimize()
#
# '''print solution'''
solution_d, solution_x, solution_y = M.getAttr('x', d), M.getAttr('x', x), M.getAttr('x', y)
var_d, var_x, var_y = np.empty([n]), np.empty([m,n]), np.empty([m,n,t])
for i in range(m):
    for j in range(n):
        var_d[j] = solution_d[j]
        var_x[i,j] = solution_x[i,j]
for i in range(m):
    for j in range(n):
        for k in range(t):
            var_y[i,j,k] = solution_y[i,j,k]
print('\nnodes\n',df.head(), '\nnurses\n',df_n.head(),'\nobj\n',int(M.objVal),\
'\nq\n',q,'\nf\n',f,'\nd\n',var_d, '\nx\n', var_x, '\ny\n',var_y)# ,'\n\ns',var_s, '\nz\n', var_z[2,:,:,4])
