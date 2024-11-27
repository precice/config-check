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


graph = []


def check_edges(graph, edges) -> bool:
    return False


class Severity(Enum):
    INFO = "Info"
    WARNING = "Warning"


class Rule:
    severity:Severity
    message:str
    possible_solution:str
    followed:bool
    edges_to_check = []# Definition from using Edges
    #Nodes?
    def __init__(self, severity:Severity = Severity.INFO, message:str = "", possible_solution:str = "", edges_to_check = []) -> None:
        self.severity = severity
        self.message = message
        self.possible_solution = possible_solution
        self.edges_to_check = edges_to_check

    def check(self) -> None:
        self.followed = check_edges(graph, self.edges_to_check)

    def output(self, number) -> None:
        if (not self.followed):
            out:str = f"[{number:2}.]" + "[" + self.severity.value + "] : " + self.message
        if (len(self.possible_solution) > 0):
            out += "\n\t[Possible Solution] : " + self.possible_solution
        print(out)


if __name__ == "__main__":
    rules = [Rule(message="test"),
             Rule(Severity.INFO, "You can't do that!", edges_to_check=[]),
             Rule(Severity.WARNING, "What's your problem?", "fuck off", [])
             ]
    number:int = 0
    for rule in rules:
        number += 1
        rule.check()
        rule.output(number)