from preciceconfigcheck.rule import Rule
from preciceconfigcheck.severity import Severity
from preciceconfigcheck.violation import Violation


class Rule_2(Rule):
    class MyViolation(Violation):
        severity = Severity.WARNING

        def __init__(self, node_a: str, node_b: str, node_c: str) -> None:
            self.node_a = node_a
            self.node_b = node_b
            self.node_c = node_c

        def format_explanation(self) -> str:
            return f"Something went wrong between {self.node_a}, {self.node_b} and {self.node_c}"

        def format_possible_solutions(self) -> list[str]:
            return [
                f"Delete {self.node_a}",
                f"Delete {self.node_b}",
                f"Delete {self.node_c}",
                f"Connect {self.node_a} and {self.node_b}",
                f"Connect {self.node_a} and {self.node_c}",
                f"Connect {self.node_a} and {self.node_b} and {self.node_a} and {self.node_c}",
            ]

    name = "2nd Example Rule"

    def check(self, graph) -> list[Violation]:
        # Find violations in the graph and return them.
        return [self.MyViolation("Node-G", "Node-H", "Node-I")]
