from typing import List, Set

import numpy as np
from ortools.linear_solver.pywraplp import Solver

from heuristic.utils import HeuristicState


def simplify_activity(state: HeuristicState, module: int) -> HeuristicState:
    """
    Simplifies a module activity, if possible. This method is a helper operator
    for fold_in and break_out, so it takes an additional module parameter.
    """
    return _simplify_activity(
        _simplify_activity(state, module),      # simplifies the given module
        len(state.modules) - 1)                 # simplifies self-study


def _simplify_activity(state: HeuristicState, module: int) -> HeuristicState:
    activities = [classroom_teacher for classroom_teacher, activity_module
                  in state.classroom_teacher_assignments.items()
                  if activity_module == module]

    if len(activities) == 0:        # nothing to optimise in this case. This
        return state                # can happen after a fold_in operation.

    classrooms, _ = zip(*activities)

    # The number of available classrooms is computed as all classrooms,
    # excluding those currently used in an activity. To this we add those
    # classrooms currently used for *this* module, as those may be re-assigned.
    available_classrooms = _classrooms_for_module(state, module)
    available_classrooms -= state.classroom_assignments
    available_classrooms |= set(classrooms)

    needed_rooms = _minimal_cover(state,
                                  module,
                                  [classroom for classroom in state.classrooms
                                   if classroom['id'] in available_classrooms])

    if len(needed_rooms) <= len(classrooms):    # this we can solve, since we
        new_state = state.copy()                # can free some rooms

        # First we remove all relevant existing activities.
        for activity in activities:
            del new_state.classroom_teacher_assignments[activity]

        # Now insert the new activities, where we re-use the assigned teachers.
        for idx, new_room in enumerate(needed_rooms):
            old_room, teacher = activities[idx]
            new_state.classroom_teacher_assignments[(new_room['id'],
                                                     teacher)] = module

        return new_state

    return state


def _classrooms_for_module(state: HeuristicState, module: int) -> Set[int]:
    """
    Returns those classrooms that are available for the given module,
    respecting the room type or self-study constraint.
    """
    if module == len(state.modules) - 1:
        return set(classroom['id'] for classroom in state.classrooms
                   if classroom['self_study_allowed'])

    return set(classroom['id'] for classroom in state.classrooms
               if classroom['room_type'] == state.modules[module]['room_type'])


def _minimal_cover(state: HeuristicState, module: int,
                   available_rooms: List) -> List:
    """
    Returns the rooms needed (from those available), such that a minimal
    amount of extra space is wasted.
    """
    solver = Solver('TestSolver', Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    # Room at idx is used iff solution value > 0 (boolean True)
    variables = {idx: solver.BoolVar(f'x[{idx}]')
                 for idx in range(len(available_rooms))}

    # Minimise the number of classroom assignments
    solver.Minimize(solver.Sum(variables.values()))

    # Only capacity is of relevance for self-study modules
    if module == len(state.modules) - 1:
        constraint = [variables[idx] * available_rooms[idx]['capacity']
                      for idx in variables]
    else:
        constraint = [variables[idx] * min(state.max_batch,
                                           available_rooms[idx]['capacity'])
                      for idx in variables]

    # Total capacity of the provided rooms *must* be greater than the number
    # of learners
    total_learners = np.count_nonzero(state.learner_assignments == module)
    solver.Add(solver.Sum(constraint) >= total_learners)

    assert solver.Solve() == Solver.OPTIMAL, "Solution is not optimal!"

    return [available_rooms[idx] for idx in range(len(available_rooms))
            if variables[idx].solution_value() > 0]
