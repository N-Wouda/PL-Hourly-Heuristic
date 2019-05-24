def setup_decision_variables(solver, assignment_problem):
    solver.assignment = solver.binary_var_matrix(
        *assignment_problem[:2], name="learner_module")

    solver.module_resources = solver.binary_var_cube(
        *assignment_problem[1:], name="module_resources")
