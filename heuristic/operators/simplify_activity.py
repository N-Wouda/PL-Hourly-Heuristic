from typing import List, Set

import numpy as np
from numpy.random import RandomState
from ortools.linear_solver.pywraplp import Solver

from heuristic.utils import HeuristicState


def simplify_activity(state: HeuristicState, rnd: RandomState) -> HeuristicState:
    """
    Simplifies a module activity, if possible.
    """
    module = rnd.choice(list(state.module_assignments))

    activities = [classroom_teacher for classroom_teacher, activity_module
                  in state.classroom_teacher_assignments.items()
                  if activity_module == module]

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

    # Only capacity is of relevance for self-study modules
    if module == len(state.modules) - 1:
        objective = [variables[idx] * available_rooms[idx]['capacity']
                     for idx in variables]
    else:
        objective = [variables[idx] * min(state.max_batch,
                                          available_rooms[idx]['capacity'])
                     for idx in variables]

    # Minimise the empty overhead in classroom assignments
    solver.Minimize(solver.Sum(objective))

    # Total capacity of the provided rooms *must* be greater than the number
    # of learners
    total_learners = np.count_nonzero(state.learner_assignments == module)
    solver.Add(solver.Sum(objective) >= total_learners)

    assert solver.Solve() == Solver.OPTIMAL, "Solution is not optimal!"

    return [available_rooms[idx] for idx in range(len(available_rooms))
            if variables[idx].solution_value() > 0]
