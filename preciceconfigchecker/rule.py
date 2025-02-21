from abc import ABC, abstractmethod
from typing import List

from networkx import Graph

from severity import Severity
from violation import Violation
import color as c


class Rule(ABC):
    """
    Abstract Class 'Rule'. Checking a 'Rule' for violations and producing formatted output.
    """

    number_errors: int = 0
    """Static Attribute: Do not use 'self.number_errors', use 'Rule.number_errors'"""
    number_warnings: int = 0
    """Static Attribute: Do not use 'self.number_warnings', use 'Rule.number_warnings'"""

    @property
    @abstractmethod
    def severity(self) -> Severity:
        """@abstract property: Type"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """@abstract property: Name of the rule in readable style."""
        pass

    def __init__(self) -> None:
        """
        Initializes a Rule object.
        """
        self.violations: List[Violation] = []
        rules.append(self)

    @abstractmethod
    def check(self, graph: Graph) -> None:
        """
        @abstractmethod: Defines how a 'Rule' should be checked

        Hint: Use 'self.violations.append(self.MyViolation(...))' to save the results directly. MyViolation should be an inner class of type Violation.
        """
        pass

    def satisfied(self) -> bool:
        """
        Shows when the 'Rule' is satisfied

        Returns:
            bool: TRUE, if there are no violations after the check
        """
        return self.violations.__len__() == 0

    def print_result(self, debug: bool) -> None:
        """
        If the 'Rule' has violations, these will be printed.
        If debug mode is enabled, more information is displayed.
        """
        if not debug and (self.severity == Severity.DEBUG or self.satisfied()):
            return
        if self.satisfied():
            print(f"[{Severity.DEBUG.value}]: '{c.dyeing(self.__class__.__name__, c.purple)}' is satisfied.")
            return

        severity_info: str
        if debug and self.severity != Severity.DEBUG:
            severity_info = f"[{self.severity.value},{Severity.DEBUG.value}]: ({c.dyeing(self.__class__.__name__, c.purple)})"
        elif debug and self.severity == Severity.DEBUG:
            severity_info = f"[{Severity.DEBUG.value}]: ({c.dyeing(self.__class__.__name__, c.purple)})"
        else:
            severity_info = f"[{self.severity.value}]:"
        print(f"{severity_info} {self.name}")

        for violation in self.violations:
            formatted_violation = violation.format()
            print(formatted_violation)

        if self.severity == Severity.WARNING:
            Rule.number_warnings += len(self.violations)
        if self.severity == Severity.ERROR:
            Rule.number_errors += len(self.violations)

# To handle all the rules
rules: list[Rule] = []
"""List of all initialized rules. Info: Each rule puts itself on this list when initialized."""
