from preciceconfigchecker.rules.disjoint_simulations import DisjointSimulationsRule as r

from tests.test_utils import assert_equal_violations, get_actual_violations, create_graph


def test_partly_disjoint_simulations():
    graph = create_graph("tests/disjoint-simulations_shared-data/precice-config.xml")

    violations_actual = get_actual_violations(graph)

    violations_expected = [r.SharedDataDisjointSimulationsViolation(
        frozenset([
            frozenset(["GeneratorA", "PropagatorA"]), frozenset(["GeneratorB", "PropagatorB"])
        ]),
        "Color"
    )]

    assert_equal_violations("Disjoint-simulations with shared data test", violations_expected, violations_actual)
