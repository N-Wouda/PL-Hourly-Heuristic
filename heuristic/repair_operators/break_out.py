from heapq import heappop

from numpy.random import Generator

from heuristic.classes import Activity, Problem, Solution
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
    problem = Problem()

    histogram = destroyed.preferences_by_module()

    while len(histogram) != 0:
        _, module, to_assign = heappop(histogram)

        try:
            classroom = destroyed.find_classroom_for(module)
            teacher = destroyed.find_teacher_for(module)
        except LookupError:
            continue

        if not destroyed.leaves_sufficient_for_self_study(classroom, teacher):
            continue

        max_size = min(classroom.capacity, problem.max_batch)

        for activity in destroyed.activities:
            if activity.is_instruction():
                continue

            if len(to_assign) >= max_size:
                break

            # We snoop off any self-study learner that can be assigned to this
            # module as well.
            learners = [learner for learner in activity.learners
                        if learner.prefers_over_self_study(module)]

            while activity.can_remove_learner() \
                    and len(to_assign) < max_size \
                    and len(learners) != 0:
                learner = learners.pop()
                activity.remove_learner(learner)
                to_assign.append(learner)

        activity = Activity(to_assign[:max_size], classroom, teacher, module)

        destroyed.activities.append(activity)
        destroyed.unassigned = [learner for learner in destroyed.unassigned
                                if learner not in activity]

        return break_out(destroyed, generator)

    # Insert final learners into existing activities, if no new activity
    # can be scheduled.
    return greedy_insert(destroyed, generator)
