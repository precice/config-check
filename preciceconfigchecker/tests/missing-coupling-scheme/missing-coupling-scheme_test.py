from precice_config_graph import graph, xml_processing
from precice_config_graph.nodes import DataType

from preciceconfigchecker.rule import rules
from preciceconfigchecker.rules_processing import check_all_rules

from preciceconfigchecker.rules.missing_coupling import MissingCouplingSchemeRule as c
from preciceconfigchecker.rules.missing_exchange import MissingExchangeRule as e

import precice_config_graph.nodes as n

xml = xml_processing.parse_file("precice-config.xml")
graph = graph.get_graph(xml)

check_all_rules(graph, False)

violations_expected = []

v_coupling_scheme = c.MissingCouplingSchemeViolation()
violations_expected.append(v_coupling_scheme)

n_color = n.DataNode("Color", DataType.SCALAR)
n_generator = n.ParticipantNode("Generator")
n_propagator = n.ParticipantNode("Propagator")
n_propagator_mesh = n.MeshNode("Propagator-Mesh")

v_exchange = e.MissingUseDataExchangeViolation(n_color, n_propagator_mesh, n_propagator, n_generator)
violations_expected.append(v_exchange)

violations_actual = []
for rule in rules:
    for violation in rule.violations:
        violations_actual.append(violation)

violations_expected_s = sorted(violations_expected, key=lambda obj: type(obj).__name__)
violations_actual_s = sorted(violations_actual, key=lambda obj: type(obj).__name__)
