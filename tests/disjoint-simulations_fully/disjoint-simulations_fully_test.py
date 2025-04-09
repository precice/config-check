from precice_config_graph.nodes import ParticipantNode
from preciceconfigchecker.rules.disjoint_simulations import DisjointSimulationsRule as r

from tests.test_utils import assert_equal_violations, get_actual_violations, create_graph


def test_fully_disjoint_simulations():
    graph = create_graph("tests/disjoint-simulations_fully/precice-config.xml")

    violations_actual = get_actual_violations(graph)

    for node in graph.nodes:
        if isinstance(node, ParticipantNode):
            if node.name == "GeneratorA":
                n_generator_a = node
            elif node.name == "PropagatorA":
                n_propagator_a = node
            elif node.name == "GeneratorB":
                n_generator_b = node
            elif node.name == "PropagatorB":
                n_propagator_b = node

    violations_expected = [r.FullyDisjointSimulationsViolation(frozenset([
        frozenset([n_generator_a, n_propagator_a]), frozenset([n_generator_b, n_propagator_b])
    ]))]

    assert_equal_violations("Fully Disjoint-simulations test", violations_expected, violations_actual)
