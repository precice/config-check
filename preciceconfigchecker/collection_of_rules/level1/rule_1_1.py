from rule import Rule
from violation import Violation
from severity import Severity

class Violation_1_1(Violation):
    def __init__(self, nodeA, nodeB) -> None:
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.explanation = f"There is a Problem with {nodeA} and {nodeB}"
        self.possible_solutions.append(f"Remove {self.nodeA}")
        self.possible_solutions.append(f"Connect {self.nodeA} with {self.nodeB}")

class Rule_1_1(Rule):
    problem = "I am Rule 1.1"
    severity = Severity.WARNING

    def __init__(self):
        super().__init__()

    def check(self) -> None:
        datas = [("NodeA", "NodeB"), ("NodeC", "NodeD")]
        for (nodeA, nodeB) in datas:
            self.violations.append(Violation_1_1(nodeA, nodeB))

Rule_1_1()
print("1.1")