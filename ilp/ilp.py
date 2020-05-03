from typing import List, Tuple

import numpy as np
from docplex.mp.model import Model

from heuristic.classes import Problem
from utils import State
from .constraints import CONSTRAINTS


def ilp() -> List[Tuple]:
    """
    Solves the integer linear programming (ILP) formulation of the hourly
    learner preference problem.
    """
    with Model("PersonalisedLearningScheduleSolver") as solver:
        solver.parameters.threads = 8

        _setup_decision_variables(solver)
        _setup_objective(solver)

        solver.B = 1000000

        for constraint in CONSTRAINTS:
            constraint(solver)

        solution = solver.solve()

        if solution is None:
            # There is not much that can be done in this case, so we raise an
            # error. Logging should pick this up, but it is nearly impossible
            # for this to happen due to the problem structure.
            raise ValueError("Infeasible!")

        return _to_state(solver).to_assignments()


def _setup_objective(solver: Model):
    """
    Specifies the optimisation objective.
    """
    problem = Problem()

    preference_max = solver.sum(
        problem.preferences[i, j] * solver.assignment[i, j]
        for i in range(len(problem.learners))
        for j in range(len(problem.modules)))

    self_study_penalty = solver.sum(
        problem.penalty * solver.assignment[i, len(problem.modules) - 1]
        for i in range(len(problem.learners)))

    solver.maximize(preference_max - self_study_penalty)


def _setup_decision_variables(solver: Model):
    """
    Prepares and applies the decision variables to the model.
    """
    problem = Problem()

    assignment_problem = [list(range(len(problem.learners))),
                          list(range(len(problem.modules))),
                          list(range(len(problem.classrooms))),
                          list(range(len(problem.teachers)))]

    solver.assignment = solver.binary_var_matrix(
        *assignment_problem[:2], name="learner_module")

    solver.module_resources = solver.binary_var_cube(
        *assignment_problem[1:], name="module_resources")


def _to_state(solver: Model) -> State:
    """
    Turns the model's decision variables into an appropriate ``State`` object,
    which may then be queried for the modelling outcomes.
    """
    problem = Problem()

    learner_assignments = [
        module
        for learner in range(len(problem.learners))
        for module in range(len(problem.modules))
        if solver.assignment[learner, module].solution_value]

    classroom_teacher_assignments = {
        (classroom, teacher): module
        for classroom in range(len(problem.classrooms))
        for teacher in range(len(problem.teachers))
        for module in range(len(problem.modules))
        if solver.module_resources[module, classroom, teacher].solution_value}

    return State(np.array(learner_assignments), classroom_teacher_assignments)
