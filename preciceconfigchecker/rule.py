from abc import ABC, abstractmethod

from networkx import Graph

from preciceconfigchecker.severity import Severity
from preciceconfigchecker.violation import Violation


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
    def name(self) -> str:
        """@abstract property: Name of the rule in readable style."""
        pass

    def __init__(self) -> None:
        """
        Initializes a Rule object.
        """

    @abstractmethod
    def check(self, graph: Graph) -> list[Violation]:
        """
        @abstractmethod: Defines how a 'Rule' should be checked

        Hint: Implement Violations as inner classes in the rule of type Violation.
        """
        pass
