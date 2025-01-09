from abc import ABC, abstractmethod
from typing import List

from networkx import DiGraph

from severity import Severity
from violation import Violation
import color as c


class Rule(ABC):
    """
    Abstract Class 'Rule'. Checking a 'Rule' for violations and producing formatted output.
    """

    @property
    @abstractmethod
    def severity(self) -> Severity:
        """@abstract property: Type"""
        pass

    @property
    @abstractmethod
    def problem(self) -> str:
        """@abstract property: Short explanation of what the rule is supposed to check in general."""
        pass

    def __init__(self) -> None:
        """
        Initializes a Rule object.
        """
        self.violations: List[Violation] = []
        rules.append(self)

    @abstractmethod
    def check(self, graph: DiGraph) -> None:
        """
        @abstractmethod: Defines how a 'Rule' should be checked

        Hint: Use 'self.violations.append(self.MyViolation(...))' to save the results directly. MyViolation should be an inner class of type Violation.
        """
        pass

    def satisfied(self) -> bool:
        """
        Shows when the 'Rule' is satisfied

        Returns:
            bool: TRUE if there are no violations after the check
        """
        return self.violations.__len__() == 0

    def print_result(self, debug:bool) -> None:
        """
        If the 'Rule' has violations, these will be printed.
        """
        if self.satisfied():
            if debug:
                print(f"[{Severity.DEBUG.value}]: '{c.dyeing(self.__class__.__name__, c.purple)}' is satisfied.")
        else:
            beginn:str = f"[{self.severity.value},{Severity.DEBUG.value}]: ({c.dyeing(self.__class__.__name__, c.purple)})" if debug else f"[{self.severity.value}]:"
            print(f"{beginn} {self.problem}")
            for violation in self.violations:
                formatted_violation = violation.format()
                print(formatted_violation)


# To handle all the rules

rules: List[Rule] = []
"""List of all initialized rules. Info: Each rule puts itself on this list when initialized."""


def check_all_rules(graph: DiGraph) -> None:
    """
    Checks all rules for violations
    """
    for rule in rules:
        rule.check(graph)


def print_all_results(debug:bool) -> None:
    """
    Prints all existing violations of all rules
    """
    for rule in rules:
        rule.print_result(debug)