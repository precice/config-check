import argparse
import sys

from preciceconfigchecker.severity import Severity
import preciceconfigchecker.color as c

from precice_config_graph import graph, xml_processing

from preciceconfigchecker.rules_processing import check_all_rules, print_all_results

def main():
    path: str = None
    debug: bool = False
    parser = argparse.ArgumentParser(usage='%(prog)s',
                                     description='Checks a preCICE config.xml file for logical errors.')
    parser.add_argument('src', type=argparse.FileType('r'), help='Path of the config.xml source file.')
    parser.add_argument('-d', '--debug', action='store_true', help='Enables debug mode')
    args = parser.parse_args()

    if args.debug:
        debug = args.debug
        print(f"[{Severity.DEBUG.value}]: Debug mode enabled")
    if args.src.name.endswith('.xml'):
        path = args.src.name
        print(f"Checking file at '{c.dyeing(path, c.cyan)}'")
    else:
        sys.exit(f"[{Severity.ERROR.value}]: '{c.dyeing(args.src.name, c.cyan)}' is not an xml file")

    # Step 1: Use preCICE itself to check for basic errors
    # TODO: Participant.check(...)

    # Step 2: Detect more issues through the use of a graph
    root = xml_processing.parse_file(path)
    G = graph.get_graph(root)

    # Individual checks need the graph
    violations_by_rule = check_all_rules(G, debug)

    # if the user uses severity=debug, then the severity has to be passed here as an argument
    print_all_results(violations_by_rule, debug)

if __name__ == "__main__":
    sys.exit(main())
