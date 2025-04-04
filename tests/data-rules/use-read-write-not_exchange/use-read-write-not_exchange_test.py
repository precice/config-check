from precice_config_graph.nodes import DataNode, ParticipantNode

from preciceconfigchecker.rules.data_use_read_write import DataUseReadWriteRule as d

from tests.test_utils import assert_equal_violations, get_actual_violations, create_graph


def test_data_not_use_not_read_not_write():

    graph = create_graph("tests/data-rules/use-read-write-not_exchange/precice-config.xml")

    violations_actual = get_actual_violations(graph)

    for node in graph.nodes:
        if isinstance(node, DataNode):
            if node.name == "ErrorColor":
                d_error_color = node
            elif node.name == "Color":
                d_color = node
        elif isinstance(node, ParticipantNode):
            if node.name == "Generator":
                p_generator = node
            elif node.name == "Propagator":
                p_propagator = node
            elif node.name == "Alligator":
                p_alligator = node
            elif node.name == "Instigator":
                p_instigator = node

    violations_expected = []
    # ErrorColor gets written by participant Generator and read by Propagator, but not exchanged between them
    violations_expected += [d.DataNotExchangedViolation(d_error_color, p_generator, p_propagator),

                            d.DataNotExchangedViolation(d_color, p_generator, p_alligator),

                            d.DataNotExchangedViolation(d_color, p_generator, p_instigator)]

    assert_equal_violations("Data-not-exchanged-test", violations_expected, violations_actual)
