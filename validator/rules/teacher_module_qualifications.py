from typing import List, Tuple

from heuristic.classes import Problem


def teacher_module_qualifications(solution: List[Tuple]) -> bool:
    """
    Verifies each teacher-module assignment satisfies the required teacher
    qualification.
    """
    problem = Problem()
    teacher_modules = {}

    for assignment in solution:
        _, module, _, teacher = assignment
        teacher_modules[teacher] = module

    for teacher_idx, module_idx in teacher_modules.items():
        teacher = problem.teachers[teacher_idx]
        module = problem.modules[module_idx]

        if not teacher.is_qualified_for(module):
            return False

    return True
