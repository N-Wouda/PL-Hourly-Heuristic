from .classroom_utilisation import classroom_utilisation
from .instruction_size import instruction_size
from .objective import objective
from .percentage_instruction import percentage_instruction
from .percentage_self_study import percentage_self_study
from .self_study_size import self_study_size
from .teacher_utilisation import teacher_utilisation

MEASURES = [
    classroom_utilisation,
    instruction_size,
    objective,
    percentage_instruction,
    percentage_self_study,
    self_study_size,
    teacher_utilisation,
]

from .compute_measures import compute_measures
