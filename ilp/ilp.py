from collections import defaultdict
from typing import List, Tuple

from docplex.mp.model import Model

from heuristic.classes import Problem
from heuristic.constants import SELF_STUDY_MODULE_ID
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

        return _to_assignments(solver)


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


def _to_assignments(solver: Model) -> List[Tuple]:
    """
    Turns the solver's decision variables into a series of (learner, module,
    classroom, teacher) assignments, which are then stored to the file system.

    TODO this is legacy code, taken from the old State object. It's not the
     prettiest, but it should work.
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

    assignments = []
    counters = defaultdict(lambda: 0)

    for module in range(len(problem.modules)):
        # Select learners and activities belonging to each module, such
        # that we can assign them below.
        learners = [learner for learner in range(len(problem.learners))
                    if learner_assignments[learner] == module]

        activities = [activity for activity, activity_module
                      in classroom_teacher_assignments.items()
                      if module == activity_module]

        # Assign at least min_batch number of learners to each activity.
        # This ensures the minimum constraint is met for all activities.
        for classroom, teacher in activities:
            for _ in range(problem.min_batch):
                if not learners:
                    break

                assignment = (learners.pop(), module, classroom, teacher)
                assignments.append(list(assignment))

                counters[classroom] += 1

        # Next we flood-fill these activities with learners, until none
        # remain to be assigned.
        for classroom, teacher in activities:
            capacity = problem.classrooms[classroom].capacity

            if module != SELF_STUDY_MODULE_ID:
                capacity = min(problem.max_batch, capacity)

            while learners:
                if counters[classroom] == capacity:  # classroom is full
                    break

                assignment = (learners.pop(), module, classroom, teacher)
                assignments.append(list(assignment))

                counters[classroom] += 1

    return assignments
