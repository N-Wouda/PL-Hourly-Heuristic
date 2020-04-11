from heuristic.classes import Module, Solution, Teacher, Problem


def find_teacher(solution: Solution, module: Module) -> Teacher:
    """
    Finds a teacher that can teach the passed-in module. If none exist, this
    function raises a LookupError.
    """
    problem = Problem()

    available_teachers = set(problem.teachers) - solution.used_teachers()

    # Since self-study does not actually require any specific qualification.
    if module.is_self_study():
        return next(iter(available_teachers))

    qualified_teachers = [teacher for teacher in available_teachers
                          if teacher.is_qualified_for(module)]

    if not qualified_teachers:
        raise LookupError(f"No qualified, available teachers for {module}.")

    return qualified_teachers[0]
