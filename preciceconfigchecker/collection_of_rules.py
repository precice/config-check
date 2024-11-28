from rule import Severity
from rule import Rule
from typing import List


# methods for checking rules
# just testing... ignore it!!!
def testfunc(edges:List[int]):
    a:int = 0
    for i in range(0, 20000000):
        a += 1
    edges.clear()
    return False

# just testing... ignore it!!!
def testfunc2(a, b):
    print("rule is followed!")
    return True


class CollectionOfRules:
    # rule, method for rule, arguments for method
    rules = [
        [Rule(message="test"), testfunc, [[1,2,3]]],
        [Rule(Severity.INFO, "Nope", "You can't do that!"), testfunc, [[4,5,6]]],
        [Rule(Severity.WARNING, "NOOOOOPE!!!", "What's your problem?", "fuck off"), testfunc, [[7,8,9]]],
        [Rule(Severity.INFO, "test right", "just testing with true output", "nothing"), testfunc2, [10,33]]
    ]

    results:List[str] = []
    
    def check_all_rules(self) -> None:
        for r in self.rules:
            rule:Rule = r[0]
            method = r[1]
            arguments = r[2]
            rule.check_with(method, arguments)
            result:str = rule.get_result()
            if (len(result) > 0):
                self.results.append(result)

    def print_result(self) -> None:
        for result in self.results:
            print(result)
