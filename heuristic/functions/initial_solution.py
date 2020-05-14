from itertools import zip_longest

from heuristic.classes import Activity, Problem, Solution


def initial_solution() -> Solution:
    """
    Constructs an initial solution, where all learners are in self-study
    activities, in appropriate classrooms (and with some random teacher
    assigned to supervise).
    """
    problem = Problem()
    solution = Solution([])

    # Not all classrooms are suitable for self-study. Such a restriction does,
    # however, not apply to teachers.
    classrooms = [classroom for classroom in problem.classrooms
                  if classroom.is_self_study_allowed()]

    learners_to_assign = problem.learners

    for classroom, teacher in zip_longest(classrooms, problem.teachers):
        assert classroom is not None
        assert teacher is not None

        learners = learners_to_assign[-min(len(learners_to_assign),
                                           classroom.capacity):]

        activity = Activity(learners,
                            classroom,
                            teacher,
                            problem.self_study_module)

        solution.add_activity(activity)

        learners_to_assign = learners_to_assign[:-activity.num_learners]

        if len(learners_to_assign) == 0:
            break

    return solution
