from preciceconfigchecker.rule import Rule
from preciceconfigchecker.severity import Severity
from preciceconfigchecker.violation import Violation


class Rule_1(Rule):
    class MyViolation1(Violation):
        severity = Severity.WARNING

        def __init__(self, node_a: str, node_b: str, line: int) -> None:
            self.node_a = node_a
            self.node_b = node_b
            super().__init__(line)

        def format_explanation(self) -> str:
            return f"Something went wrong between {self.node_a} and {self.node_b}"

        def format_possible_solutions(self) -> list[str]:
            return [f"Delete {self.node_a}",
                    f"Delete {self.node_b}",
                    f"Connect {self.node_a} and {self.node_b}"
                    ]
        
    class MyViolation2(Violation):
        severity = Severity.DEBUG

        def __init__(self, node_a: str, node_b: str, line: int) -> None:
            self.node_a = node_a
            self.node_b = node_b
            super().__init__(line)

        def format_explanation(self) -> str:
            return f"Something went wrong between {self.node_a} and {self.node_b}"

        def format_possible_solutions(self) -> list[str]:
            return [f"Connect {self.node_a} and {self.node_b}"
                    ]
        

    name = "1st Example Rule"

    def check(self, graph) -> list[Violation]:
        #Find violations in the graph and return them.
        violations = [
            self.MyViolation1("Node-A", "Node-B", 1)
        ]
        # ...
        violations.append(self.MyViolation1("Node-C", "Node-D", 2))
        # ...
        violations.append(self.MyViolation2("Node-E", "Node-F", 3))
        return violations