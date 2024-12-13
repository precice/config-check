from rule import Rule
from violation import Violation
from severity import Severity

class Violation_2_1(Violation):
    def __init__(self, nodeA) -> None:
        self.nodeA = nodeA
        self.explanation = f"There is a Problem with {self.nodeA}"
        self.possible_solutions.append(f"Remove {self.nodeA}")

class Rule_2_1(Rule):
    problem = "I am Rule 2.1"
    severity = Severity.WARNING

    def __init__(self):
        super().__init__()

    def check(self) -> None:
        datas = ["NodeQ", "NodeR", "NodeS"]
        for data in datas:
            self.violations.append(Violation_2_1(data))

Rule_2_1()
print("2.1")