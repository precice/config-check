import contextlib
import io

from precice_config_graph import graph as g, xml_processing
from precice_config_graph.nodes import DataNode, ParticipantNode

from preciceconfigchecker.rules_processing import check_all_rules, print_all_results
from preciceconfigchecker.rule import rules
from preciceconfigchecker import color

from preciceconfigchecker.rules.compositional_coupling import CompositionalCouplingRule as c


def equals(a, b):
    if type(a) != type(b):
        return False
    return vars(a) == vars(b)


def test_missing_coupling_scheme():
    xml = xml_processing.parse_file("precice-config.xml")
    graph = g.get_graph(xml)

    violations_actual = []

    # To suppress terminal messages
    with contextlib.redirect_stdout(io.StringIO()):
        # Debug=True might find additional violations, if they are of the severity "debug".
        violations_by_rule = check_all_rules(graph, True)

    for rule in rules:
        violations_actual += violations_by_rule[rule]

    # Extract nodes from graph to build custom violations
    for node in graph.nodes():
        if isinstance(node, ParticipantNode):
            if node.name == "Generator":
                n_generator = node
            elif node.name == "Propagator":
                n_propagator = node
            elif node.name == "Alligator":
                n_alligator = node

    violations_expected = []
    violations_expected += [c.CompositionalDeadlockViolation([n_generator, n_propagator, n_alligator])]

    # Sort them so that violations of the same type are in the same order
    violations_expected_s = sorted(violations_expected, key=lambda obj: type(obj).__name__)
    violations_actual_s = sorted(violations_actual, key=lambda obj: type(obj).__name__)

    assert len(violations_actual_s) == len(violations_expected_s), (
        f"[Compositional-coupling test] Different number of expected- and actual violations.\n"
        f"   Number of expected violations: {len(violations_expected)},\n"
        f"   Number of actual violations: {len(violations_actual)}.")

    for violation_e, violation_a in zip(violations_expected_s, violations_actual_s):
        assert equals(violation_a, violation_e), (
            "[Compositional-coupling test] Expected- and actual violations do not match.\n"
            f"   Expected violation: {violation_e.format_explanation()}\n"
            f"   Actual violation: {violation_a.format_explanation()}")
    # Only gets reached if no AssertionError gets raised
    print(f"[Compositional-coupling test] {color.dyeing("Passed", color.green)}.")
