from heapq import heappop

from numpy.random import Generator

from src.classes import Activity, Solution
from src.functions import get_problem
from .greedy_insert import greedy_insert


def break_out(destroyed: Solution, generator: Generator) -> Solution:
    """
    Breaks out instruction activities based on the preferences of the unassigned
    learners. Where possible, a new activity is formed from these learners,
    along with some self-study learners that strictly prefer the new activity
    over self-study.

    If any learners remain that cannot be assigned to a new activity, those are
    inserted into existing activities using ``greedy_insert``.
    """
    problem = get_problem()

    histogram = destroyed.preferences_by_module()

    while len(histogram) != 0:
        _, module, to_assign = heappop(histogram)

        try:
            classroom = destroyed.find_classroom_for(module)
            teacher = destroyed.find_teacher_for(module)
        except LookupError:
            continue

        max_size = min(classroom.capacity, problem.max_batch)

        for activity in destroyed.activities:
            if activity.is_instruction():
                continue

            if len(to_assign) >= max_size:
                break

            # We snoop off any self-study learners that can be assigned to
            # this module as well.
            learners = [learner for learner in activity.learners
                        if learner.is_qualified_for(module)
                        if learner.prefers_over_self_study(module)]

            learners = learners[:max_size - len(to_assign)]
            num_removed = activity.remove_learners(learners)
            to_assign.extend(learners[:num_removed])

        activity = Activity(to_assign[:max_size], classroom, teacher, module)

        destroyed.add_activity(activity)
        destroyed.unassigned -= set(activity.learners)

        return break_out(destroyed, generator)

    # Insert final learners into existing activities, if no new activity
    # can be scheduled.
    return greedy_insert(destroyed, generator)
