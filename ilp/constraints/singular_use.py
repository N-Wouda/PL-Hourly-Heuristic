from utils import Data


def singular_use(data: Data, solver):
    """
    Ensures each classroom and each teacher are used exactly once.
    """
    for teacher in range(len(data.teachers)):
        classrooms = solver.sum(
            solver.module_resources[module, classroom, teacher]
            for module in range(len(data.modules))
            for classroom in range(len(data.classrooms)))

        # Each teacher may be assigned to *at most* one classroom.
        solver.add_constraint(classrooms <= 1)

    for classroom in range(len(data.classrooms)):
        teachers = solver.sum(
            solver.module_resources[module, classroom, teacher]
            for module in range(len(data.modules))
            for teacher in range(len(data.teachers)))

        # Each classroom may be assigned to *at most* one teacher.
        solver.add_constraint(teachers <= 1)
