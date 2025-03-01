from precice_config_graph import graph as g, xml_processing
from tests.test_utils import assert_equal_violations, get_actual_violations


def test_simple_good():
    xml = xml_processing.parse_file("tests/simple-good/precice-config.xml")
    graph = g.get_graph(xml)

    violations_actual = get_actual_violations(graph)

    # No violations are expected
    violations_expected = []

    assert_equal_violations("Simple-good test", violations_expected, violations_actual)
