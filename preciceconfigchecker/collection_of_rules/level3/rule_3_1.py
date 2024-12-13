from rule import Rule
from violation import Violation
from severity import Severity

class Violation_3_1(Violation):
    def __init__(self, nodeA, nodeB, nodeC) -> None:
        self.nodeA = nodeA
        self.nodeB = nodeB
        self.nodeC = nodeC
        self.explanation = f"There is a Problem with {self.nodeA}, {self.nodeB} and {self.nodeC}"
        self.possible_solutions.append(f"Remove {self.nodeA}")
        self.possible_solutions.append(f"Remove {self.nodeB}")
        self.possible_solutions.append(f"Remove {self.nodeC}")
        self.possible_solutions.append(f"Remove {self.nodeA} and {self.nodeB}")
        self.possible_solutions.append(f"Remove {self.nodeB} and {self.nodeC}")
        self.possible_solutions.append(f"Remove {self.nodeA} and {self.nodeC}")
        self.possible_solutions.append(f"Remove {self.nodeA}, {self.nodeB} and {self.nodeC}")

class Rule_3_1(Rule):
    problem = "I am Rule 3.1"
    severity = Severity.ERROR

    def __init__(self):
        super().__init__()

    def check(self) -> None:
        datas = [("NodeT", "NodeU", "NodeV")]
        for data in datas:
            self.violations.append(Violation_3_1(*data))

Rule_3_1()
print("3.1")