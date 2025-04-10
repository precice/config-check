from preciceconfigchecker.rule import Rule
from preciceconfigchecker.severity import Severity
from preciceconfigchecker.violation import Violation

class Rule_5(Rule):
    class MyViolation1(Violation):
        severity = Severity.DEBUG

        def __init__(self, line: int) -> None:
            super().__init__(line)

        def format_explanation(self) -> str:
            return "Testing Debug"
        
        def format_possible_solutions(self) -> list[str]:
            return ["The",
                    "Test"
            ]
        
    class MyViolation2(Violation):
        severity = Severity.DEBUG
        
        def __init__(self, test:str, line: int) -> None:
            self.test = test
            super().__init__(line)

        def format_explanation(self) -> str:
            return f"{self.test} Debug"
        
        def format_possible_solutions(self) -> list[str]:
            return ["The",
                    "Test"
            ]

    name = "5th Example Rule"

    def check(self, graph) -> list[Violation]:
        #Find violations in the graph and return them.
        return [ self.MyViolation1(42),
                 self.MyViolation2('Testing', 69) 
                 ]