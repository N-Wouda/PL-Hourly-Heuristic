import itertools

from utils import Data
from heuristic.classes import Problem


def teaching_qualification(solver):
    """
    The teaching qualification constraint ensures teacher-module assignments
    are feasible. Each module has a teaching qualification requirement, and
    each teacher has a qualification for each module. Qualifications are
    ordinal as {0, 1, 2, 3}, where ``0`` indicates no qualification, and the
    rest are in decreasing level of qualification: a ``1`` is better than a
    ``2``.

    Example
    -------
    Suppose a module requires a qualification of ``2``. Then any teacher with
    an equal or better (in this case, ``2`` or ``1``) qualification is eligible
    to teach this activity.

    Note
    ----
    Since self-study has a required qualification of ``3``, every teacher is
    eligible to supervise the activity. As such, we can ignore this assignment
    here.
    """
    problem = Problem()

    for module, teacher in itertools.product(range(len(problem.modules) - 1),
                                             range(len(problem.teachers))):
        is_assigned = solver.sum(
            solver.module_resources[module, classroom, teacher]
            for classroom in range(len(problem.classrooms)))

        module_qualification = problem.modules[module].qualification
        teacher_qualification = problem.qualifications[teacher, module]

        # Module requirement must be 'less' than teacher qualification.
        solver.add_constraint(module_qualification * is_assigned
                              >= teacher_qualification * is_assigned)

        # Zero implies the teacher is not qualified, so we should ensure those
        # assignments cannot happen.
        solver.add_constraint(teacher_qualification * is_assigned
                              >= is_assigned)
