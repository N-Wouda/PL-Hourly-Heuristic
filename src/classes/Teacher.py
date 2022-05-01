from dataclasses import dataclass

from .Module import Module


@dataclass(frozen=True)
class Teacher:
    id: int

    def is_qualified_for(self, module: Module) -> bool:
        """
        Tests if this teacher is qualified to teach the passed-in module.
        """
        from .Problem import Problem

        if module.is_self_study():
            return True

        problem = Problem()

        # A teach is qualified only if its qualification degree is lower than
        # or equal to that required by the module. E.g. teacher is first (1),
        # and module requires only second or third degree (2, resp. 3).  A
        # qualification of 0 indicates the teacher is *not* qualified.
        t_qualification = problem.qualifications[self.id, module.id]
        return 0 < t_qualification <= module.qualification
