from networkx import Graph

from preciceconfigchecker.rule import Rule, rules
from preciceconfigchecker.severity import Severity

# ALL RULES THAT SHOULD BE CHECKED NEED TO BE IMPORTED
# SOME IDE's MIGHT REMOVE THEM AS UNUSED IMPORTS
from preciceconfigchecker.rules import missing_coupling
from preciceconfigchecker.rules import missing_exchange
from preciceconfigchecker.rules import data_use_read_write


def all_rules_satisfied() -> bool:
    """
    Checks whether all rules are satisfied.

    Returns:
        bool: TRUE, if all rules are satisfied.
    """
    return all(rule.satisfied() for rule in rules)


def check_all_rules(graph: Graph, debug: bool) -> None:
    """
    Checks all rules for violations
    """
    print("\nChecking rules...")
    for rule in rules:
        if debug or rule.severity != Severity.DEBUG:
            rule.check(graph)
    print("Rules checked.")


def print_all_results(debug: bool) -> None:
    """
    Prints all existing violations of all rules
    """
    if not all_rules_satisfied():
        print("The following issues were found:")
    for rule in rules:
        rule.print_result(debug)
    error_str: str = f"{Severity.ERROR.value}"
    warning_str: str = f"{Severity.WARNING.value}"
    if Rule.number_errors != 1:
        error_str += "s"
    if Rule.number_warnings != 1:
        warning_str += "s"
    if Rule.number_errors != 0 or Rule.number_warnings != 0:
        print(f"Your configuration file raised {Rule.number_errors} {error_str} "
              f"and {Rule.number_warnings} {warning_str}.")
        print("Please review your configuration file before continuing.")
    else:
        print("You are all set to start you simulation!")
