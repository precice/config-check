from rule import Rule
from violation import Violation
from severity import Severity

class Violation_1_3(Violation):
    def __init__(self, nodeA, nodeB) -> None:
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.explanation = f"There is a Problem with {self.nodeA} and {self.nodeB}"
        self.possible_solutions.append(f"Remove {self.nodeA}")
        self.possible_solutions.append(f"Connect {self.nodeA} with {self.nodeB}")

class Rule_1_3(Rule):
    problem = "I am Rule 1.3"
    severity = Severity.ERROR

    def __init__(self):
        super().__init__()

    def check(self) -> None:
        datas = [("NodeK", "NodeL")]
        for data in datas:
            self.violations.append(Violation_1_3(*data))

Rule_1_3()
print("1.3")