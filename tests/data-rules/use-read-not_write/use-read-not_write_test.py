from precice_config_graph.nodes import DataNode, MeshNode, ParticipantNode

from preciceconfigchecker.rules.data_use_read_write import DataUseReadWriteRule as d

from tests.test_utils import assert_equal_violations, get_actual_violations, create_graph


def test_data_not_use_not_read_not_write():
    graph = create_graph("tests/data-rules/use-read-not_write/precice-config.xml")

    violations_actual = get_actual_violations(graph)

    for node in graph.nodes:
        if isinstance(node, DataNode):
            if node.name == "ErrorColor":
                d_error_color = node
        elif isinstance(node, ParticipantNode):
            if node.name == "Generator":
                p_generator = node
            elif node.name == "Alligator":
                p_alligator = node
        elif isinstance(node, MeshNode):
            if node.name == "Water-Generator-Mesh":
                m_water_generator = node
            elif node.name == "Food-Generator-Mesh":
                m_food_generator = node

    violations_expected = []
    # ErrorColor gets used in Generator-Mesh, gets read by participant Generator, does not get written
    violations_expected += [
        d.DataUsedReadNotWrittenViolation(d_error_color, m_water_generator, [p_generator, p_alligator]),

        d.DataUsedReadNotWrittenViolation(d_error_color, m_food_generator, [p_generator])]

    assert_equal_violations("Data used, read, not written-test", violations_actual, violations_expected)
