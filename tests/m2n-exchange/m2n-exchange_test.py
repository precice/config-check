import contextlib
import io

from precice_config_graph import graph as g, xml_processing
from precice_config_graph.nodes import ParticipantNode

from preciceconfigchecker.rule import rules
from preciceconfigchecker.rules.m2n_exchange import M2NExchangeRule as e
from preciceconfigchecker.rules_processing import check_all_rules, print_all_results
from tests.test_utils import assert_equal_violations


def test_m2n_exchange():
    xml = xml_processing.parse_file("precice-config.xml")
    graph = g.get_graph(xml)

    violations_actual = []

    with contextlib.redirect_stdout(io.StringIO()):
        violations_by_rule = check_all_rules(graph, True)

    for rule in rules:
        violations_actual += violations_by_rule[rule]

    violations_expected = []

    for node in graph.nodes:
        if isinstance(node, ParticipantNode):
            if node.name == "Alligator":
                n_alligator = node
            elif node.name == "Generator":
                n_generator = node
            elif node.name == "Propagator":
                n_propagator = node

    violations_expected += [e.MissingM2NEchangeViolation(n_alligator),
                            e.DuplicateM2NExchangeViolation(n_generator, n_propagator)]



    assert_equal_violations("M2N-Exchange test", violations_expected, violations_actual)
