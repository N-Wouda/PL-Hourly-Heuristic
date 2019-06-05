import itertools

from utils import Data


def room_type(data: Data, solver):
    for j, k in itertools.product(range(len(data.modules) - 1),
                                  range(len(data.classrooms))):

        assignment = solver.sum(solver.module_resources[j, k, l]
                                for l in range(len(data.teachers)))

        m_r = data.modules[j]["room_type"]
        c_r = data.classrooms[k]["room_type"]

        solver.add_constraint((m_r - c_r) * assignment == 0)  # eq. (19)
