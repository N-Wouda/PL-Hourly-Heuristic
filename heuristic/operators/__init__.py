from .break_out import break_out
from .fold_in import fold_in
from .insert_learner import insert_learner
from .simplify_activity import simplify_activity
from .split_activity import split_activity
from .swap_learner import swap_learner
from .swap_teacher import swap_teacher

OPERATORS = [
    break_out,
    fold_in,
    #insert_learner,
    simplify_activity,
    # split_activity,
    #swap_learner,
    swap_teacher
]
"""
    Each of these methods should function in at most quadratic time, so as not
    to slow down the problem too much. Less is preferred!
"""
