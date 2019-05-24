def setup_objective(solver, data):
    preference_max = solver.sum(
        solver.P[i, j] * solver.assignment[i, j]
        for i in range(len(data["learners"]))
        for j in range(len(data["modules"])))

    self_study_penalty = solver.sum(
        solver.w * solver.assignment[i, len(data["modules"]) - 1]
        for i in range(len(data["learners"])))

    solver.maximize(preference_max - self_study_penalty)
