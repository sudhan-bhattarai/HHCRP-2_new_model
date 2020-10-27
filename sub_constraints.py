def subConstraints(M, y, z, s, m, n, t, nN, et, lt, sd, grid, bigM, df_n, df, gb):

    for i in range(m):
        for j in range(n + 1):
            for k in range(t):
                '''every node visited once'''
                M.addConstr(gb.quicksum(z[i, j, l, k] for l in range(n + 1)) == y[i, j, k])
                M.addConstr(gb.quicksum(z[i, l, j, k] for l in range(n + 1)) == y[i, j, k])

                '''time window'''
                if j <= n-1:
                    M.addConstr(s[i, j + 1, k] + bigM *(1 - y[i, j + 1, k]) >= et[j + 1])
                    M.addConstr(s[i, j + 1, k] + sd[j + 1] - bigM *(1 - y[i, j + 1, k]) <= lt[j + 1])

                '''ommiting a loop inside a node'''
                if j != 0:
                    M.addConstr(z[i, j, j, k] == 0)

                '''service start time of patient needing multiple nurses at a same time'''
                if j <= n-1:
                    for p in range(m):
                        if nN [j+1] != 1 and i != p:
                            M.addConstr(s[i, j+1, k] + bigM * (2 - y[i, j+1, k] - y[p, j+1, k]) >= s[p, j+1, k])
                            M.addConstr(s[i, j+1, k] <= s[p, j+1, k] + bigM * (2 - y[i, j+1, k] - y[p, j+1, k]) )
    M.update()

    for i in range(m):
        for j in range(n):
            for l in range(n):
                for k in range(t):

                    '''service start time'''
                    M.addConstr(s[i, j, k] <= bigM * y[i, j, k])

                    '''nurses' total time available in planning horizon'''
                    M.addConstr(z[i, 0, j + 1, k] * grid[0, j + 1] + s[i, l + 1, k] + (grid[l + 1, 0] + sd[l + 1]) * z[i, l + 1, 0, k] <=
                                df_n["Time"][i] / t + bigM * (1 - z[i, l + 1, 0, k]) + bigM * (1 - z[i, 0, j + 1, k]))
    M.update()

    # for i in range(m):
    #     for k in range(t):
    #         for j in range(n):
    #             for l in range(n):
    #
    #                 '''scheduling constraint'''
    #                 M.addConstr(s[i, j + 1, k] + (sd[j + 1] + grid[j + 1, l]) * z[i, j + 1, l, k] <= s[i, l, k] + bigM * (1 - z[i, j + 1, l, k]))
    M.update()
