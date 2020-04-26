from heuristic.classes import Classroom, Module, Problem, Solution


def find_classroom(solution: Solution, module: Module) -> Classroom:
    """
    Finds a classroom that can host the passed-in module. If none exist, this
    function raises a LookupError.
    """
    problem = Problem()

    # TODO minimal needed, move onto solution

    # Finds the first classroom that fits the required room type, if any.
    for classroom in set(problem.classrooms) - solution.used_classrooms():
        if classroom.room_type == module.room_type:
            return classroom

        # Since self-study is generally allowed in multiple room types.
        if module.is_self_study() and classroom.is_self_study_allowed():
            return classroom

    raise LookupError(f"No qualified, available classrooms for {module}.")
