from functools import wraps
from typing import Callable

from ortools.linear_solver.pywraplp import Solver

from heuristic.classes import Module, Problem, Solution, Activity


def simplify_activities(operator: Callable[..., Solution]):
    """
    Simplifies the activity assignments. This ensures existing activities are
    grouped, where-ever possible, into the most compact form possible.
    """

    @wraps(operator)
    def wrapper(*args, **kwargs):
        solution = operator(*args, **kwargs)
        modules = {activity.module for activity in solution.activities}

        for module in modules:
            _simplify(solution, module)

        return solution

    return wrapper


def _simplify(solution: Solution, module: Module) -> Solution:
    # TODO clean and document this
    problem = Problem()

    activities = [activity for activity in solution.activities
                  if activity.module is module]

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

    total_learners = sum(activity.num_learners for activity in activities)
    solver.Add(solver.Sum(constraint) >= total_learners)

    assert solver.Solve() == Solver.OPTIMAL, "Solution is not optimal!"

    rooms = [classroom for variable, classroom in zip(variables, classrooms)
             if variable.solution_value() > 0]

    if len(rooms) < len(activities):
        teachers = {activity.teacher for activity in activities}

        indices = [idx for idx, activity in enumerate(solution.activities)
                   if activity.module is module]

        for idx in reversed(indices):
            solution.remove_activity(idx)

        learners = [learner
                    for activity in activities
                    for learner in activity.learners]

        activities = []

        for room in rooms:
            min_learners = learners[:problem.min_batch]
            learners = learners[problem.min_batch:]

            activities.append(Activity(min_learners,
                                       room,
                                       teachers.pop(),
                                       module))

        for activity in activities:
            while len(learners) != 0 and activity.can_insert_learner():
                activity.insert_learner(learners.pop())

            if len(learners) == 0:
                break

        for activity in activities:
            solution.add_activity(activity)

    return solution
