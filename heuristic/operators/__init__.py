from .break_out import break_out
from .fold_in import fold_in
from .swap_learner import swap_learner
from .swap_classroom import swap_classroom
from .swap_teacher import swap_teacher
from .insert_learner import insert_learner


OPERATORS = [
    break_out,
    #fold_in,
    insert_learner,
    swap_learner,
    #swap_teacher,
    #swap_classroom
]
"""
    Each of these methods should function in at most quadratic time, so as not
    to slow down the problem too much. Less is preferred!
"""
