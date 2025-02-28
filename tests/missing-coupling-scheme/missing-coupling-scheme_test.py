import contextlib
import io

from precice_config_graph import graph as g, xml_processing
from precice_config_graph.nodes import DataNode, ParticipantNode

from preciceconfigchecker.rules_processing import check_all_rules
from preciceconfigchecker.rule import rules

from preciceconfigchecker.rules.missing_coupling import MissingCouplingSchemeRule as c
from preciceconfigchecker.rules.data_use_read_write import DataUseReadWriteRule as d
from tests.test_utils import assert_equal_violations


def test_missing_coupling_scheme():
    xml = xml_processing.parse_file("tests/missing-coupling-scheme/precice-config.xml")
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
        if isinstance(node, DataNode):
            if node.name == "Color":
                n_color = node
        if isinstance(node, ParticipantNode):
            if node.name == "Generator":
                n_generator = node
            elif node.name == "Propagator":
                n_propagator = node

    violations_expected = []

    v_missing_coupling_scheme = c.MissingCouplingSchemeViolation()
    violations_expected += [v_missing_coupling_scheme]

    v_data_not_exchanged = d.DataNotExchangedViolation(n_generator, n_propagator, n_color)
    violations_expected += [v_data_not_exchanged]

    assert_equal_violations("Missing-coupling-scheme test", violations_expected, violations_actual)
