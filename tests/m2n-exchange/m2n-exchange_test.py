from precice_config_graph.nodes import ParticipantNode
from preciceconfigcheck.rules.m2n_exchange import M2NExchangeRule as e
from preciceconfigcheck.rules.disjoint_simulations import DisjointSimulationsRule as d
from tests.test_utils import (
    assert_equal_violations,
    create_graph,
    get_actual_violations,
)


def test_m2n_exchange():
    graph = create_graph("tests/m2n-exchange/precice-config.xml")

    violations_actual = get_actual_violations(graph)

    for node in graph.nodes:
        if isinstance(node, ParticipantNode):
            if node.name == "Alligator":
                n_alligator = node
            elif node.name == "Generator":
                n_generator = node
            elif node.name == "Propagator":
                n_propagator = node
            elif node.name == "Instigator":
                n_instigator = node

    violations_expected = [
        e.MissingM2NExchangeViolation(n_alligator),
        e.DuplicateM2NExchangeViolation(n_generator, n_propagator),
        d.FullyDisjointSimulationsViolation(
            frozenset(
                [
                    frozenset([n_generator, n_propagator, n_instigator]),
                    frozenset([n_alligator]),
                ]
            )
        ),
    ]

    assert_equal_violations("M2N-Exchange test", violations_expected, violations_actual)
