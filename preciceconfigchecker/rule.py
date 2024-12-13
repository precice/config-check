from typing import List
from abc import ABC, abstractmethod
from violation import Violation
from severity import Severity

rules = []


class Rule(ABC):
    @property
    @abstractmethod
    def problem(self) -> str: pass
    @property
    @abstractmethod
    def severity(self) -> Severity: pass

    complete_output:str = ""
    violations:List[Violation] = []

    @abstractmethod
    def __init__(self) -> None:
        self.violations = []
        self.complete_output = ""
        self.add_self_to_list()

    def add_self_to_list(self) -> None:
        rules.append(self)

    @abstractmethod
    def check(self) -> None: pass

    def satisfied(self) -> bool:
        return (len(self.violations) == 0)

    def collect_output(self) -> None:
        if self.satisfied():
            return
        out:str = f"[{self.severity.value}]: {self.problem}"
        for violation in self.violations:
            out += violation.create_output()
        if (len(self.complete_output) > 0):
            out = f"\n{out}"
        self.complete_output = out

    def get_complete_output(self) -> str:
        return self.complete_output