import contextlib
import io

from precice_config_graph import graph as g, xml_processing
from preciceconfigchecker.rule import rules
from preciceconfigchecker.rules_processing import check_all_rules
from tests.test_utils import assert_equal_violations


def test_simple_good():
    xml = xml_processing.parse_file("tests/simple-good/precice-config.xml")
    graph = g.get_graph(xml)

    violations_actual = []

    with contextlib.redirect_stdout(io.StringIO()):
        violations_by_rule = check_all_rules(graph, True)

    for rule in rules:
        violations_actual += violations_by_rule[rule]

    # No violations are expected
    violations_expected = []

    assert_equal_violations("Simple-good test", violations_expected, violations_actual)
