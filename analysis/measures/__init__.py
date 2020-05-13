from .instance import instance
from .num_activities import num_activities
from .num_instruction import num_instruction
from .num_self_study import num_self_study
from .objective import objective

MEASURES = {
    "instance": instance,  # this one is not free-form, and *must* be "instance"
    "objective": objective,
    "instruction (# learners)": num_instruction,
    "self-study (# learners)": num_self_study,
    "activities (#)": num_activities,
}
