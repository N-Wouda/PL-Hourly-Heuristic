from typing import List, Tuple

from utils import Data


def teacher_module_qualifications(data: Data, solution: List[Tuple]) -> bool:
    """
    Verifies each teacher-module assignment satisfies the required teacher
    qualification.
    """
    teacher_modules = {}

    for assignment in solution:
        _, module, _, teacher = assignment
        teacher_modules[teacher] = module

    return all(0
               < data.qualifications[teacher, module]
               <= data.modules[module]["qualification"]
               for teacher, module in teacher_modules.items())
