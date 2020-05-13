from .instance import instance
from .num_classrooms_used import num_classrooms_used
from .num_instruction import num_instruction
from .num_self_study import num_self_study
from .num_teachers_used import num_teachers_used
from .objective import objective

MEASURES = {
    "instance": instance,  # this one is not free-form, and *must* be "instance"
    "objective": objective,
    "instruction (# learners)": num_instruction,
    "self-study (# learners)": num_self_study,
    "used classrooms": num_classrooms_used,
    "used teachers": num_teachers_used
}
