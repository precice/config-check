from typing import List

import networkx as nx
from networkx import Graph
from precice_config_graph.edges import Edge
from precice_config_graph.nodes import DataNode, MeshNode, ReadDataNode, WriteDataNode, WatchpointNode, ExportNode, \
    WatchIntegralNode, ParticipantNode
from rule import Rule
from severity import Severity
from violation import Violation


class DataUseReadWrite(Rule):
    name = "There is a problem with using, reading and writing data."
    # This is an oversight, but not an error
    severity = Severity.WARNING

    class DataNotUsedNotReadNotWrittenViolation(Violation):
        """
            This violation handles nobody using, reading or writing a data node.
        """

        def __init__(self, data_node: DataNode):
            self.data_node = data_node

        def format_explanation(self) -> str:
            return f"Data {self.data_node.name} is declared but never used, read or written."

        def format_possible_solutions(self) -> List[str]:
            return [f"Consider using {self.data_node.name} in a mesh and have participants read and write it.",
                    "Otherwise please remove it to improve readability."]

    class DataUsedNotReadNotWrittenViolation(Violation):
        """
            This violation handles someone using a data node, but nobody is reading and writing said data node.
        """

        def __init__(self, data_node: DataNode, mesh: MeshNode):
            self.data_node = data_node
            self.mesh = mesh

        def format_explanation(self) -> str:
            return f"Data {self.data_node.name} gets used in mesh {self.mesh.name}, but nobody is reading or writing it."

        def format_possible_solutions(self) -> List[str]:
            return [f"Consider having a participant read data {self.data_node.name}.",
                    f"Consider having a participant write data {self.data_node.name}.",
                    "Otherwise please remove it to improve readability."]

    class DataUsedNotReadWrittenViolation(Violation):
        """
            This class handles someone using and writing a data node, but nobody reading said data node.
        """

        def __init__(self, data_node: DataNode, mesh: MeshNode, participant: ParticipantNode):
            self.data_node = data_node
            self.mesh = mesh
            self.participant = participant

        def format_explanation(self) -> str:
            return (
                f"Data {self.data_node.name} is used in mesh {self.mesh.name} and participant {self.participant.name} "
                f"is writing it, but nobody is reading it.")

        def format_possible_solutions(self) -> List[str]:
            return [f"Consider having a participant read data {self.data_node.name}.",
                    f"Consider exporting data {self.data_node.name} by a participant.",
                    f"Consider using watchpoints or watch-integrals to keep track of data {self.data_node.name}.",
                    "Otherwise please remove it to improve readability."]

    class DataUsedReadNotWrittenViolation(Violation):
        """
            This class handles someone using and reading a data node, but nobody writing said data node.
        """

        def __init__(self, data_node: DataNode, mesh: MeshNode,
                     reader: ReadDataNode | ExportNode | WatchpointNode | WatchIntegralNode):
            self.data_node = data_node
            self.mesh = mesh
            self.reader = reader
            if isinstance(reader, ReadDataNode):
                # If it is a read-data node, we have to get the participant it originates from
                self.reader = reader.participant
                self.type = "participant"
            elif isinstance(reader, ExportNode):
                self.type = "export"
            elif isinstance(reader, WatchpointNode):
                self.type = "watchpoint"
            elif isinstance(reader, WatchIntegralNode):
                self.type = "watch-integral"
            else:
                self.type = ""

        def format_explanation(self) -> str:
            return (
                f"Data {self.data_node.name} is being used in mesh {self.mesh.name} and {self.type} {self.reader.name} "
                f"is reading it, but nobody is writing it.")

        def format_possible_solutions(self) -> List[str]:
            return [f"Consider having a participant write {self.data_node.name}.",
                    "Otherwise please remove it to improve readability."]

    def check(self, graph: Graph) -> None:
        g1 = nx.subgraph_view(graph, filter_node=filter_use_read_write_data)
        for node in g1.nodes:
            # We only need to test data nodes here
            if isinstance(node, DataNode):
                use_data: bool = False
                read_data: bool = False
                write_data: bool = False
                mesh: MeshNode = None
                writer: ParticipantNode = None
                reader: ReadDataNode | ExportNode | WatchpointNode | WatchIntegralNode = None
                # Check all edges connected to the data node
                # TODO: What happens if multiple cases occur? Like multiple participants reading data node,
                #  but noone writing it
                for edge in g1.edges(node):
                    # Check if a mesh is using data-node
                    if is_use_data(edge):
                        use_data = True
                        # Get mesh using the data
                        mesh = get_mesh_node(edge)
                        # Check if the mesh has any connection to a "reader" node
                        # If yes, also remember who and that someone is reading the data node
                        mesh_edges = g1.edges(mesh)
                        for mesh_edge in mesh_edges:
                            if is_export(mesh_edge):
                                read_data = True
                                reader = get_reader_node(mesh_edge)
                            elif is_watchpoint(mesh_edge):
                                read_data = True
                                reader = get_reader_node(mesh_edge)
                            elif is_watch_integral(mesh_edge):
                                read_data = True
                                reader = get_reader_node(mesh_edge)
                    # Check if a participant is reading data-node
                    elif is_read_data(edge):
                        read_data = True
                        # Find out who is reading data-node: Overwrite result from above, as a participant is more
                        # important than a different "reader" node
                        reader = get_read_data_node(edge)
                    # Check if someone is writing data-node
                    elif is_write_data(edge):
                        write_data = True
                        # Find out who is writing data-node
                        writer = get_writer_node(edge)
                if use_data and read_data and write_data:
                    # Everything is fine here
                    continue
                elif use_data and read_data and not write_data:
                    self.violations.append(self.DataUsedReadNotWrittenViolation(node, mesh, reader))
                elif use_data and not read_data and write_data:
                    self.violations.append(self.DataUsedNotReadWrittenViolation(node, mesh, writer))
                elif use_data and not read_data and not write_data:
                    self.violations.append(self.DataUsedNotReadNotWrittenViolation(node, mesh))
                elif not use_data and read_data and write_data:
                    # This case gets handled by precice-tools check
                    continue
                elif not use_data and read_data and not write_data:
                    # This case gets handled by precice-tools check
                    continue
                elif not use_data and not read_data and write_data:
                    # This case gets handled by precice-tools check
                    continue
                elif not use_data and not read_data and not write_data:
                    self.violations.append(self.DataNotUsedNotReadNotWrittenViolation(node))

