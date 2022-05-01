from src.classes import Solution


def num_self_study(solution: Solution):
    return sum(activity.num_learners for activity in solution.activities
               if activity.is_self_study())
