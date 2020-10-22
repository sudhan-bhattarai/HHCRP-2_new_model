
def masterConstraints(M, d, x, y, m, n, t, q, q2, q3, Q, nN, f, gb):
    '''constraint 2'''
    for j in range(n):
        if nN[j] == 1:
            M.addConstr(gb.quicksum(x[i, j] for i in range(m)) == d[j])
        else:
            M.addConstr(gb.quicksum(x[i,j] for i in range(m)) == nN[j] * d[j])
    M.update()
    '''constraint 2'''
    for j in range(n):
        if nN[j] == 1:
            M.addConstr(gb.quicksum(gb.quicksum( y[i, j + 1, k] for k in range(t)) for i in range(m)) == f[j] * d[j])
        else:
            M.addConstr(gb.quicksum(gb.quicksum( y[i, j + 1, k] for k in range(t)) for i in range(m)) == nN[j] * f[j] * d[j])
    M.update()
    '''constraint 3'''
    for i in range(m):
        for j in range(n):
            for k in range(t):
                M.addConstr(y[i, j + 1, k] <= x[i, j])
    M.update()
    '''constraint 4'''
    for i in range(m):
        for j in range(n):
            if nN[j] == 1:
                if q[j] != Q[i]:
                    M.addConstr(x[i, j] == 0)
            elif nN[j] == 2:
                if q[j] != Q[i] and q2[j] != Q[i]:
                    M.addConstr(x[i, j] == 0)
            elif nN[j] == 3:
                if q[j] != Q[i] and q2[j] != Q[i] and q3[j] != Q[i]:
                    M.addConstr(x[i, j] == 0)
    M.update()
    '''constraint 5'''
    for i in range(m):
        for k in range(t):
            M.addConstr(y[i, 0, k] == 1)  # j = 0 for depot location
            M.addConstr(y[i, 0, k] == 1)
    M.update()
    '''constraint 6'''
    for i in range(m):
        for j in range(n):
            for k in range(t):
                for p in range(1, (4 - (f[j]) + 1)):
                    if (k + p) <= 4:
                        M.addConstr(y[i, j + 1, k] + y[i, j + 1, k + p] <= 1)
    M.update()
