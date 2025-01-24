from typing import List

from rule import Rule
from severity import Severity
from violation import Violation

class Rule_5(Rule):
    class MyViolation(Violation):
        def __init__(self, line: int) -> None:
            super().__init__(line)

        def format_explanation(self) -> str:
            return "Testing Debug"
        
        def format_possible_solutions(self) -> List[str]:
            return ["The",
                    "Test"
            ]

    severity = Severity.DEBUG
    name = "5th Example Rule"

    def check(self, graph) -> None:
        #Find violations in the graph and add them to the violations list in Rule.
        self.violations.append(self.MyViolation(42))
    
Rule_5()