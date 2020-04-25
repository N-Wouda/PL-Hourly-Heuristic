from collections import defaultdict

from numpy.random import RandomState

from heuristic.classes import Problem, Solution
from heuristic.constants import SELF_STUDY_MODULE_ID


def greedy_insert(destroyed: Solution, rnd_state: RandomState) -> Solution:
    """
    Greedily inserts learners into the best, feasible activities. If no
    activity can be found for a learner, (s)he is inserted into self-study
    instead.
    """
    rnd_state.shuffle(destroyed.unassigned)

    problem = Problem()

    activities_by_module = defaultdict(list)

    for activity in destroyed.activities:
        activities_by_module[activity.module.id].append(activity)

    # TODO this is pretty nasty.
    unused_teachers = set(problem.teachers) - destroyed.used_teachers()
    unused_classrooms = set(problem.classrooms) - destroyed.used_classrooms()
    unused_classrooms = {classroom for classroom in unused_classrooms
                         if classroom.is_self_study_allowed()}

    while len(destroyed.unassigned) != 0:
        learner = destroyed.unassigned.pop()

        # Attempts to insert the learner into the most preferred, feasible
        # instruction activity. If no such activities exist the learner is
        # inserted into a self-study activity instead.
        for module in problem.most_preferred[learner.id]:
            if module not in activities_by_module:
                continue

            if learner.self_study_objective() > problem.preferences[learner.id,
                                                                    module]:
                continue

            if _insert(learner, activities_by_module[module]):
                break
        else:
            # TODO make all this nicer

            # Learner could not be inserted into a regular instruction activity,
            # so now we opt for self-study.
            self_study_activities = activities_by_module[SELF_STUDY_MODULE_ID]

            if not _insert(learner, self_study_activities):
                for activity in self_study_activities:
                    if activity.num_learners >= 2 * problem.min_batch:
                        teacher = unused_teachers.pop()
                        classroom = unused_classrooms.pop()

                        new_activity = activity.split_with(classroom, teacher)
                        new_activity.insert_learner(learner)
                        destroyed.activities.append(new_activity)
                        activities_by_module[SELF_STUDY_MODULE_ID].append(
                            new_activity)

                        break
                else:
                    # This would be most curious, and warrant further
                    # investigation.
                    raise Exception("It should always be possible to "
                                    "schedule a learner in self-study.")

    return destroyed


def _insert(learner, activities):
    for activity in activities:
        if activity.can_insert_learner():
            activity.insert_learner(learner)
            return True

    return False
