import numpy as np


def setup_solver_data(solver, data):
    P = np.asarray(data["preferences"])

    # Self-study module preference
    P = np.concatenate((P, np.max(P, axis=1)[:, None]), axis=1)

    Q = np.asarray(data["qualifications"])

    solver.P = P
    solver.Q = Q

    solver.w = data["parameters"]["penalty"]
    solver.delta_min = data["parameters"]["min_batch"]
    solver.delta_max = data["parameters"]["max_batch"]
    solver.B = 1000000
