from .learner_schedule import learner_schedule
from .max_batch import max_batch
from .min_batch import min_batch
from .room_type import room_type
from .self_study_allowed import self_study_allowed
from .singular_use import singular_use
from .strictly_positive_assignment import strictly_positive_assignment
from .teaching_qualification import teaching_qualification

CONSTRAINTS = [
    learner_schedule,
    max_batch,
    min_batch,
    room_type,
    self_study_allowed,
    singular_use,
    strictly_positive_assignment,
    teaching_qualification,
]
