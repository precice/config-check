import contextlib
import io

from precice_config_graph import graph as g, xml_processing
from precice_config_graph.nodes import ParticipantNode

from preciceconfigchecker.rules_processing import check_all_rules
from preciceconfigchecker.rule import rules

from preciceconfigchecker.rules.compositional_coupling import CompositionalCouplingRule as c

from tests.test_utils import assert_equal_violations


def test_missing_coupling_scheme():
    xml = xml_processing.parse_file("tests/compositional-coupling/precice-config.xml")
    graph = g.get_graph(xml)

    violations_actual = []

    # To suppress terminal messages
    with contextlib.redirect_stdout(io.StringIO()):
        # Debug=True might find additional violations, if they are of the severity "debug".
        violations_by_rule = check_all_rules(graph, True)

    for rule in rules:
        violations_actual += violations_by_rule[rule]

    # Extract nodes from graph to build custom violations
    for node in graph.nodes():
        if isinstance(node, ParticipantNode):
            if node.name == "Generator":
                n_generator = node
            elif node.name == "Propagator":
                n_propagator = node
            elif node.name == "Alligator":
                n_alligator = node

    violations_expected = []
    violations_expected += [c.CompositionalDeadlockViolation([n_generator, n_propagator, n_alligator])]

    assert_equal_violations("Compositional-coupling test", violations_expected, violations_actual)
