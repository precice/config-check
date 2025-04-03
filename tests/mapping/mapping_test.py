from precice_config_graph.nodes import ParticipantNode, MeshNode, Direction, MappingConstraint, MappingType

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
            elif node.name == "Instigator":
                p_instigator = node
            elif node.name == "Elevator":
                p_elevator = node
            elif node.name == "Incinerator":
                p_incinerator = node
        elif isinstance(node, MeshNode):
            if node.name == "Alligator-Mesh":
                m_alligator = node
            elif node.name == "Generator-Mesh":
                m_generator = node
            elif node.name == "Propagator-Mesh":
                m_propagator = node
            elif node.name == "Instigator-Mesh":
                m_instigator = node
            elif node.name == "Elevator-Mesh":
                m_elevator = node
            elif node.name == "Incinerator-Mesh":
                m_incinerator = node
            elif node.name == "Forsaken-Mesh":
                m_forsaken = node
            elif node.name == "Popular-Mesh":
                m_popular = node
            elif node.name == "Impostor-Mesh":
                m_impostor = node

    violations_expected = [

        m.MappingDirectionViolation(p_propagator, p_generator, m_propagator, m_generator, Direction.WRITE),

        m.IncorrectExchangeMappingViolation(p_propagator, p_generator, m_generator, Direction.WRITE),

        m.JustInTimeMappingPermissionViolation(p_alligator, p_generator, m_generator, Direction.READ),

        m.MissingCouplingSchemeMappingViolation(p_alligator, p_generator, m_generator, Direction.READ),

        m.JustInTimeMappingTypeViolation(p_instigator, p_alligator, m_alligator, Direction.READ,
                                         MappingType.RADIAL_GEOMETRIC_MULTISCALE),
        m.JustInTimeMappingFormatViolation(p_instigator, p_alligator, m_alligator, Direction.READ,
                                           MappingConstraint.SCALED_CONSISTENT_SURFACE),
        m.JustInTimeMappingFormatViolation(p_instigator, p_alligator, m_alligator, Direction.WRITE,
                                           MappingConstraint.CONSISTENT),
        m.ParallelCouplingMappingFormatViolation(p_elevator, p_instigator, m_elevator, m_instigator, Direction.READ,
                                                 MappingConstraint.CONSERVATIVE),
        m.JustInTimeMappingFormatDirectionViolation(p_incinerator, p_propagator, m_propagator, Direction.READ,
                                                    MappingConstraint.SCALED_CONSISTENT_VOLUME),
        m.MissingExchangeMappingViolation(p_elevator, p_instigator, m_instigator, Direction.READ),

        m.IncorrectExchangeMappingViolation(p_incinerator, p_propagator, m_propagator, Direction.READ),

        m.UnclaimedMeshMappingViolation(p_generator, m_forsaken, Direction.WRITE),

        m.RepeatedlyClaimedMeshMappingViolation(p_generator, [p_generator, p_incinerator], m_popular, Direction.READ),

        m.SameParticipantMappingViolation(p_incinerator, m_incinerator,Direction.READ)
    ]

    assert_equal_violations("Mapping-test", violations_expected, violations_actual)
