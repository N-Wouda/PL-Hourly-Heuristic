from heapq import heappop

from numpy.random import Generator

from src.classes import Activity, Problem, Solution
from src.constants import SELF_STUDY_MODULE_ID
from .greedy_insert import greedy_insert


def break_out(destroyed: Solution,
              generator: Generator,
              problem: Problem) -> Solution:
    """
    Breaks out instruction activities based on the preferences of the unassigned
    learners. Where possible, a new activity is formed from these learners,
    along with some self-study learners that strictly prefer the new activity
    over self-study.

    If any learners remain that cannot be assigned to a new activity, those are
    inserted into existing activities using ``greedy_insert``.
    """
    prefs = problem.preferences

    unassigned = [learner.id for learner in destroyed.unassigned]
    histogram = problem.preferences_by_module(unassigned)

    while len(histogram) != 0:
        _, module_id, to_assign_ids = heappop(histogram)

        module = problem.modules[module_id]
        to_assign = [problem.learners[learn_id] for learn_id in to_assign_ids]

        try:
            classroom = destroyed.find_classroom_for(module)
            teacher = destroyed.find_teacher_for(module)
        except LookupError:
            continue

        max_size = min(classroom.capacity, problem.max_batch)

        for activity in destroyed.activities:
            if activity.is_instruction():
                continue

            # We snoop off any self-study learners that can be assigned to
            # this module as well.
            learners = [learner for learner in activity.learners
                        if (prefs[learner.id, module.id]
                            > prefs[learner.id, SELF_STUDY_MODULE_ID])]

            learners = learners[:max_size - len(to_assign)]
            num_removed = activity.remove_learners(learners)
            to_assign.extend(learners[:num_removed])

            if len(to_assign) >= max_size:
                break

        activity = Activity(to_assign[:max_size], classroom, teacher, module)

        destroyed.add_activity(activity)
        destroyed.unassigned -= set(activity.learners)

        return break_out(destroyed, generator, problem)

    # Insert final learners into existing activities, if no new activity
    # can be scheduled.
    return greedy_insert(destroyed, generator, problem)
