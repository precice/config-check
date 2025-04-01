from precice_config_graph.nodes import ParticipantNode, MeshNode, Direction, MappingConstraint, MappingType

from preciceconfigchecker.rules.mapping import MappingRule as m

from tests.test_utils import assert_equal_violations, get_actual_violations, create_graph


def test_mapping():
    graph = create_graph("precice-config.xml")

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
            elif node.name == "Instigator":
                p_instigator = node
        elif isinstance(node, MeshNode):
            if node.name == "Alligator-Mesh":
                m_alligator = node
            elif node.name == "Generator-Mesh":
                m_generator = node
            elif node.name == "Propagator-Mesh":
                m_propagator = node
            elif node.name == "Instigator-Mesh":
                m_instigator = node

    violations_expected = []

    violations_expected += [m.JustInTimeMappingViolation(p_alligator, m_generator, Direction.READ)]

    violations_expected += [
        m.MappingDirectionViolation(p_propagator, p_generator, m_propagator, m_generator, Direction.WRITE)]

    violations_expected += [m.JustInTimeMappingTypeViolation(p_instigator, m_alligator, Direction.READ,
                                                             MappingType.RADIAL_GEOMETRIC_MULTISCALE)]

    violations_expected += [m.JustInTimeMappingDirectionConstraintViolation(p_instigator, m_alligator, Direction.READ,
                                                                            MappingConstraint.SCALED_CONSISTENT_SURFACE)]

    violations_expected += [
        m.JustInTimeMappingDirectionConstraintViolation(p_instigator, m_alligator,
                                                        Direction.WRITE, MappingConstraint.CONSISTENT)]

    assert_equal_violations("Mapping-test", violations_expected, violations_actual)
