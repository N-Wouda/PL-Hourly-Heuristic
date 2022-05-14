from dataclasses import dataclass

from .Module import Module


@dataclass(frozen=True)
class Teacher:
    id: int
    degree: int
    frm_module: int
    to_module: int

    def is_qualified_for(self, module: Module) -> bool:
        """
        Tests if this teacher is qualified to teach the passed-in module.
        """
        if module.is_self_study():
            return True

        if self.degree > module.qualification:
            return False

        return self.frm_module <= module.id < self.to_module
