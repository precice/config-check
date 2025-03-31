from precice_config_graph.nodes import ParticipantNode, MeshNode

from preciceconfigchecker.rules.mapping import MappingRule as m

from tests.test_utils import assert_equal_violations, get_actual_violations, create_graph


def test_mapping():
    graph = create_graph("tests/mapping/precice-config.xml")

    violations_actual = get_actual_violations(graph)

    # extract nodes from graph to build expected violations
    for node in graph.nodes():
        if isinstance(node, ParticipantNode):
            if node.name == "Alligator":
                p_alligator = node
            elif node.name == "Generator":
                p_generator = node
            elif node.name == "Propagator":
                p_propagator = node
        elif isinstance(node, MeshNode):
            if node.name == "Alligator-Mesh":
                m_alligator = node
            elif node.name == "Generator-Mesh":
                m_generator = node
            elif node.name == "Propagator-Mesh":
                m_propagator = node

    violations_expected = []

    violations_expected += [m.JustInTimeMappingViolation(p_alligator, m_generator, "from")]

    violations_expected += [m.MappingDirectionViolation(p_propagator,p_generator, m_propagator,  m_generator,"from")]

    assert_equal_violations("Mapping-test", violations_expected, violations_actual)
