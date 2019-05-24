from docplex.mp.model import Model

from .constraints import constraints
from .setup_decision_variables import setup_decision_variables
from .setup_objective import setup_objective
from .setup_solver_data import setup_solver_data
from .write_results import write_results


def ilp(num_exp, data):
    """
    As outlined in Niels Wouda's bachelor's thesis. Uses an LP to solve the
    classroom/teacher/module assignment problem s.t. Learner preference ordering
    is optimised.

    Parameters
    ----------
    num_exp : int
        The experiment instance number
    data : dict
        The problem-specific data

    Raises
    ------
    ValueError
        If the schedule is infeasible
    """
    assignment_problem = [list(range(len(data["learners"]))),
                          list(range(len(data["modules"]))),
                          list(range(len(data["classrooms"]))),
                          list(range(len(data["teachers"])))]

    with Model("PersonalisedLearningScheduleSolver") as solver:
        solver.parameters.threads = 8

        setup_solver_data(solver, data)  # adds data fields to solver instance
        setup_decision_variables(solver, assignment_problem)
        setup_objective(solver, data)

        # Applies given constraints to the problem (see `/constraints` for
        # details).
        for constraint in constraints:
            constraint.apply(solver, data)

        solution = solver.solve()

        if solution is None:
            raise ValueError("Infeasible!")

        print("Objective\t{0}".format(write_results(num_exp, data, solver)))
