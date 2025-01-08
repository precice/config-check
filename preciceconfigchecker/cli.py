import sys

from precice_config_graph import graph, xml_processing

from rule import check_all_rules, print_all_results

# ALL RULES THAT SHOULD BE CHECKED NEED TO BE IMPORTED
# SOME IDE's MIGHT REMOVE THEM AS UNUSED IMPORTS
import rules.missing_coupling

if __name__ == "__main__":
    path = sys.argv[1]

    print(f"Checking file at {path}")

    # Step 1: Use preCICE itself to check for basic errors
    # TODO: Participant.check(...)

    # Step 2: Detect more issues through the use of a graph
    root = xml_processing.parse_file(path)
    graph = graph.get_graph(root)

    # individual checks need the graph
    check_all_rules(graph)

    # if the user uses severity=debug, then the severity has to be passed here as an argument
    print_all_results()
    print("All rules checked")
