from precice_config_graph import graph, xml_processing
from preciceconfigchecker.rule import rules
from preciceconfigchecker.rules_processing import check_all_rules

xml = xml_processing.parse_file("precice-config.xml")
graph = graph.get_graph(xml)

check_all_rules(graph, True)

violations = []
for rule in rules:
    if len(rule.violations) > 0:
        violations.append(rule.violations)

assert len(violations) == 0, "There seems to be an error."
print("Passed simple-good test.")
