import contextlib
import io

from precice_config_graph import graph as g, xml_processing
from precice_config_graph.nodes import DataNode, ParticipantNode

from preciceconfigchecker.rules_processing import check_all_rules
from preciceconfigchecker.rule import rules
from preciceconfigchecker import color

from preciceconfigchecker.rules.missing_coupling import MissingCouplingSchemeRule as c
from preciceconfigchecker.rules.data_use_read_write import DataUseReadWrite as d


def equals(a, b):
    if type(a) != type(b):
        return False
    return vars(a) == vars(b)


def test_missing_coupling_scheme():
    xml = xml_processing.parse_file("tests/missing-coupling-scheme/precice-config.xml")
    graph = g.get_graph(xml)

    violations_actual = []

    # To suppress terminal messages
    with contextlib.redirect_stdout(io.StringIO()):
        # Debug=True might find additional violations, if they are of the severity "debug".
        violations_by_rule = check_all_rules(graph, True)

    for rule in rules:
        violations_actual += violations_by_rule[rule]
    print(violations_actual)

    # Extract nodes from graph to build custom violations
    for node in graph.nodes():
        if isinstance(node, DataNode):
            if node.name == "Color":
                n_color = node
        if isinstance(node, ParticipantNode):
            if node.name == "Generator":
                n_generator = node
            elif node.name == "Propagator":
                n_propagator = node

    violations_expected = []

    v_missing_coupling_scheme = c.MissingCouplingSchemeViolation()
    violations_expected += [v_missing_coupling_scheme]

    v_data_not_exchanged = d.DataNotExchangedViolation(n_generator, n_propagator, n_color)
    violations_expected += [v_data_not_exchanged]

    # Sort them so that violations of the same type are in the same order
    violations_expected_s = sorted(violations_expected, key=lambda obj: type(obj).__name__)
    violations_actual_s = sorted(violations_actual, key=lambda obj: type(obj).__name__)

    assert len(violations_expected_s) == len(violations_actual_s), (
        f"[Missing-coupling-scheme test] Different number of expected- and actual violations.\n"
        f"   Number of expected violations: {len(violations_expected)},\n"
        f"   Number of actual violations: {len(violations_actual)}.")

    for violation_e, violation_a in zip(violations_expected_s, violations_actual_s):
        assert equals(violation_e, violation_a), (
            "[Missing-coupling-scheme test] Expected- and actual violations do not match.\n"
            f"   Expected violation: {violation_e.format_explanation()}\n"
            f"   Actual violation: {violation_a.format_explanation()}")
    # Only gets reached if no AssertionError gets raised
    print(f"[Missing-coupling-scheme test] {color.dyeing("Passed", color.green)}.")
