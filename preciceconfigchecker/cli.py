from precice_config_graph import graph, xml_processing
from pyprecice import Participant
from collection_of_rules import CollectionOfRules


def test_rules() -> None:
    collection_of_rules: CollectionOfRules = CollectionOfRules()
    collection_of_rules.check_all_rules()
    collection_of_rules.print_result()

if __name__ == "__main__":
    path = sys.argv[1]

    print(f"Checking file at {path}")

    # Step 1: Use PreCICE itself to check for basic errors
    #TODO: Participant.check(...)

    # Step 2: Detect more issues through the use of a graph
    root = xml_processing.parse_file(path)
    graph.get_graph(root)
    test_rule()