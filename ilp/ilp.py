import numpy as np
from docplex.mp.model import Model

from utils import Data, State
from .constraints import CONSTRAINTS


def ilp(data: Data) -> State:
    """
    Solves the integer linear programming (ILP) formulation of the hourly
    learner preference problem.
    """
    with Model("PersonalisedLearningScheduleSolver") as solver:
        solver.parameters.threads = 8

        _setup_decision_variables(data, solver)
        _setup_objective(data, solver)

        solver.B = 1000000

        for constraint in CONSTRAINTS:
            constraint(data, solver)

        solution = solver.solve()

        if solution is None:
            raise ValueError("Infeasible!")

        return _to_state(data, solver)


def _setup_objective(data: Data, solver: Model):
    preference_max = solver.sum(
        data.preferences[i, j] * solver.assignment[i, j]
        for i in range(len(data.learners))
        for j in range(len(data.modules)))

    self_study_penalty = solver.sum(
        data.penalty * solver.assignment[i, len(data.modules) - 1]
        for i in range(len(data.learners)))

    solver.maximize(preference_max - self_study_penalty)


def _setup_decision_variables(data: Data, solver: Model):
    assignment_problem = [list(range(len(data.learners))),
                          list(range(len(data.modules))),
                          list(range(len(data.classrooms))),
                          list(range(len(data.teachers)))]

    solver.assignment = solver.binary_var_matrix(
        *assignment_problem[:2], name="learner_module")

    solver.module_resources = solver.binary_var_cube(
        *assignment_problem[1:], name="module_resources")


def _to_state(data: Data, solver: Model) -> State:
    learner_assignments = [
        module
        for learner in range(len(data.learners))
        for module in range(len(data.modules))
        if solver.assignment[learner, module].solution_value]

    classroom_teacher_assignments = {
        (classroom, teacher): module
        for classroom in range(len(data.classrooms))
        for teacher in range(len(data.teachers))
        for module in range(len(data.modules))
        if solver.module_resources[module, classroom, teacher].solution_value}

    return State(data,
                 np.asarray(learner_assignments),
                 classroom_teacher_assignments)
