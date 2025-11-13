from precice_config_graph.nodes import ParticipantNode, MeshNode, DataNode
import precice_config_graph.enums as e

from preciceconfigcheck.rules.disjoint_simulations import DisjointSimulationsRule as d
from preciceconfigcheck.rules.coupling_scheme_mapping import (
    CouplingSchemeMappingRule as c,
)
from preciceconfigcheck.rules.mapping import (
    MappingRule as m,
    MissingDataProcessing as mdp,
)
from preciceconfigcheck.rules.receive_mesh import ReceiveMeshRule as r

from tests.test_utils import (
    assert_equal_violations,
    create_graph,
    get_actual_violations,
)


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
        c.MissingMappingCouplingSchemeViolation(
            p_generator, p_propagator, m_generator, d_color
        ),
        c.MissingMappingCouplingSchemeViolation(
            p_generator, p_propagator, m_propagator, d_color
        ),
        c.MissingMappingAPIAccessCouplingSchemeViolation(
            p_alligator, p_instigator, m_alligator, d_color
        ),
        d.SharedDataDisjointSimulationsViolation(
            d_color,
            frozenset(
                [
                    frozenset([p_generator, p_propagator, p_elevator]),
                    frozenset([p_alligator, p_instigator]),
                ]
            ),
        ),
        m.JustInTimeMappingMissingDataProcessingViolation(
            p_alligator, p_instigator, m_instigator, e.Direction.WRITE, mdp.READ_DATA
        ),
        r.UnusedReceiveMesh(p_generator, m_propagator),
        r.UnusedReceiveMesh(p_propagator, m_generator),
    ]

    assert_equal_violations(
        "Coupling-scheme-mapping-test", violations_expected, violations_actual
    )
