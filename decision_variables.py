def decisionVariables(M, gb, m, n, t, d, x, y, z, s):
    ''' decision variable: delta '''
    for i in range(n):
        d[i] = M.addVar(vtype=gb.GRB.BINARY, name="d%d" % (i))
    M.update()
    '''decision variable x'''
    for i in range(m):
        for j in range(n):
            x[i, j] = M.addVar(vtype=gb.GRB.BINARY, name='x%d,%d' % (i, j))
    M.update()
    '''decision variable y'''
    for i in range(m):
        for j in range(n + 1):  # +1 is for depot
            for k in range(t):
                y[i, j, k] = M.addVar(vtype=gb.GRB.BINARY,
                                      name='y%d,%d,%d' % (i, j, k))
    M.update()
    '''variable z'''
    for i in range(m):
        for j in range(n + 1):
            for l in range(n + 1):
                for k in range(t):
                    z[i, j, l, k] = M.addVar(
                        vtype=gb.GRB.BINARY, name="z%d,%d,%d,%d" % (i, j, l, k))
    M.update()
    '''variable s'''
    for i in range(m):
        for j in range(n + 1):
            for k in range(t):
                s[i, j, k] = M.addVar(vtype=gb.GRB.CONTINUOUS,
                                      name="s%d,%d,%d" % (i, j, k))
    M.update()
