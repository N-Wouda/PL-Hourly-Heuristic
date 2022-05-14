from .largest_regret_activities import largest_regret_activities
from .most_slack_classrooms import most_slack_classrooms
from .random_activities import random_activities
from .random_learners import random_learners
from .smallest_activities import smallest_activities
from .worst_learners import worst_learners

DESTROY_OPERATORS = [
    random_activities,
    random_learners,
    worst_learners,
]
