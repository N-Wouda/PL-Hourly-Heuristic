from operator import attrgetter, methodcaller

from numpy.random import Generator

from src.classes import Activity, Problem, Solution


def greedy_insert(destroyed: Solution,
                  generator: Generator,
                  problem: Problem) -> Solution:
    """
    Greedily inserts learners into the best, feasible activities. If no
    activity can be found for a learner, (s)he is inserted into self-study
    instead.
    """
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
            if len(unused_classrooms) == 0 or len(unused_teachers) == 0:
                # This implies we need to remove one or more instruction
                # activities. Let's do the naive and greedy thing, and switch
                # the instruction activity with lowest objective value into a
                # self-study assignment.
                iterable = [activity
                            for activity in destroyed.activities
                            if activity.is_instruction()
                            if activity.classroom.is_self_study_allowed()
                            # After switching to self-study, the max_batch
                            # constraint is longer applicable - only capacity.
                            if activity.can_insert_learner(if_self_study=True)]

                activity = min(iterable, key=methodcaller("objective"))

                activities[problem.self_study_module].append(activity)
                activities[activity.module].remove(activity)

                activity.switch_to_self_study()
                activity.insert_learner(learner)
                continue

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

                    new_activity = activity.split_with(classroom, teacher)
                    activity.insert_learner(learner)

                    destroyed.add_activity(new_activity)
                    activities[problem.self_study_module].append(new_activity)
                    break
            else:
                # It could be that there is no self-study activity. In that
                # case we should make one. Should be rare.
                classroom = unused_classrooms.pop()
                teacher = unused_teachers.pop()

                # This could be a problem if there are insufficient learners
                # left. That has never happened so far, so the concern seems
                # more theoretical than real.
                learners = [destroyed.unassigned.pop()
                            for _ in range(problem.min_batch)]

                activity = Activity(learners, classroom, teacher,
                                    problem.self_study_module)

                # Since we popped this learner from the unassigned list before,
                # it is not yet in the new activity.
                activity.insert_learner(learner)

                destroyed.add_activity(activity)
                activities[problem.self_study_module].append(activity)

    return destroyed


def _insert(learner, activities):
    for idx, activity in enumerate(activities):
        if activity.can_insert_learner():
            activity.insert_learner(learner)

            # Ensures the next traversal finds an activity that we could just
            # insert into (so probably can for several more learners).
            activities[0], activities[idx] = activity, activities[0]
            return True

    return False
