from networkx import Graph

import preciceconfigchecker.color as c
from preciceconfigchecker.rule import Rule
# ALL RULES THAT SHOULD BE CHECKED NEED TO BE IMPORTED
# SOME IDE's MIGHT REMOVE THEM AS UNUSED IMPORTS
# noinspection PyUnresolvedReferences
from preciceconfigchecker.rules import missing_coupling, missing_exchange, data_use_read_write, compositional_coupling, \
    m2n_exchange
from preciceconfigchecker.severity import Severity
from preciceconfigchecker.violation import Violation

rules: list[Rule] = [
    missing_coupling.MissingCouplingSchemeRule(),
    missing_exchange.MissingExchangeRule(),
    data_use_read_write.DataUseReadWriteRule(),
    compositional_coupling.CompositionalCouplingRule(),
    m2n_exchange.M2NExchangeRule()
]

def has_satisfied_rules(violations_by_rule: dict[Rule, list[Violation]], debug:bool) -> bool:
    """
    Checks if at least one rule is satisfied.
    If debug mode is enabled, violations with severity level DEBUG are also considered.

    Args:
        violations_by_rule (dict[Rule, list[Violation]]): of rules and their violations that need to be checked.
        debug (bool): for debug mode.

    Returns:
        bool: True, if at least one rule is satisfied.
    """
    for (rule, violations) in violations_by_rule.items():
        if rule.satisfied(violations, debug):
            return True
    return False

def has_unsatisfied_rules(violations_by_rule: dict[Rule, list[Violation]], debug:bool):
    """
    Checks if at least one rule is unsatisfied.
    If debug mode is enabled, violations with severity level DEBUG are also considered.

    Args:
        violations_by_rule (dict[Rule, list[Violation]]): of rules and their violations that need to be checked.
        debug (bool): for debug mode.

    Returns:
        bool: True, if at least one rule is unsatisfied.
    """
    for (rule, violations) in violations_by_rule.items():
        if not rule.satisfied(violations, debug):
            return True
    return False

def check_all_rules(graph: Graph, debug: bool) -> dict[Rule, list[Violation]]:
    """
    Checks a graph for violations according to the rules.
    If debug mode is enabled, violations with severity level DEBUG are also considered.

    Args:
        graph (Graph): that needs to be checked with all rules.
        debug (bool): for debug mode.

    Returns:
        dict[Rule, list[Violation]]: of rules and their violations.
    """
    print("")
    if debug:
        print("Checking rules...")

    violations_by_rule = {}
    for rule in rules:
        violations_by_rule[rule] = rule.check(graph)

    if debug:
        print("Rules checked.\n")

    return violations_by_rule


def print_all_results(violations_by_rule: dict[Rule, list[Violation]], debug: bool) -> None:
    """
    Prints all existing violations of all rules.
    If debug mode is enabled, violations with severity level DEBUG are also considered.

    Args:
        violations_by_rule (dict[Rule, list[Violation]]): of rules and their violations that must be printed.
        debug (bool): for debug mode.

    Returns:
        None
    """
    if not all_rules_satisfied(violations_by_rule, debug):
        print("The following issues were found:\n")
    for (rule, violations) in violations_by_rule.items():
        print_result(rule, violations, debug)

    def total_violations_by_severity(severity: Severity) -> int:
        """
        Counts how many violations of a severity type there are.

        Args:
            severity (Severity): type that must be counted.

        Returns:
            int: Number of severity type.
        """
        result:int = 0
        for violations in violations_by_rule.values():
            for violation in violations:
                if violation.severity.name == severity.name:
                    result += 1
        return result

    total_num_errors = total_violations_by_severity(Severity.ERROR)
    total_num_warnings = total_violations_by_severity(Severity.WARNING)

    if total_num_errors != 0 or total_num_warnings != 0:
        error_str: str = Severity.ERROR.value + ("s" if total_num_errors != 1 else "")
        warning_str: str = Severity.WARNING.value + ("s" if total_num_warnings != 1 else "")
        print(f"Your configuration file raised {total_num_errors} {error_str} "
              f"and {total_num_warnings} {warning_str}.")
        print("Please review your configuration file before continuing.")
    else:
        print("You are all set to start you simulation!")


def print_result(rule: Rule, violations: list[Violation], debug: bool) -> None:
    """
    If the rule has violations, these will be printed.
    If debug mode is enabled, more information is displayed.

    Args:
        rule (Rule): that must be printed.
        violations (list[Violation]): that must be printed.
        debug (bool): for debug mode.

    Returns:
        None
    """
    if not debug and Rule.satisfied(violations, debug):
        return
    elif Rule.satisfied(violations, debug):
        print(f"[{Severity.DEBUG.value}]: '{c.dyeing(rule.__class__.__name__, c.purple)}' is satisfied.\n")
        return
    else:
        print(f"{rule.name}")

        for violation in violations:
            if debug or violation.severity.name != Severity.DEBUG.name:
                formatted_violation = violation.format(debug)
                print(formatted_violation)

        print("")
