from precice_config_graph.nodes import ParticipantNode, DataNode
from preciceconfigchecker.rules.disjoint_simulations import DisjointSimulationsRule as r

from tests.test_utils import assert_equal_violations, get_actual_violations, create_graph


def test_partly_disjoint_simulations():
    graph = create_graph("tests/disjoint-simulations_shared-data/precice-config.xml")

    violations_actual = get_actual_violations(graph)

    for node in graph.nodes:
        if isinstance(node, ParticipantNode):
            if node.name == "GeneratorA":
                p_generator_a = node
            elif node.name == "PropagatorA":
                p_propagator_a = node
            elif node.name == "GeneratorB":
                p_generator_b = node
            elif node.name == "PropagatorB":
                p_propagator_b = node
        elif isinstance(node, DataNode):
            if node.name == "Color":
                d_color = node

    violations_expected = [r.SharedDataDisjointSimulationsViolation(
        d_color,
        frozenset([
            frozenset([p_generator_a, p_propagator_a]), frozenset([p_generator_b, p_propagator_b])
        ])
    )]

    assert_equal_violations("Disjoint-simulations with shared data test", violations_expected, violations_actual)
