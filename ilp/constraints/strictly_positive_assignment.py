import itertools

from utils import Data


def strictly_positive_assignment(data: Data, solver):
    """
    Ensures learners are assigned only to modules for which they hold a
    strictly positive preference. This guarantees learners are not assigned
    to modules they are currently ineligible to take.
    """
    for learner, module in itertools.product(range(len(data.learners)),
                                             range(len(data.modules))):
        preference = data.preferences[learner, module] \
            * solver.assignment[learner, module]

        grace = solver.B * (1 - solver.assignment[learner, module])

        # For each learner and module assignment, the preference for that
        # module needs to be strictly positive - unless the learner is not
        # assigned, in which case we use a grace term to ensure the constraint
        # holds.
        solver.add_constraint(preference + grace >= 0.00001)
