from operator import attrgetter

from numpy.random import Generator

from heuristic.classes import Activity, Problem, Solution


def greedy_insert(destroyed: Solution, generator: Generator) -> Solution:
    """
    Greedily inserts learners into the best, feasible activities. If no
    activity can be found for a learner, (s)he is inserted into self-study
    instead.
    """
    problem = Problem()

    unused_teachers = set(problem.teachers) - destroyed.used_teachers()

    unused_classrooms = set(problem.classrooms) - destroyed.used_classrooms()
    unused_classrooms = [classroom for classroom in unused_classrooms
                         if classroom.is_self_study_allowed()]

    # It is typically a good idea to prefers using larger rooms for self-study.
    unused_classrooms.sort(key=attrgetter("capacity"))

    activities = destroyed.activities_by_module()

    while len(destroyed.unassigned) != 0:
        learner = destroyed.unassigned.pop()
        inserted = False

        # Attempts to insert the learner into the most preferred, feasible
        # instruction activity.
        for module_id in problem.most_preferred[learner.id]:
            module = problem.modules[module_id]

            if module not in activities:
                continue

            if not learner.prefers_over_self_study(module):
                break

            if inserted := _insert(learner, activities[module]):
                break

            # Could not insert, so the module activities must be exhausted.
            del activities[module]

        # Learner could not be inserted into a regular instruction activity,
        # so now we opt for self-study.
        if not inserted and not _insert(learner,
                                        activities[problem.self_study_module]):
            for activity in activities[problem.self_study_module]:
                biggest_classroom = unused_classrooms[-1]

                if activity.classroom.capacity < biggest_classroom.capacity:
                    current = activity.classroom
                    activity.classroom = unused_classrooms.pop()
                    unused_classrooms.insert(0, current)

                    destroyed.switch_classrooms(current, activity.classroom)
                    activity.insert_learner(learner)
                    break

                if activity.can_split():
                    teacher = unused_teachers.pop()
                    classroom = unused_classrooms.pop()

                    new = activity.split_with(classroom, teacher)
                    activity.insert_learner(learner)

                    destroyed.add_activity(new)
                    activities[problem.self_study_module].insert(0, new)
                    break
            else:
                # It could be that there is no self-study activity. In that
                # case we should make one. This does not happen often.
                classroom = unused_classrooms.pop()
                teacher = unused_teachers.pop()

                learners = destroyed.unassigned[-problem.min_batch:]
                destroyed.unassigned = destroyed.unassigned[:-problem.min_batch]

                activity = Activity(learners, classroom, teacher,
                                    problem.self_study_module)

                destroyed.add_activity(activity)
                activities[problem.self_study_module].append(activity)

    return destroyed


def _insert(learner, activities):
    for activity in activities:
        if activity.can_insert_learner():
            activity.insert_learner(learner)
            return True

    return False
