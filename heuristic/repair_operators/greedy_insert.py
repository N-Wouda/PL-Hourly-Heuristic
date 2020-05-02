from collections import defaultdict
from operator import attrgetter

from numpy.random import Generator

from heuristic.classes import Activity, Problem, Solution
from heuristic.constants import SELF_STUDY_MODULE_ID


def greedy_insert(destroyed: Solution, generator: Generator) -> Solution:
    """
    Greedily inserts learners into the best, feasible activities. If no
    activity can be found for a learner, (s)he is inserted into self-study
    instead.

    TODO make all this nicer
    """
    generator.shuffle(destroyed.unassigned)

    # TODO this thing is gnarly - clean it up

    problem = Problem()

    activities_by_module = defaultdict(list)

    for activity in destroyed.activities:
        activities_by_module[activity.module.id].append(activity)

    unused_teachers = set(problem.teachers) - destroyed.used_teachers()

    unused_classrooms = set(problem.classrooms) - destroyed.used_classrooms()
    unused_classrooms = [classroom for classroom in unused_classrooms
                         if classroom.is_self_study_allowed()]

    # Ensures we always first use the largest classrooms for self-study. This is
    # typically a good idea, as it leaves the smaller classrooms to more
    # specific instruction activities.
    unused_classrooms.sort(key=attrgetter("capacity"))

    while len(destroyed.unassigned) != 0:
        learner = destroyed.unassigned.pop()

        # Attempts to insert the learner into the most preferred, feasible
        # instruction activity. If no such activities exist the learner is
        # inserted into a self-study activity instead.
        for module in problem.most_preferred[learner.id]:
            if module not in activities_by_module:
                continue

            self_study_mod = problem.most_preferred[learner.id, 0]
            self_study_pref = problem.preferences[learner.id, self_study_mod]
            self_study_pref -= problem.penalty

            module_pref = problem.preferences[learner.id, module]

            if self_study_pref > module_pref:
                continue

            if _insert(learner, activities_by_module[module]):
                break
        else:
            # Learner could not be inserted into a regular instruction activity,
            # so now we opt for self-study.
            if not _insert(learner, activities_by_module[SELF_STUDY_MODULE_ID]):
                for activity in activities_by_module[SELF_STUDY_MODULE_ID]:
                    biggest_classroom = unused_classrooms[-1]

                    if activity.classroom.capacity < biggest_classroom.capacity:
                        current = activity.classroom
                        activity.classroom = unused_classrooms.pop()
                        unused_classrooms.insert(0, current)

                        activity.insert_learner(learner)

                        break

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
                    # It could be that there is no self-study activity. In that
                    # case we should make one.
                    if len(activities_by_module[SELF_STUDY_MODULE_ID]) == 0:
                        classroom = unused_classrooms.pop()
                        teacher = unused_teachers.pop()

                        # TODO select which learners more intelligently?
                        learners = destroyed.unassigned[-problem.min_batch:]
                        destroyed.unassigned = destroyed.unassigned[
                                               :problem.min_batch]

                        activity = Activity(learners, classroom, teacher,
                                            problem.self_study_module)

                        destroyed.activities.append(activity)
                        activities_by_module[SELF_STUDY_MODULE_ID].append(
                            activity)
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
