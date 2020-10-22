import numpy as np


def printSolution(M, solution_d, solution_x, solution_y, solution_z, solution_s, m, n, t, df, df_n, q, f):
    var_d, var_x, var_y, var_z, var_s = np.empty([n]), np.empty([m, n]), np.empty(
        [m, n + 1, t]), np.empty([m, n + 1, n + 1, t]), np.empty([m, n + 1, t])
    for i in range(m):
        for j in range(n):
            var_d[j] = solution_d[j]
            var_x[i, j] = solution_x[i, j]
    for i in range(m):
        for j in range(n + 1):
            for k in range(t):
                var_y[i, j, k] = solution_y[i, j, k]
                var_s[i, j, k] = solution_s[i, j, k]
                for l in range(n + 1):
                    var_z[i, j, l, k] = solution_z[i, j, l, k]
    print('\nnodes\n', df.head())
    print('\nnurses\n', df_n.head())
    np.set_printoptions(formatter={'float': '{: 0.0f}'.format})

    print('\nobj\n', int(M.objVal),
          '\nq\n', q,
          '\nf\n', f,
          '\nd\n', var_d,
          '\nx\n', var_x,
          '\ny\n', var_y,
          '\n\ns', var_s[0, :, 0],
          '\n', var_s[1, :, 0],
          '\nz\n', var_z[0, :, :, 0])
