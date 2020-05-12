from functools import wraps
from typing import Callable, List

from ortools.linear_solver.pywraplp import Solver

from heuristic.classes import Activity, Module, Problem, Solution


def simplify_activities(operator: Callable[..., Solution]):
    """
    Simplifies the activity assignments. This ensures existing activities are
    grouped, where-ever possible, into the most compact form possible.
    """

    @wraps(operator)
    def wrapper(*args, **kwargs):
        solution = operator(*args, **kwargs)

        for module, activities in solution.activities_by_module().items():
            if len(activities) > 1:  # nothing to simplify with one activity.
                _simplify(solution, activities, module)

        return solution

    return wrapper


def _simplify(solution: Solution, activities: List[Activity], module: Module):
    problem = Problem()

    # Classrooms that may be used for this module: all those the are suitable,
    # minus those in use, plus those in use for the module's activities.
    classrooms = set(problem.classrooms_by_module[module])
    classrooms -= solution.used_classrooms()
    classrooms |= {activity.classroom for activity in activities}
    classrooms = list(classrooms)

    solver = Solver('TestSolver', Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    variables = [solver.BoolVar(f'x[{idx}]') for idx in range(len(classrooms))]

    solver.Minimize(solver.Sum(variables))

    if module.is_self_study():
        constraint = [variable * classroom.capacity
                      for variable, classroom in zip(variables, classrooms)]
    else:
        constraint = [variable * min(problem.max_batch, classroom.capacity)
                      for variable, classroom in zip(variables, classrooms)]

    num_learners = sum(activity.num_learners for activity in activities)
    solver.Add(solver.Sum(constraint) >= num_learners)

    assert solver.Solve() == Solver.OPTIMAL, "Solution is not optimal!"

    rooms = [classroom for variable, classroom in zip(variables, classrooms)
             if variable.solution_value()]

    if len(rooms) == len(activities):
        return  # no improvement.

    teachers = {activity.teacher for activity in activities}

    indices = [idx for idx, activity in enumerate(solution.activities)
               if activity.module is module]

    for idx in reversed(indices):  # reversed so the indices don't shift
        solution.remove_activity(idx)

    learners = [learner
                for activity in activities
                for learner in activity.learners]

    activities = []

    # First fill with the minimal required number of learners, per room.
    for room in rooms:
        min_learners = learners[:problem.min_batch]
        learners = learners[problem.min_batch:]

        activities.append(Activity(min_learners, room, teachers.pop(), module))

    # Then flood-fill with the remaining learners.
    for activity in activities:
        while len(learners) != 0 and activity.can_insert_learner():
            activity.insert_learner(learners.pop())

        if len(learners) == 0:
            break

    for activity in activities:
        solution.add_activity(activity)
