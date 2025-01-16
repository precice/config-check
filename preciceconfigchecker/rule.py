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

    number_errors:int = 0
    """Static Attribute: Do not use 'self.number_errors', use 'Rule.number_errors'"""
    number_warnings:int = 0
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
            bool: TRUE, if there are no violations after the check
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
            severity_info:str = f"[{self.severity.value},{Severity.DEBUG.value}]: ({c.dyeing(self.__class__.__name__, c.purple)})" if debug else f"[{self.severity.value}]:"
            print(f"{severity_info} {self.name}")
            for violation in self.violations:
                formatted_violation = violation.format()
                print(formatted_violation)
            if self.severity == Severity.WARNING:
                Rule.number_warnings += len(self.violations)
            if self.severity == Severity.ERROR:
                Rule.number_errors += len(self.violations)

# To handle all the rules

rules: List[Rule] = []
"""List of all initialized rules. Info: Each rule puts itself on this list when initialized."""

def all_rules_satisfied() -> bool:
    """
    Checks whether all rules are satisfied.

    Returns:
        bool: TRUE, if all rules are satisfied.
    """
    return all(rule.satisfied() for rule in rules)


def check_all_rules(graph: DiGraph) -> None:
    """
    Checks all rules for violations
    """
    print("\nChecking rules...")
    for rule in rules:
        rule.check(graph)
    print("Rules checked.")


def print_all_results(debug:bool) -> None:
    """
    Prints all existing violations of all rules
    """
    if not all_rules_satisfied():
        print("The following issues were found:")
    for rule in rules:
        rule.print_result(debug)
    if Rule.number_errors != 0 or Rule.number_warnings != 0:
        print(f"Your configuration file raised {Rule.number_errors} {Severity.ERROR.value}s and {Rule.number_warnings} {Severity.WARNING.value}s.\nPlease review your configuration file before continuing.")
    else:
        print("You are all set to start you simulation!")
