from rule import Rule
from severity import Severity
from violation import Violation

class Rule_5(Rule):
    class MyViolation(Violation):
        def __init__(self, line: int) -> None:
            super().__init__(line)

        def format_explanation(self) -> str:
            return "Testing Debug"
        
        def format_possible_solutions(self) -> list[str]:
            return ["The",
                    "Test"
            ]

    severity = Severity.DEBUG
    name = "5th Example Rule"

    def check(self, graph) -> list[Violation]:
        #Find violations in the graph and return them.
        return [ self.MyViolation(42) ]