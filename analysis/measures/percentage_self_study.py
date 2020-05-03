from heuristic.classes import Problem, Solution


def percentage_self_study(solution: Solution) -> float:
    """
    Computes the percentage of learners doing self-study.
    """
    problem = Problem()

    num_learners = sum(activity.num_learners
                       for activity in solution.activities)

    return 100 * num_learners / len(problem.learners)