DataUseReadWrite()

def filter_use_read_write_data(node) -> bool:
    """
    This method filters nodes, that could potentially use data, read data or write data.

    A mesh is the only node that can "use" data.

    A read-data node, export, watchpoint or watch-integral are considered to "read" data.

    A write-data node is considered to "write" data.

    Args:
         node: The node to check.

    Returns:
        True, if the node is a data-, read-/write-, or mesh node.
    """
    return (isinstance(node, DataNode) or
            isinstance(node, MeshNode) or
            isinstance(node, ReadDataNode) or
            isinstance(node, ExportNode) or
            isinstance(node, WatchpointNode) or
            isinstance(node, WatchIntegralNode) or
            isinstance(node, WriteDataNode))


def get_mesh_node(edge: Edge) -> MeshNode | None:
    """
    Returns the mesh node of the given edge.

    This assumes the edge to connect a mesh node to a different node.
    If the edge connects two other nodes, then the behavior is undefined.

    Args:
        edge: The edge to get the mesh node from.

    Returns:
        The mesh node of the given edge.
    """
    node1, node2 = edge
    if isinstance(node1, MeshNode):
        return node1
    elif isinstance(node2, MeshNode):
        return node2
    else:
        return None


def get_reader_node(edge: Edge) -> ReadDataNode | ExportNode | WatchpointNode | WatchIntegralNode | None:
    """
    Returns the node of the given edge, which is a "reader" node.

    This assumes the edge to connect a "reader" node to a different node.
    A reader node is considered to "read" data and is of one of the following types:
    ReadData, Export, Watchpoint or WatchIntegral.
    Otherwise, the behavior of this function is undefined.

    Args:
        edge: The edge to get the "reader" node from.

    Returns:
        The "reader" node of the given edge.
    """
    n1, n2 = edge
    if isinstance(n1, ReadDataNode):
        return n1
    elif isinstance(n1, ExportNode):
        return n1
    elif isinstance(n1, WatchpointNode):
        return n1
    elif isinstance(n1, WatchIntegralNode):
        return n1
    elif isinstance(n2, ReadDataNode):
        return n1
    elif isinstance(n2, ExportNode):
        return n1
    elif isinstance(n2, WatchpointNode):
        return n1
    elif isinstance(n2, WatchIntegralNode):
        return n1
    else:
        return None


