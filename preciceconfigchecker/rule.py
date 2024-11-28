from enum import Enum


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

    def check_with(self, check_method, args) -> None:
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