#from config-graph import buildGraph # TODO: Import adjacent library
#from pyprecice import Participant
#
#if __name__ == "__main__":
#    # Step 1: Use PreCICE itself to check for basic errors
#    Participant.check(...)
#    # Step 2: Detect more issues through the use of a graph
#    buildGraph("precice-config.xml")

from enum import Enum
from typing import List
import random


graph = []


class Severity(Enum):
    INFO = "Info"
    WARNING = "Warning"


class Rule:
    severity:Severity
    name:str
    message:str
    possible_solutions:str
    followed:bool = True
    numbers_not_followed:int = 0

    def __init__(self, severity:Severity = Severity.INFO, name:str = "Rule", message:str = "", possible_solutions:str = "") -> None:
        self.severity = severity
        self.name = name
        self.message = message
        self.possible_solutions = possible_solutions

    def check(self, check_method, args) -> None:
        result = check_method(*args)
        if type(result) is not bool:
            print("Error : The passed method does not return a bool value!")
        else:
            self.followed = result

    def get_result(self) -> str:
        if (self.followed):
            return ""
        Rule.numbers_not_followed += 1
        out:str = f"[{Rule.numbers_not_followed:2}.]" + "[" + self.severity.value + "][" + self.name + "] : " + self.message
        if (len(self.possible_solutions) > 0):
            out += "\n\t[Possible Solution] : " + self.possible_solutions
        return out


class Violations:
    violations:List[str]

    def __init__(self) -> None:
        self.violations = list()

    def add(self, violation:str) -> None:
        self.violations.append(violation)

    def print_all(self) -> None:
        for violation in self.violations:
            if (len(violation) > 0):
                print(violation)




# just testing... ignore it!!!
def testfunc(edges:List[int]):
    a:int = 0
    for i in range(0, 50000000):
        a += 1
    graph.append("a")
    edges.clear()
    return False

# just testing... ignore it!!!
def testfunc2(a, b):
    print(a+b)
    return True

# just testing... ignore it!!!
if __name__ == "__main__":
    rules = [Rule(message="test"),
             Rule(Severity.INFO, "Nope", "You can't do that!"),
             Rule(Severity.WARNING, "NOOOOOPE!!!", "What's your problem?", "fuck off")
             ]
    violations:Violations = Violations()
    for rule in rules:
        if bool(random.randint(0,1)):
            rule.check(testfunc, [[1,2,3]])
        else:
            rule.check(testfunc2, ["pa", "ss"])
        violations.add(rule.get_result())
    violations.print_all()