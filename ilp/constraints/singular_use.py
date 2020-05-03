from heuristic.classes import Problem


def singular_use(solver):
    """
    Ensures each classroom and each teacher are used exactly once.
    """
    problem = Problem()

    for teacher in range(len(problem.teachers)):
        classrooms = solver.sum(
            solver.module_resources[module, classroom, teacher]
            for module in range(len(problem.modules))
            for classroom in range(len(problem.classrooms)))

        # Each teacher may be assigned to *at most* one classroom.
        solver.add_constraint(classrooms <= 1)

    for classroom in range(len(problem.classrooms)):
        teachers = solver.sum(
            solver.module_resources[module, classroom, teacher]
            for module in range(len(problem.modules))
            for teacher in range(len(problem.teachers)))

        # Each classroom may be assigned to *at most* one teacher.
        solver.add_constraint(teachers <= 1)
