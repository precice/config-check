from preciceconfigchecker.rules.disjoint_simulations import DisjointSimulationsRule as d
from preciceconfigchecker.rules.coupling_scheme_mapping import CouplingSchemeMappingRule as c
from preciceconfigchecker.rules.mapping import MappingRule as m
from tests.test_utils import assert_equal_violations, create_graph, get_actual_violations
from precice_config_graph.nodes import ParticipantNode, MeshNode, DataNode, Direction


def test_coupling_scheme_mapping():
    graph = create_graph("tests/coupling-scheme-mapping/precice-config.xml")

    violations_actual = get_actual_violations(graph)

    for node in graph.nodes:
        if isinstance(node, DataNode):
            if node.name == "Color":
                d_color = node
        if isinstance(node, ParticipantNode):
            if node.name == "Generator":
                p_generator = node
            elif node.name == "Propagator":
                p_propagator = node
            elif node.name == "Alligator":
                p_alligator = node
            elif node.name == "Instigator":
                p_instigator = node
            elif node.name == "Elevator":
                p_elevator = node
        elif isinstance(node, MeshNode):
            if node.name == "Generator-Mesh":
                m_generator = node
            elif node.name == "Propagator-Mesh":
                m_propagator = node
            elif node.name == "Alligator-Mesh":
                m_alligator = node
            elif node.name == "Instigator-Mesh":
                m_instigator = node

    violations_expected = [

        c.MissingMappingCouplingSchemeViolation(p_generator, p_propagator, m_generator),

        c.MissingMappingCouplingSchemeViolation(p_generator, p_propagator, m_propagator),

        c.MissingMappingAPIAccessCouplingSchemeViolation(p_alligator, p_instigator, m_alligator),

        d.SharedDataDisjointSimulationsViolation(d_color, frozenset([frozenset([p_generator, p_propagator, p_elevator]),
                                                                     frozenset([p_alligator, p_instigator])])),
        m.JustInTimeMappingMissingDataProcessingViolation(p_alligator, p_instigator, m_instigator, Direction.WRITE,
                                                          m.MissingDataProcessing.READ_DATA)
    ]

    assert_equal_violations("Coupling-scheme-mapping-test", violations_expected, violations_actual)
