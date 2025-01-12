from typing import List

import networkx as nx
from networkx import Graph

from precice_config_graph.edges import Edge
from precice_config_graph.nodes import DataNode, ReadDataNode, WriteDataNode, MeshNode

from rule import Rule
from severity import Severity
from violation import Violation


class DataUsedNotReadNotWrittenRule(Rule):
    problem = "Data gets used by a mesh but nobody is reading or writing it."
    # This is an oversight, but not an error
    severity = Severity.WARNING

    class DataUsedNotReadNotWrittenViolation(Violation):

        def __init__(self, data_node: DataNode, mesh_node: MeshNode):
            self.data_node = data_node
            self.mesh_node = mesh_node

        def format_explanation(self) -> str:
            return f"Mesh {self.mesh_node.name} is using data {self.data_node.name}, which does not get written or read by any participant"

        def format_possible_solutions(self) -> List[str]:
            return [
                f"Using data {self.data_node.name} in mesh {self.mesh_node.name} but never writing or reading it could "
                f"lead to unwanted behaviour during the coupling.",
                f"Consider reading and writing {self.data_node.name} or remove it, to avoid errors."]

    def check(self, graph: Graph) -> None:
        use_data: bool = False
        read_write_data: bool = False
        mesh: MeshNode = None
        # Only data, read-/write-data and mesh nodes are important for this problem
        g1 = nx.subgraph_view(graph, filter_node=filter_data_read_write_data_mesh_nodes)
        for node in g1.nodes:
            # we focus on data nodes and their edges
            if isinstance(node, DataNode):
                edges = g1.edges(node)
                # test for use-data and read-/write data nodes: data-node has both? great; if not, then we need to catch them
                for edge in edges:
                    use_data = False
                    read_write_data = False
                    # if the data node does not have a use-data edge, then this is a different problem
                    if is_use_data(edge):
                        use_data = True
                        mesh = get_mesh_node(edge)
                    # if it has both read- and write-data edges, then all is fine; otherwise this is a different problem
                    if is_write_data(edge) or is_read_data(edge):
                        read_write_data = True
                # if both use- and read-/write data are present, great
                if use_data and read_write_data:
                    continue
                # if only use-data: we got him
                elif use_data:
                    self.violations.append(self.DataUsedNotReadNotWrittenViolation(node, mesh))
                # else: a different error


# instantiate object to add it to the rules array
DataUsedNotReadNotWrittenRule()


def get_mesh_node(edge: Edge):
    """
    Returns the mesh node of the given edge.

    This assumes the edge to connect a mesh node with a different node.
    If the edge connects two other nodes, then the behaviour is undefined.

    Args:
        edge: The edge to get the mesh node from.

    Returns:
        The mesh node of the given edge.
    """
    node1, node2 = edge
    if isinstance(node1, MeshNode):
        mesh = node1
    elif isinstance(node2, MeshNode):
        mesh = node2
    else:
        mesh = None
    return mesh


def filter_data_read_write_data_mesh_nodes(node) -> bool:
    """
    This method filters data, read-/write_data and mesh nodes.

    Args:
         node: The node to check.

    Returns:
        True, if the node is a data-, read-/write-, or mesh node.
    """
    return (isinstance(node, DataNode) or
            isinstance(node, ReadDataNode) or
            isinstance(node, WriteDataNode) or
            isinstance(node, MeshNode))


def is_use_data(edge: Edge) -> bool:
    """
    This method filters use-data edges.

    A use-data edge connects a data node with a mesh node.
    Thus, it gets tested, whether the start- and end-node are data- and mesh nodes respectively.

    Args:
         edge: The edge to check.

    Returns:
        True, if the edge is a use data edge.
    """
    n1, n2 = edge
    return (isinstance(n1, DataNode) and isinstance(n2, MeshNode) or
            isinstance(n1, MeshNode) and isinstance(n2, DataNode))


def is_read_data(edge) -> bool:
    """
    This method filters read-data edges.

    A read-data edge connects a data node with a read-data node.
    Thus, it gets tested, whether the start- and end-node are data- and read-data nodes respectively.

    Args:
         edge: The edge to check.

    Returns:
        True, if the edge is a read-data edge.
    """
    n1, n2 = edge
    return (isinstance(n1, DataNode) and isinstance(n2, ReadDataNode) or
            isinstance(n1, ReadDataNode) and isinstance(n2, DataNode))


def is_write_data(edge) -> bool:
    """
    This method filters write-data edges.

    A write-data edge connects a data node with a write-data node.
    Thus, it gets tested, whether the start- and end-node are data- and write-data nodes respectively.

    Args:
         edge: The edge to check.

    Returns:
        True, if the edge is a write-data edge.
    """
    n1, n2 = edge
    return (isinstance(n1, DataNode) and isinstance(n2, WriteDataNode) or
            isinstance(n1, WriteDataNode) and isinstance(n2, DataNode))
