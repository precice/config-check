import sys

from severity import Severity
import color as c

from precice_config_graph import graph, xml_processing

from rule import check_all_rules, print_all_results

# ALL RULES THAT SHOULD BE CHECKED NEED TO BE IMPORTED
# SOME IDE's MIGHT REMOVE THEM AS UNUSED IMPORTS
import rules.missing_coupling

path:str = None
debug = False

if __name__ == "__main__":
    arguments = sys.argv
    if len(arguments) > 3:
        sys.exit(f"[{Severity.ERROR.value}]: too many arguments.")
    for argument in arguments:
        if argument == arguments[0]:
            pass
        elif argument.endswith(".xml"):
            path = argument
        elif argument == "--debug":
            debug = True
            print(f"[{Severity.DEBUG.value}]: debug mode enabled")
        else:
            sys.exit(f"[{Severity.ERROR.value}]: {c.dyeing(argument, c.cyan)} is an invalid argument.")
    if not path:
        sys.exit(f"[{Severity.ERROR.value}]: No path was passed as an argument.")

    print(f"Checking file at {c.dyeing(path, c.cyan)}")

    # Step 1: Use preCICE itself to check for basic errors
    # TODO: Participant.check(...)

    # Step 2: Detect more issues through the use of a graph
    root = xml_processing.parse_file(path)
    graph = graph.get_graph(root)

    # individual checks need the graph
    print("Checking all rules...")
    check_all_rules(graph)

    # if the user uses severity=debug, then the severity has to be passed here as an argument
    print_all_results()
    print("All rules checked")
