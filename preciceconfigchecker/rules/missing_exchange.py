import networkx as nx
from networkx import Graph
from precice_config_graph.nodes import DataNode, ExchangeNode, MeshNode, ParticipantNode, ReadDataNode, WriteDataNode
from rule import Rule
from severity import Severity
from violation import Violation


class MissingExchangeRule(Rule):
    # To communicate data, it needs to be exchanged in a coupling scheme. Declaring and using data,
    # but without an exchange is an error.
    severity = Severity.ERROR
    name = "Missing data exchange."

    class MissingExchangeViolation(Violation):
        """
        This class handles data, which does not get used, not getting exchanged either.
        """

        def __init__(self, data_node: DataNode) -> None:
            self.data_node = data_node

        def format_explanation(self) -> str:
            return f"Data {self.data_node.name} does not get exchanged in a coupling-scheme."

        def format_possible_solutions(self) -> list[str]:
            return [f"Please exchange {self.data_node.name} in a coupling-scheme.",
                    "Otherwise, please remove it to improve readability."]

    class MissingUseDataExchangeViolation(Violation):
        """
        This class handles data being used, read and written but not being exchanged in a coupling-scheme.
        """

        def __init__(self, data_node: DataNode, mesh: MeshNode, reader: ParticipantNode,
                     writer: ParticipantNode) -> None:
            self.data_node = data_node
            self.mesh = mesh
            self.writer = writer
            self.reader = reader

        def format_explanation(self) -> str:
            return (f"Data {self.data_node.name} is used in mesh {self.mesh.name}, gets written by participant {self.writer.name} "
                    f"and read by participant {self.reader.name}, but does not get exchanged in a coupling-scheme.")

        def format_possible_solutions(self) -> list[str]:
            return [f"Please exchange {self.data_node.name} in a coupling-scheme.",
                    f"Simply add the following line to a coupling-scheme involving participants {self.reader.name} and "
                    f"{self.writer.name}:\n "
                    f"<exchange data=\"{self.data_node.name}\" mesh=\"{self.mesh.name}\" from=\"{self.writer.name}\" to=\"{self.reader.name}\" />"]

    def check(self, graph: Graph) -> list[Violation]:
        # Only data and exchange nodes remain
        g1 = nx.subgraph_view(graph, filter_node=filter_data_exchange_nodes)

        violations = []

        for node in g1.nodes():
            # Check all data nodes
            if isinstance(node, DataNode):
                mesh: MeshNode = None
                reader: ParticipantNode = None
                writer: ParticipantNode = None
                # Get all neighboring nodes
                exchanges = g1.neighbors(node)
                # No adjacent nodes mean that there are no exchanges with this data-node
                if not list(exchanges):
                    # Now we have to get the mesh, reader and writer of data for the output message
                    for adjacent in graph.neighbors(node):
                        if isinstance(adjacent, MeshNode):
                            mesh = adjacent
                        elif isinstance(adjacent, ReadDataNode):
                            reader = adjacent.participant
                        elif isinstance(adjacent, WriteDataNode):
                            writer = adjacent.participant
                    # Data gets used, read and written
                    if mesh and reader and writer:
                        violations.append(self.MissingUseDataExchangeViolation(node, mesh, reader, writer))
                    # Data does not get used, read and written
                    else:
                        violations.append(self.MissingExchangeViolation(node))

        return violations


# Initialize a rule object to add it to the rules-array.
MissingExchangeRule()


# Helper functions
def filter_data_exchange_nodes(node) -> bool:
    """
    A function filtering data and exchange nodes in the graph.

    Args:
        node: the node to check

    Returns:
        True, if the node is a data or exchange node.
    """
    return isinstance(node, DataNode) or isinstance(node, ExchangeNode)
