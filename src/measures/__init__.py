from .instance import instance
from .num_activities import num_activities
from .num_instruction import num_instruction
from .num_self_study import num_self_study
from .objective import objective
from .instruction_activity_sizes import instruction_activity_sizes

MEASURES = {
    "instance": instance,  # this one is not free-form, and *must* be "instance"
    "objective": objective,
    "instruction (# learners)": num_instruction,
    "self-study (# learners)": num_self_study,
    "activities (#)": num_activities,
    "instruction activity sizes": instruction_activity_sizes
}
