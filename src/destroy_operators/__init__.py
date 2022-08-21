from .most_slack_classrooms import most_slack_classrooms
from .random_activities import random_activities
from .random_learners import random_learners
from .smallest_activities import smallest_activities
from .regret_learners import regret_learners

DESTROY_OPERATORS = [
    most_slack_classrooms,
    random_activities,
    random_learners,
    regret_learners,
    smallest_activities,
]
