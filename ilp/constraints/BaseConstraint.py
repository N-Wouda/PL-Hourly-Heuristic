class BaseConstraint(object):

    @staticmethod
    def apply(solver, data):
        raise NotImplementedError("To be implemented by subclasses")
