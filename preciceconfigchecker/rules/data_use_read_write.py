from typing import List

import networkx as nx
from networkx import Graph
from precice_config_graph.nodes import DataNode, MeshNode, ReadDataNode, WriteDataNode, WatchpointNode, ExportNode, \
    WatchIntegralNode, ParticipantNode
from rule import Rule
from severity import Severity
from violation import Violation


class DataUseReadWrite(Rule):
    name = "Data rules."
    # These are oversights, but do not necessarily cause the simulation to malfunction.
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
            This class handles a mesh using and someone reading a data node, but nobody writing said data node.
        """

        def __init__(self, data_node: DataNode, mesh: MeshNode,
                     reader: ParticipantNode | ExportNode | WatchpointNode | WatchIntegralNode):
            self.data_node = data_node
            self.mesh = mesh
            self.reader = reader
            if isinstance(reader, ParticipantNode):
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
                reader: ParticipantNode | ExportNode | WatchpointNode | WatchIntegralNode = None
                for neighbor in g1.neighbors(node):
                    # Check if data gets used by a mesh
                    if isinstance(neighbor, MeshNode):
                        use_data = True
                        mesh = neighbor
                        mesh_neighbors = g1.neighbors(neighbor)
                        # Check if mesh gets observed by export, watchpoint or -integral
                        # These types of reader nodes are less important than a read-data node, thus only check them if
                        # no read-data node has been found
                        for mesh_neighbor in mesh_neighbors:
                            if isinstance(neighbor, ExportNode) and not read_data:
                                read_data = True
                                reader = mesh_neighbor
                            elif isinstance(neighbor, WatchpointNode) and not read_data:
                                read_data = True
                                reader = mesh_neighbor
                            elif isinstance(neighbor, WatchIntegralNode) and not read_data:
                                read_data = True
                                reader = neighbor
                    # Check if data gets read by a participant
                    elif isinstance(neighbor, ReadDataNode):
                        read_data = True
                        reader = neighbor.participant
                    elif isinstance(neighbor, WriteDataNode):
                        write_data = True
                        writer = neighbor.participant

                # Add violations according to use/read/write
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


# Initialize a rule object to add it to the rules-array.
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
