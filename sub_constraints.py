def subConstraints(M, y, z, s, m, n, t, nN, et, lt, sd, grid, bigM, df_n, df, gb):
    '''Constraint: every nodes visited once'''
    for i in range(m):
        for j in range(n + 1):
            for k in range(t):
                M.addConstr(gb.quicksum(z[i, j, l, k] for l in range(n + 1)) == y[i, j, k])
                M.addConstr(gb.quicksum(z[i, l, j, k] for l in range(n + 1)) == y[i, j, k])
                for l in range(n + 1):
                    if j == l:
                        if j != 0 and l != 0:
                            M.addConstr(z[i, j, l, k] == 0)
    M.update()
    '''constraints: service start time'''
    for i in range(m):
        for k in range(t):
            for j in range(n):
                for l in range(n):
                    M.addConstr(s[i, j + 1, k] + (sd[j + 1] + grid[j + 1, l]) * z[i, j + 1, l, k] <= s[i, l, k] + bigM * (1 - z[i, j + 1, l, k]))
                    M.addConstr(s[i, j, k] <= bigM * y[i, j, k])
    '''constraint: service start time of patient needing multiple nurses at a same time'''
    for i in range(m):
        for p in range(m):
            for j in range(n):
                for k in range(t):
                    if j != 0 and nN [j] != 1 and i != p:
                        M.addConstr(s[i, j, k] + bigM * (2 - y[i, j, k] - y[p, j, k]) >= s[p, j, k])
                        M.addConstr(s[i, j, k] <= s[p, j, k] + bigM * (2 - y[i, j, k] - y[p, j, k]) )
    M.update()
    '''constraint: nurses' total time available in planning horizon'''
    for i in range(m):
        for j in range(n):
            for l in range(n):
                for k in range(t):
                    M.addConstr(z[i, 0, j + 1, k] * grid[0, j + 1] + s[i, l + 1, k] + (grid[l + 1, 0] + sd[l + 1]) * z[i, l + 1, 0, k] <=
                                df_n["Time"][i] / t + bigM * (1 - z[i, l + 1, 0, k]) + bigM * (1 - z[i, 0, j + 1, k]))
    M.update()
    '''time window'''
    for i in range(m):
        for j in range(n):
            for k in range(t):
                M.addConstr(s[i, j + 1, k] + bigM *(1 - y[i, j + 1, k]) >= et[j + 1])
                M.addConstr(s[i, j + 1, k] + sd[j + 1] - bigM *(1 - y[i, j + 1, k]) <= lt[j + 1])
    M.update()
