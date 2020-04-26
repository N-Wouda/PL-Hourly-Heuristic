from heapq import heappop

from numpy.random import RandomState

from heuristic.classes import Activity, Problem, Solution
from heuristic.functions import find_classroom, find_teacher
from .greedy_insert import greedy_insert


def break_out(destroyed: Solution, rnd_state: RandomState) -> Solution:
    """
    TODO.
    """
    problem = Problem()

    histogram = destroyed.preferences_by_module()

    while len(histogram) != 0:
        _, module, to_assign = heappop(histogram)

        if len(to_assign) < problem.min_batch:
            # TODO we can probably also grab a few from self-study for the
            #   comparison.
            continue

        try:
            classroom = find_classroom(destroyed, module)
            teacher = find_teacher(destroyed, module)
        except LookupError:
            continue

        classrooms = set(problem.classrooms) - destroyed.used_classrooms()
        classrooms.remove(classroom)

        if classroom.is_self_study_allowed() \
                and not _leaves_sufficient_for_self_study(destroyed,
                                                          classrooms):
            continue

        max_size = min(classroom.capacity, problem.max_batch)

        for activity in destroyed.activities:
            if activity.is_self_study():
                # We snoop off any self-study learner that can be assigned to
                # this module as well.
                learners = [learner for learner in activity.learners
                            if learner.prefers_over_self_study(module)]

                while activity.can_remove_learner() \
                        and len(to_assign) < max_size \
                        and len(learners) != 0:
                    learner = learners.pop()
                    activity.remove_learner(learner)
                    to_assign.append(learner)

        if len(to_assign) > max_size:
            # TODO sort by best?
            to_assign = to_assign[:max_size]

        activity = Activity(to_assign, classroom, teacher, module)

        destroyed.activities.append(activity)
        destroyed.unassigned = [learner for learner in destroyed.unassigned
                                if learner not in activity]

        return break_out(destroyed, rnd_state)

    # Insert final learners into existing activities, if no new activity
    # can be scheduled.
    return greedy_insert(destroyed, rnd_state)


def _leaves_sufficient_for_self_study(destroyed, classrooms):
    capacity = sum(classroom.capacity for classroom in classrooms
                   if classroom.is_self_study_allowed())

    return len(destroyed.unassigned) < capacity