def get_read_data_node(edge: Edge) -> ReadDataNode | None:
    """
    Returns the read-data node of the given edge.

    This assumes the edge to connect a read-data node to a different node.
    Otherwise, the behavior of this function is undefined.

    Args:
        edge: The edge to get the read-data node from.

    Returns:
        The read-data node of the given edge.
    """
    n1, n2 = edge
    if isinstance(n1, ReadDataNode):
        return n1
    elif isinstance(n2, ReadDataNode):
        return n2
    else:
        return None


def get_writer_node(edge: Edge) -> ParticipantNode | None:
    """
    Returns the participant node of the given edge.

    This assumes the edge to connect a participant node to a different node.
    If the edge connects two other nodes, then the behavior is undefined.

    Args:
        edge: The edge to get the participant node from.

    Returns:
        The participant node of the given edge.
    """
    n1, n2 = edge
    if isinstance(n1, ParticipantNode):
        return n1
    elif isinstance(n2, ParticipantNode):
        return n2
    else:
        return None


def filter_data_read_write_data_mesh_nodes(node) -> bool:
    """
    This method filters data, read-/write-data and mesh nodes.

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

    A use-data edge connects a data node to a mesh node.
    Thus, it gets tested, whether the start- and end-node are data- and mesh nodes respectively.

    Args:
         edge: The edge to check.

    Returns:
        True, if the edge is a use-data edge.
    """
    n1, n2 = edge
    return (isinstance(n1, DataNode) and isinstance(n2, MeshNode) or
            isinstance(n1, MeshNode) and isinstance(n2, DataNode))


def is_read_data(edge) -> bool:
    """
    This method filters read-data edges.

    A read-data edge connects a data node to a read-data node.
    Thus, it gets tested, whether the start- and end-node ares data- and read-data nodes respectively.

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

    A write-data edge connects a data node to a write-data node.
    Thus, it gets tested, whether the start- and end-node ares data- and write-data nodes respectively.

    Args:
         edge: The edge to check.

    Returns:
        True, if the edge is a write-data edge.
    """
    n1, n2 = edge
    return (isinstance(n1, DataNode) and isinstance(n2, WriteDataNode) or
            isinstance(n1, WriteDataNode) and isinstance(n2, DataNode))


def is_export(edge) -> bool:
    """
    This method filters export-mesh edges.

    An export-mesh edge connects an export node to a mesh node.
    Thus, it gets tested, whether the start- and end-nodes are export- and mesh nodes respectively.

    Args:
         edge: The edge to check.

    Returns:
        True, if the edge is an export-mesh edge.
    """
    n1, n2 = edge
    return (isinstance(n1, MeshNode) and isinstance(n2, ExportNode) or
            isinstance(n1, ExportNode) and isinstance(n2, MeshNode))


def is_watchpoint(edge) -> bool:
    """
    This method filters watchpoint-mesh edges.

    A watchpoint-mesh edge connects a watchpoint node to a mesh node.
    Thus, it gets tested, whether the start- and end-nodes are watchpoint- and mesh nodes respectively.

    Args:
         edge: The edge to check.

    Returns:
        True, if the edge is a watchpoint-mesh edge.
    """
    n1, n2 = edge
    return (isinstance(n1, DataNode) and isinstance(n2, WatchpointNode) or
            isinstance(n1, WatchpointNode) and isinstance(n2, DataNode))


def is_watch_integral(edge) -> bool:
    """
    This method filters watch_integral-mesh edges.

    A watch_integral-mesh edge connects a watch-integral node to a mesh node.
    Thus, it gets tested, whether the start- and end-nodes are watch-integral- and mesh nodes respectively.

    Args:
         edge: The edge to check.

    Returns:
        True, if the edge is a watch_integral-mesh edge.
    """
    n1, n2 = edge
    return (isinstance(n1, DataNode) and isinstance(n2, WatchIntegralNode) or
            isinstance(n1, WatchIntegralNode) and isinstance(n2, DataNode))
