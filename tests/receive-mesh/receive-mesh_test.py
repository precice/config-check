from precice_config_graph.nodes import ParticipantNode, MeshNode

from tests.test_utils import assert_equal_violations, get_actual_violations, create_graph
from preciceconfigchecker.rules.receive_mesh import ReceiveMeshRule as r


def test_receive_mesh():
    graph = create_graph("tests/receive-mesh/precice-config.xml")

    violations_actual = get_actual_violations(graph)

    for node in graph.nodes:
        if isinstance(node, ParticipantNode):
            if node.name == "Generator":
                p_generator = node
            elif node.name == "Propagator":
                p_propagator = node
        elif isinstance(node, MeshNode):
            if node.name == "Wedding-Gift-Mesh":
                m_wedding_gift = node

    violations_expected = [
        r.UnusedReceiveMesh(p_propagator, m_wedding_gift)
    ]

    assert_equal_violations("Receive-mesh test", violations_expected, violations_actual)
