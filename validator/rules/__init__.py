from .activity_size import activity_size
from .classroom_teacher_tuples_to_modules \
    import classroom_teacher_tuples_to_modules
from .classrooms_to_modules import classrooms_to_modules
from .classrooms_to_teachers import classrooms_to_teachers
from .learners_to_classrooms import learners_to_classrooms
from .learners_to_modules import learners_to_modules
from .learners_to_teachers import learners_to_teachers
from .module_classroom_room_type import module_classroom_room_type
from .teacher_module_qualifications import teacher_module_qualifications
from .teachers_to_classrooms import teachers_to_classrooms
from .teachers_to_modules import teachers_to_modules

RULES = [
    activity_size,
    classroom_teacher_tuples_to_modules,
    classrooms_to_modules,
    classrooms_to_teachers,
    learners_to_classrooms,
    learners_to_modules,
    learners_to_teachers,
    module_classroom_room_type,
    teacher_module_qualifications,
    teachers_to_classrooms,
    teachers_to_modules,
]
