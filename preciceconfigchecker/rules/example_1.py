from typing import List

from rule import Rule
from severity import Severity
from violation import Violation


class Rule_1(Rule):
    class MyViolation(Violation):
        def __init__(self, node_a: str, node_b: str) -> None:
            self.node_a = node_a
            self.node_b = node_b

        def format_explanation(self) -> str:
            return f"Something went wrong between {self.node_a} and {self.node_b}"

        def format_possible_solutions(self) -> List[str]:
            return [f"Delete {self.node_a}",
                    f"Delete {self.node_b}",
                    f"Connect {self.node_a} and {self.node_b}"
                    ]

    severity = Severity.INFO
    problem = "No connection between two nodes"

    def check(self) -> None:
        # Find violations in the graph and add them to the violations list in Rule.
        self.violations.append(self.MyViolation("Node-A", "Node-B"))
        self.violations.append(self.MyViolation("Node-C", "Node-D"))
        self.violations.append(self.MyViolation("Node-E", "Node-F"))


Rule_1()
